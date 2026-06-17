"""End-to-end tests for favorites/recently-viewed endpoints (issue #162).

Drives the public router with a learner principal override against the
in-memory DB.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.domain.auth_identity import UserPrincipal

pytestmark = pytest.mark.integration

_LEARNER = UserPrincipal(
    user_id=uuid.UUID("22222222-2222-2222-2222-222222222222"),
    username="learner",
    scopes=frozenset(),
    audience=None,
    expires_at=datetime(2999, 1, 1, tzinfo=UTC),
)
_OTHER = UserPrincipal(
    user_id=uuid.UUID("33333333-3333-3333-3333-333333333333"),
    username="other",
    scopes=frozenset(),
    audience=None,
    expires_at=datetime(2999, 1, 1, tzinfo=UTC),
)


@pytest.fixture
def learner_client(app: FastAPI, _prepared_schema: None) -> TestClient:
    app.dependency_overrides[require_principal] = lambda: _LEARNER
    return TestClient(app)


def test_add_list_and_delete_favorite(learner_client: TestClient) -> None:
    created = learner_client.post(
        "/api/v1/me/favorites", json={"type": "course", "ref": "quantum-101"}
    )
    assert created.status_code == 201
    body = created.json()
    assert body["type"] == "course"
    assert body["ref"] == "quantum-101"
    fav_id = body["id"]
    assert "addedAt" in body  # camelCase aliasing

    listed = learner_client.get("/api/v1/me/favorites")
    assert listed.status_code == 200
    assert [f["ref"] for f in listed.json()] == ["quantum-101"]

    deleted = learner_client.delete(f"/api/v1/me/favorites/{fav_id}")
    assert deleted.status_code == 204
    assert learner_client.get("/api/v1/me/favorites").json() == []


def test_favorite_is_idempotent(learner_client: TestClient) -> None:
    first = learner_client.post(
        "/api/v1/me/favorites", json={"type": "lesson", "ref": "l1"}
    )
    second = learner_client.post(
        "/api/v1/me/favorites", json={"type": "lesson", "ref": "l1"}
    )
    assert first.json()["id"] == second.json()["id"]
    assert len(learner_client.get("/api/v1/me/favorites").json()) == 1


def test_delete_missing_favorite_returns_404(learner_client: TestClient) -> None:
    resp = learner_client.delete(f"/api/v1/me/favorites/{uuid.uuid4()}")
    assert resp.status_code == 404


def test_invalid_favorite_type_rejected(learner_client: TestClient) -> None:
    resp = learner_client.post(
        "/api/v1/me/favorites", json={"type": "bogus", "ref": "x"}
    )
    assert resp.status_code == 422


def test_record_and_list_recent(learner_client: TestClient) -> None:
    learner_client.post("/api/v1/me/recent", json={"type": "course", "ref": "a"})
    learner_client.post("/api/v1/me/recent", json={"type": "course", "ref": "b"})
    # Re-viewing "a" bumps it to the front.
    learner_client.post("/api/v1/me/recent", json={"type": "course", "ref": "a"})

    recent = learner_client.get("/api/v1/me/recent")
    assert recent.status_code == 200
    refs = [v["ref"] for v in recent.json()]
    assert refs == ["a", "b"]
    assert len(refs) == 2  # no duplicate for re-viewed "a"


def test_recent_limit_is_enforced(learner_client: TestClient) -> None:
    for i in range(5):
        learner_client.post(
            "/api/v1/me/recent", json={"type": "note", "ref": f"n{i}"}
        )
    limited = learner_client.get("/api/v1/me/recent?limit=2")
    assert limited.status_code == 200
    assert len(limited.json()) == 2
    # Out-of-range limit is rejected by query validation.
    assert learner_client.get("/api/v1/me/recent?limit=0").status_code == 422


def test_favorites_are_user_scoped(app: FastAPI, _prepared_schema: None) -> None:
    app.dependency_overrides[require_principal] = lambda: _LEARNER
    me = TestClient(app)
    me.post("/api/v1/me/favorites", json={"type": "course", "ref": "mine"})

    app.dependency_overrides[require_principal] = lambda: _OTHER
    other = TestClient(app)
    assert other.get("/api/v1/me/favorites").json() == []
