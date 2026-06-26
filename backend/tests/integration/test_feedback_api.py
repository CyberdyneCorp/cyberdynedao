"""Integration tests for the learner-feedback channel (issue #233).

Drives the full API: a signed-in learner submits problem/feature feedback;
an admin reads and filters the triage queue; non-admins are refused.
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


def _learner() -> UserPrincipal:
    return UserPrincipal(
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
def learner_client(app: FastAPI, _prepared_schema: None) -> TestClient:
    app.dependency_overrides[require_principal] = _learner
    return TestClient(app)


@pytest.fixture
def admin_client(app: FastAPI, _prepared_schema: None) -> TestClient:
    app.dependency_overrides[require_editor] = _editor
    return TestClient(app)


def test_submit_problem_and_feature_then_admin_lists(
    learner_client: TestClient, admin_client: TestClient
) -> None:
    problem = learner_client.post(
        "/api/v1/feedback",
        json={
            "kind": "problem",
            "message": "Quiz 4 has no correct answer.",
            "courseId": "cheminformatics-basics",
            "platform": "ios",
            "appVersion": "1.4.2",
        },
    )
    assert problem.status_code == 201, problem.text
    body = problem.json()
    assert body["kind"] == "problem"
    assert body["status"] == "new"
    assert body["courseId"] == "cheminformatics-basics"
    assert body["platform"] == "ios"

    feature = learner_client.post(
        "/api/v1/feedback",
        json={"kind": "feature", "message": "Add a dark mode for the player."},
    )
    assert feature.status_code == 201, feature.text
    assert feature.json()["kind"] == "feature"

    # Admin sees both, newest first.
    listed = admin_client.get("/api/v1/admin/feedback")
    assert listed.status_code == 200, listed.text
    kinds = [f["kind"] for f in listed.json()]
    assert kinds == ["feature", "problem"]

    # Filter by kind and status.
    problems = admin_client.get("/api/v1/admin/feedback", params={"kind": "problem"})
    assert [f["kind"] for f in problems.json()] == ["problem"]
    new_only = admin_client.get("/api/v1/admin/feedback", params={"status": "new"})
    assert len(new_only.json()) == 2
    closed = admin_client.get("/api/v1/admin/feedback", params={"status": "closed"})
    assert closed.json() == []


def test_submit_rejects_unknown_kind(learner_client: TestClient) -> None:
    resp = learner_client.post(
        "/api/v1/feedback",
        json={"kind": "complaint", "message": "x"},
    )
    assert resp.status_code == 422


def test_submit_rejects_empty_message(learner_client: TestClient) -> None:
    resp = learner_client.post("/api/v1/feedback", json={"kind": "problem", "message": ""})
    assert resp.status_code == 422


@pytest.mark.usefixtures("_prepared_schema")
def test_admin_list_requires_editor(client: TestClient) -> None:
    # No auth → the admin queue is not readable.
    assert client.get("/api/v1/admin/feedback").status_code in (401, 403)
