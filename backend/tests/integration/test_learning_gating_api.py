"""End-to-end tests for the learning gating + eligibility endpoints.

Seeds a small catalogue directly into the in-memory DB, then drives the
public router with a learner principal override.
"""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator
from datetime import UTC, datetime

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.adapters.outbound.persistence.learning.models import (
    LearningModuleRow,
    LearningPathRow,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.infrastructure.database.engine import get_session_factory

pytestmark = pytest.mark.integration

_LEARNER = UserPrincipal(
    user_id=uuid.UUID("22222222-2222-2222-2222-222222222222"),
    username="learner",
    scopes=frozenset(),
    audience=None,
    expires_at=datetime(2999, 1, 1, tzinfo=UTC),
)


@pytest_asyncio.fixture
async def seeded(_prepared_schema: None) -> AsyncIterator[None]:
    factory = get_session_factory()
    async with factory() as session:
        session.add_all(
            [
                LearningModuleRow(
                    slug="b1",
                    title="Beginner One",
                    category="c",
                    description="d",
                    level="Beginner",
                    duration="1h",
                    icon="x",
                    topics=[],
                    sort_order=10,
                ),
                LearningModuleRow(
                    slug="i1",
                    title="Intermediate One",
                    category="c",
                    description="d",
                    level="Intermediate",
                    duration="1h",
                    icon="x",
                    topics=[],
                    sort_order=20,
                ),
                LearningPathRow(
                    slug="p1",
                    title="Path",
                    description="d",
                    module_slugs=["b1", "i1"],
                    estimated_time="4w",
                    icon="x",
                    sort_order=10,
                ),
            ]
        )
        await session.commit()
    yield


@pytest.fixture
def learner_client(app: FastAPI) -> TestClient:
    app.dependency_overrides[require_principal] = lambda: _LEARNER
    return TestClient(app)


def test_gating_locks_intermediate_until_beginner_done(
    seeded: None, learner_client: TestClient
) -> None:
    resp = learner_client.get("/api/v1/learning/paths/p1/gating")
    assert resp.status_code == 200, resp.text
    gates = {g["moduleSlug"]: g for g in resp.json()}
    assert gates["b1"]["unlocked"] is True
    assert gates["i1"]["unlocked"] is False
    assert gates["i1"]["blockedBy"] == "b1"
    assert gates["i1"]["reason"] == "level"


def test_eligibility_reports_next_module(seeded: None, learner_client: TestClient) -> None:
    resp = learner_client.get("/api/v1/learning/paths/p1/eligibility")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["eligible"] is True
    assert body["alreadyEnrolled"] is False
    assert body["nextModule"] == "b1"


def test_gating_unknown_path_404(seeded: None, learner_client: TestClient) -> None:
    assert learner_client.get("/api/v1/learning/paths/ghost/gating").status_code == 404


def test_gating_requires_auth(client: TestClient) -> None:
    assert client.get("/api/v1/learning/paths/p1/gating").status_code in (401, 403)
