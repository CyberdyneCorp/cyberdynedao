"""End-to-end analytics tests — exercises the real aggregation queries.

Seeds enrollments, progress, quiz attempts, courses, catalogue, and a
certificate for one learner, then asserts the learner dashboard and the
admin overview compute the expected figures.
"""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator
from datetime import UTC, datetime

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.middleware.auth import (
    require_editor,
    require_principal,
)
from cyberdyne_backend.adapters.outbound.persistence.courses.models import CourseRow
from cyberdyne_backend.adapters.outbound.persistence.learning.models import (
    CertificateRow,
    EnrollmentRow,
    LearningModuleRow,
    LearningPathRow,
    ModuleProgressRow,
)
from cyberdyne_backend.adapters.outbound.persistence.quizzes.models import QuizAttemptRow
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.infrastructure.database.engine import get_session_factory

pytestmark = pytest.mark.integration

_USER = uuid.UUID("33333333-3333-3333-3333-333333333333")
_NOW = datetime(2026, 1, 1, tzinfo=UTC)
_QUIZ_A = uuid.uuid4()
_QUIZ_B = uuid.uuid4()
_LESSON = uuid.uuid4()


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
async def seeded(_prepared_schema: None) -> AsyncIterator[None]:
    factory = get_session_factory()
    async with factory() as s:
        s.add_all(
            [
                EnrollmentRow(
                    id=uuid.uuid4(),
                    user_id=_USER,
                    path_slug="p1",
                    started_at=_NOW,
                    status="completed",
                ),
                EnrollmentRow(
                    id=uuid.uuid4(), user_id=_USER, path_slug="p2", started_at=_NOW, status="active"
                ),
                ModuleProgressRow(
                    id=uuid.uuid4(),
                    user_id=_USER,
                    module_slug="m1",
                    percent=100,
                    started_at=_NOW,
                    completed_at=_NOW,
                    updated_at=_NOW,
                ),
                ModuleProgressRow(
                    id=uuid.uuid4(),
                    user_id=_USER,
                    module_slug="m2",
                    percent=50,
                    started_at=_NOW,
                    completed_at=None,
                    updated_at=_NOW,
                ),
                CertificateRow(
                    id=uuid.uuid4(),
                    user_id=_USER,
                    path_slug="p1",
                    issued_at=_NOW,
                    verification_hash="h",
                    signed_payload="s",
                ),
                # Quiz A: best 90, passed. Quiz B: 40, failed.
                QuizAttemptRow(
                    id=uuid.uuid4(),
                    user_id=_USER,
                    quiz_id=_QUIZ_A,
                    lesson_id=_LESSON,
                    score=60,
                    passed=False,
                    attempt_number=1,
                    answers={},
                    submitted_at=_NOW,
                ),
                QuizAttemptRow(
                    id=uuid.uuid4(),
                    user_id=_USER,
                    quiz_id=_QUIZ_A,
                    lesson_id=_LESSON,
                    score=90,
                    passed=True,
                    attempt_number=2,
                    answers={},
                    submitted_at=_NOW,
                ),
                QuizAttemptRow(
                    id=uuid.uuid4(),
                    user_id=_USER,
                    quiz_id=_QUIZ_B,
                    lesson_id=_LESSON,
                    score=40,
                    passed=False,
                    attempt_number=1,
                    answers={},
                    submitted_at=_NOW,
                ),
                LearningModuleRow(
                    slug="m1",
                    title="M1",
                    category="c",
                    description="d",
                    level="Beginner",
                    duration="1h",
                    icon="x",
                    topics=[],
                    sort_order=1,
                ),
                LearningModuleRow(
                    slug="m2",
                    title="M2",
                    category="c",
                    description="d",
                    level="Beginner",
                    duration="1h",
                    icon="x",
                    topics=[],
                    sort_order=2,
                ),
                LearningPathRow(
                    slug="p1",
                    title="P1",
                    description="d",
                    module_slugs=["m1", "m2"],
                    estimated_time="4w",
                    icon="x",
                    sort_order=1,
                ),
                CourseRow(
                    id=uuid.uuid4(),
                    slug="c-pub",
                    title="Pub",
                    description="d",
                    level="Beginner",
                    status="published",
                    mandatory=False,
                    sort_order=1,
                    created_at=_NOW,
                ),
                CourseRow(
                    id=uuid.uuid4(),
                    slug="c-draft",
                    title="Draft",
                    description="d",
                    level="Beginner",
                    status="draft",
                    mandatory=False,
                    sort_order=2,
                    created_at=_NOW,
                ),
            ]
        )
        await s.commit()
    yield


@pytest.fixture
def learner_client(app: FastAPI) -> TestClient:
    app.dependency_overrides[require_principal] = _learner
    return TestClient(app)


@pytest.fixture
def editor_client(app: FastAPI) -> TestClient:
    app.dependency_overrides[require_editor] = _editor
    return TestClient(app)


def test_learner_dashboard(seeded: None, learner_client: TestClient) -> None:
    resp = learner_client.get("/api/v1/analytics/me")
    assert resp.status_code == 200, resp.text
    d = resp.json()
    assert d["enrolledPaths"] == 2
    assert d["completedPaths"] == 1
    assert d["activePaths"] == 1
    assert d["completedModules"] == 1
    assert d["inProgressModules"] == 1
    assert d["avgModulePercent"] == 75.0
    assert d["quizzesAttempted"] == 2
    assert d["quizzesPassed"] == 1
    assert d["quizPassRate"] == 50.0
    assert d["avgQuizScore"] == 65.0  # mean(best 90, 40)
    assert d["totalQuizAttempts"] == 3
    assert d["certificates"] == 1


def test_admin_overview(seeded: None, editor_client: TestClient) -> None:
    resp = editor_client.get("/api/v1/admin/analytics/overview")
    assert resp.status_code == 200, resp.text
    o = resp.json()
    assert o["totalLearners"] == 1
    assert o["totalEnrollments"] == 2
    assert o["completedEnrollments"] == 1
    assert o["enrollmentCompletionRate"] == 50.0
    assert o["publishedCourses"] == 1
    assert o["draftCourses"] == 1
    assert o["totalModules"] == 2
    assert o["totalPaths"] == 1
    assert o["totalCertificates"] == 1
    assert o["totalQuizAttempts"] == 3
    assert o["avgQuizScore"] == 63.3  # (60+90+40)/3
    assert o["quizPassRate"] == 33.3  # 1/3 passed


def test_learner_dashboard_requires_auth(client: TestClient) -> None:
    assert client.get("/api/v1/analytics/me").status_code in (401, 403)


def test_admin_overview_requires_editor(client: TestClient) -> None:
    assert client.get("/api/v1/admin/analytics/overview").status_code in (401, 403)


@pytest.mark.usefixtures("_prepared_schema")
def test_empty_dashboard_is_zeroed(learner_client: TestClient) -> None:
    # Tables exist but hold no rows for this user → all-zero dashboard.
    d = learner_client.get("/api/v1/analytics/me").json()
    assert d["enrolledPaths"] == 0
    assert d["avgQuizScore"] == 0.0
    assert d["quizPassRate"] == 0.0
