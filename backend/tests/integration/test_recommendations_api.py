"""End-to-end API tests for the course-recommendations endpoint.

Drives router -> use case -> SQLAlchemy -> in-memory sqlite. Courses are
authored + published via the admin API; the learner has no progress, so
the deterministic ranking targets Beginner. The LLM summary comes from
the offline ``StaticChatClient`` (no ``OPENAI_API_KEY`` in tests), so it
is deterministic and non-empty.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.middleware.auth import (
    require_editor,
    require_principal,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal

pytestmark = pytest.mark.integration

_LEARNER = UserPrincipal(
    user_id=uuid.UUID("22222222-2222-2222-2222-222222222222"),
    username="learner",
    scopes=frozenset(),
    audience=None,
    expires_at=datetime(2999, 1, 1, tzinfo=UTC),
)


def _editor() -> UserPrincipal:
    return UserPrincipal(
        user_id=uuid.uuid4(),
        username="editor",
        scopes=frozenset({"editor"}),
        audience=None,
        expires_at=datetime(2999, 1, 1, tzinfo=UTC),
    )


@pytest.fixture
def authed_client(app: FastAPI) -> TestClient:
    app.dependency_overrides[require_editor] = _editor
    app.dependency_overrides[require_principal] = lambda: _LEARNER
    return TestClient(app)


def _publish_course(client: TestClient, title: str, level: str) -> None:
    create = client.post(
        "/api/v1/admin/courses",
        json={"title": title, "description": "d", "level": level},
    )
    assert create.status_code == 201, create.text
    slug = create.json()["slug"]
    assert client.post(f"/api/v1/admin/courses/{slug}/publish").status_code == 200


@pytest.mark.usefixtures("_prepared_schema")
def test_recommendations_for_fresh_learner(authed_client: TestClient) -> None:
    _publish_course(authed_client, "Advanced Topic", "Advanced")
    _publish_course(authed_client, "Getting Started", "Beginner")

    resp = authed_client.get("/api/v1/recommendations/me")
    assert resp.status_code == 200, resp.text
    body = resp.json()

    assert body["summary"]  # offline canned reply, non-empty
    titles = [c["title"] for c in body["courses"]]
    # No progress -> Beginner targeted -> beginner course ranks first.
    assert titles[0] == "Getting Started"
    assert body["courses"][0]["reason"] == "Matches your current level"
    assert {"slug", "title", "level", "reason"} == set(body["courses"][0].keys())


@pytest.mark.usefixtures("_prepared_schema")
def test_recommendations_empty_catalogue(authed_client: TestClient) -> None:
    resp = authed_client.get("/api/v1/recommendations/me")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["courses"] == []
    assert "no published courses" in body["summary"].lower()


def test_recommendations_require_auth(client: TestClient) -> None:
    assert client.get("/api/v1/recommendations/me").status_code in (401, 403)
