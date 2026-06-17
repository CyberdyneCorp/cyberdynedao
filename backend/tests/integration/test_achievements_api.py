"""End-to-end tests for the achievements endpoint (issue #163)."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.adapters.outbound.persistence.courses.models import (
    CourseCertificateRow,
)
from cyberdyne_backend.adapters.outbound.persistence.learning.models import (
    ModuleProgressRow,
)
from cyberdyne_backend.adapters.outbound.persistence.quizzes.models import (
    QuizAttemptRow,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.infrastructure.database.engine import get_session_factory

pytestmark = pytest.mark.integration

_USER = uuid.UUID("88888888-8888-8888-8888-888888888888")
_NOW = datetime(2026, 6, 17, 12, 0, tzinfo=UTC)


def _learner() -> UserPrincipal:
    return UserPrincipal(
        user_id=_USER,
        username="learner",
        scopes=frozenset(),
        audience=None,
        expires_at=datetime(2999, 1, 1, tzinfo=UTC),
    )


def _attempt(score: int, passed: bool) -> QuizAttemptRow:
    return QuizAttemptRow(
        id=uuid.uuid4(),
        user_id=_USER,
        quiz_id=uuid.uuid4(),
        lesson_id=uuid.uuid4(),
        score=score,
        passed=passed,
        attempt_number=1,
        answers={},
        submitted_at=_NOW,
    )


async def _seed() -> None:
    factory = get_session_factory()
    async with factory() as s:
        s.add(
            CourseCertificateRow(
                id=uuid.uuid4(),
                user_id=_USER,
                course_slug="c1",
                issued_at=_NOW,
                verification_hash="h",
                signed_payload="p",
            )
        )
        s.add_all([_attempt(85, True), _attempt(100, True)])
        s.add(
            ModuleProgressRow(
                id=uuid.uuid4(),
                user_id=_USER,
                module_slug="m1",
                percent=100,
                started_at=_NOW,
            )
        )
        await s.commit()


@pytest.fixture
def client(app: FastAPI, _prepared_schema: None) -> TestClient:
    app.dependency_overrides[require_principal] = lambda: _learner()
    return TestClient(app)


def test_earned_and_in_progress(client: TestClient) -> None:
    import asyncio

    asyncio.run(_seed())

    resp = client.get("/api/v1/achievements/me")
    assert resp.status_code == 200, resp.text
    by_key = {a["key"]: a for a in resp.json()}

    # Earned (thresholds of 1 reached).
    assert by_key["first_course"]["earnedAt"] is not None
    assert by_key["first_quiz"]["earnedAt"] is not None
    assert by_key["first_certificate"]["earnedAt"] is not None

    # In progress with real current/target.
    assert by_key["five_courses"]["earnedAt"] is None
    assert by_key["five_courses"]["progress"] == {"current": 1, "target": 5}
    assert by_key["quiz_master"]["progress"] == {"current": 2, "target": 10}
    assert by_key["perfectionist"]["progress"] == {"current": 1, "target": 5}
    assert by_key["module_explorer"]["progress"] == {"current": 1, "target": 5}

    # id mirrors key for client compatibility.
    assert by_key["first_course"]["id"] == "first_course"


def test_fresh_learner_has_all_in_progress(client: TestClient) -> None:
    body = client.get("/api/v1/achievements/me").json()
    assert len(body) >= 9
    assert all(a["earnedAt"] is None for a in body)
    assert all(a["progress"]["current"] == 0 for a in body)


def test_earned_at_is_stable_across_reads(client: TestClient) -> None:
    import asyncio

    asyncio.run(_seed())

    first = {a["key"]: a["earnedAt"] for a in client.get("/api/v1/achievements/me").json()}
    second = {a["key"]: a["earnedAt"] for a in client.get("/api/v1/achievements/me").json()}
    # The award timestamp is persisted, so it doesn't drift on re-read.
    assert first["first_course"] == second["first_course"]
    assert first["first_course"] is not None
