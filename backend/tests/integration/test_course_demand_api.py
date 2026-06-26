"""Integration tests for the course/topic demand registry (issue #232).

A typed request and a Scan-to-Learn no-match for the same topic land in the
same cluster; the admin backlog returns clusters ranked by demand. Uses the
real SQLAlchemy adapter (in-memory) so the adapter's clustering is exercised.
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


def _learner(uid: str) -> UserPrincipal:
    return UserPrincipal(
        user_id=uuid.UUID(uid),
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


def _client(app: FastAPI, principal: UserPrincipal) -> TestClient:
    app.dependency_overrides[require_principal] = lambda: principal
    return TestClient(app)


@pytest.mark.usefixtures("_prepared_schema")
def test_typed_and_scan_cluster_then_admin_ranks(app: FastAPI) -> None:
    # Two different learners request the same topic via the two entry points.
    leo = _client(app, _learner("11111111-1111-1111-1111-111111111111"))
    typed = leo.post(
        "/api/v1/learning/course-requests",
        json={"topic": "Eigenvalues", "source": "typed", "subject": "Linear Algebra"},
    )
    assert typed.status_code == 201, typed.text
    assert typed.json()["topicKey"] == "eigenvalues"
    assert typed.json()["source"] == "typed"

    eshani = _client(app, _learner("22222222-2222-2222-2222-222222222222"))
    scan = eshani.post(
        "/api/v1/learning/course-requests",
        json={
            "topic": "eigenvalues?",
            "source": "scan",
            "sourceQuestionText": "Find the eigenvalues of A",
        },
    )
    assert scan.status_code == 201, scan.text

    # A third learner asks for a different, less-wanted topic.
    santino = _client(app, _learner("33333333-3333-3333-3333-333333333333"))
    santino.post(
        "/api/v1/learning/course-requests",
        json={"topic": "Topology", "source": "typed"},
    )

    app.dependency_overrides[require_editor] = _editor
    admin = TestClient(app)
    listed = admin.get("/api/v1/admin/learning/course-requests")
    assert listed.status_code == 200, listed.text
    clusters = listed.json()
    # eigenvalues (2) ranks above topology (1); the two eigenvalues entry points
    # collapsed into one cluster.
    assert [(c["topicKey"], c["count"]) for c in clusters] == [
        ("eigenvalues", 2),
        ("topology", 1),
    ]


@pytest.mark.usefixtures("_prepared_schema")
def test_submit_rejects_unknown_source(app: FastAPI) -> None:
    client = _client(app, _learner("11111111-1111-1111-1111-111111111111"))
    resp = client.post(
        "/api/v1/learning/course-requests",
        json={"topic": "x", "source": "voice"},
    )
    assert resp.status_code == 422


@pytest.mark.usefixtures("_prepared_schema")
def test_admin_list_requires_editor(client: TestClient) -> None:
    assert client.get("/api/v1/admin/learning/course-requests").status_code in (401, 403)
