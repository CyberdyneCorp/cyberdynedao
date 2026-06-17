"""End-to-end tests for the activity + learner-stats endpoints (#164)."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.domain.auth_identity import UserPrincipal

pytestmark = pytest.mark.integration

_USER = uuid.UUID("55555555-5555-5555-5555-555555555555")
_OTHER = uuid.UUID("66666666-6666-6666-6666-666666666666")


def _principal(user_id: uuid.UUID) -> UserPrincipal:
    return UserPrincipal(
        user_id=user_id,
        username="learner",
        scopes=frozenset(),
        audience=None,
        expires_at=datetime(2999, 1, 1, tzinfo=UTC),
    )


@pytest.fixture
def client(app: FastAPI, _prepared_schema: None) -> TestClient:
    app.dependency_overrides[require_principal] = lambda: _principal(_USER)
    return TestClient(app)


def test_record_then_stats_reflect_counts(client: TestClient) -> None:
    for kind in ["code_run", "code_run", "simulation_run"]:
        resp = client.post("/api/v1/me/activity", json={"kind": kind})
        assert resp.status_code == 201, resp.text
    client.post(
        "/api/v1/me/activity", json={"kind": "concept_mastered", "ref": "ohms-law"}
    )
    client.post(
        "/api/v1/me/activity", json={"kind": "concept_mastered", "ref": "ohms-law"}
    )

    stats = client.get("/api/v1/me/stats")
    assert stats.status_code == 200, stats.text
    body = stats.json()
    assert body["codeRunsCount"] == 2
    assert body["simulationsRun"] == 1
    assert body["conceptsMastered"] == 1  # deduped by ref
    # Activity happened today → a 1-day streak.
    assert body["currentStreakDays"] == 1
    assert body["lastActiveOn"] is not None


def test_empty_stats_are_zeroed(client: TestClient) -> None:
    body = client.get("/api/v1/me/stats").json()
    assert body == {
        "currentStreakDays": 0,
        "longestStreakDays": 0,
        "lastActiveOn": None,
        "codeRunsCount": 0,
        "simulationsRun": 0,
        "conceptsMastered": 0,
    }


def test_invalid_kind_rejected(client: TestClient) -> None:
    resp = client.post("/api/v1/me/activity", json={"kind": "bogus"})
    assert resp.status_code == 422


def test_tz_offset_out_of_range_rejected(client: TestClient) -> None:
    assert client.get("/api/v1/me/stats?tzOffsetMinutes=99999").status_code == 422


def test_activity_is_user_scoped(app: FastAPI, _prepared_schema: None) -> None:
    app.dependency_overrides[require_principal] = lambda: _principal(_USER)
    me = TestClient(app)
    me.post("/api/v1/me/activity", json={"kind": "code_run"})

    app.dependency_overrides[require_principal] = lambda: _principal(_OTHER)
    other = TestClient(app)
    assert other.get("/api/v1/me/stats").json()["codeRunsCount"] == 0
