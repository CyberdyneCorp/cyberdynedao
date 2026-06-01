"""End-to-end tests for the enrollment-deadline endpoints."""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.middleware.auth import (
    require_editor,
    require_principal,
)
from cyberdyne_backend.adapters.outbound.persistence.learning.models import EnrollmentRow
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.infrastructure.database.engine import get_session_factory

pytestmark = pytest.mark.integration

_USER = uuid.UUID("44444444-4444-4444-4444-444444444444")
_NOW = datetime(2026, 6, 1, 12, 0, tzinfo=UTC)


def _learner() -> UserPrincipal:
    return UserPrincipal(
        user_id=_USER, username="l", scopes=frozenset(), audience=None, expires_at=_NOW
    )


def _editor() -> UserPrincipal:
    return UserPrincipal(
        user_id=uuid.uuid4(),
        username="e",
        scopes=frozenset({"editor"}),
        audience=None,
        expires_at=_NOW,
    )


@pytest_asyncio.fixture
async def enrolled(_prepared_schema: None) -> AsyncIterator[None]:
    factory = get_session_factory()
    async with factory() as s:
        s.add(
            EnrollmentRow(
                id=uuid.uuid4(),
                user_id=_USER,
                path_slug="p1",
                started_at=_NOW,
                status="active",
                due_at=None,
            )
        )
        await s.commit()
    yield


@pytest.fixture
def both_client(app: FastAPI) -> TestClient:
    app.dependency_overrides[require_principal] = _learner
    app.dependency_overrides[require_editor] = _editor
    return TestClient(app)


def test_set_and_list_deadline(enrolled: None, both_client: TestClient) -> None:
    # No deadline yet → status none.
    initial = both_client.get("/api/v1/learning/deadlines").json()
    assert initial[0]["status"] == "none"
    assert initial[0]["dueAt"] is None

    # Admin sets a deadline far in the future → upcoming.
    due = (_NOW + timedelta(days=30)).isoformat()
    resp = both_client.patch(
        f"/api/v1/admin/learning/enrollments/{_USER}/p1/deadline",
        json={"dueAt": due},
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["dueAt"] is not None

    listed = both_client.get("/api/v1/learning/deadlines").json()
    assert listed[0]["status"] == "upcoming"
    assert listed[0]["daysRemaining"] is not None

    # Clear it again.
    cleared = both_client.patch(
        f"/api/v1/admin/learning/enrollments/{_USER}/p1/deadline",
        json={"dueAt": None},
    )
    assert cleared.status_code == 200
    assert cleared.json()["dueAt"] is None


def test_set_deadline_unknown_enrollment_404(enrolled: None, both_client: TestClient) -> None:
    resp = both_client.patch(
        f"/api/v1/admin/learning/enrollments/{uuid.uuid4()}/ghost/deadline",
        json={"dueAt": None},
    )
    assert resp.status_code == 404


def test_deadlines_requires_auth(client: TestClient) -> None:
    assert client.get("/api/v1/learning/deadlines").status_code in (401, 403)
