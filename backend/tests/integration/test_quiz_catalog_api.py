"""End-to-end tests for the browse-quizzes catalogue endpoint (#169).

Seeds two published courses (one categorized) plus a draft course, each
with a lesson + quiz, and a learner attempt on one quiz. Then drives
GET /api/v1/quizzes with a learner principal override.
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
from cyberdyne_backend.adapters.outbound.persistence.courses.models import (
    CategoryRow,
    CourseRow,
    LessonRow,
)
from cyberdyne_backend.adapters.outbound.persistence.quizzes.models import (
    QuizAttemptRow,
    QuizOptionRow,
    QuizQuestionRow,
    QuizRow,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.infrastructure.database.engine import get_session_factory

pytestmark = pytest.mark.integration

_USER = uuid.UUID("44444444-4444-4444-4444-444444444444")
_NOW = datetime(2026, 1, 1, tzinfo=UTC)

_CAT = uuid.uuid4()
_COURSE_PUB = uuid.uuid4()
_COURSE_PUB2 = uuid.uuid4()
_COURSE_DRAFT = uuid.uuid4()
_LESSON_PUB = uuid.uuid4()
_LESSON_PUB2 = uuid.uuid4()
_LESSON_DRAFT = uuid.uuid4()
_QUIZ_PUB = uuid.uuid4()
_QUIZ_PUB2 = uuid.uuid4()
_QUIZ_DRAFT = uuid.uuid4()


def _learner() -> UserPrincipal:
    return UserPrincipal(
        user_id=_USER,
        username="learner",
        scopes=frozenset(),
        audience=None,
        expires_at=datetime(2999, 1, 1, tzinfo=UTC),
    )


def _course(id_, slug, status, *, category_id=None) -> CourseRow:
    return CourseRow(
        id=id_,
        slug=slug,
        title=slug.upper(),
        description="d",
        level="Beginner",
        status=status,
        mandatory=False,
        sort_order=1,
        category_id=category_id,
        created_at=_NOW,
    )


def _lesson(id_, course_id, title) -> LessonRow:
    return LessonRow(
        id=id_,
        course_id=course_id,
        title=title,
        lesson_type="text",
        sort_order=1,
        created_at=_NOW,
    )


def _quiz_with_two_questions(quiz_id, lesson_id) -> list:
    rows: list = [
        QuizRow(
            id=quiz_id,
            lesson_id=lesson_id,
            passing_score=70,
            created_at=_NOW,
        )
    ]
    for i in range(2):
        q_id = uuid.uuid4()
        rows.append(
            QuizQuestionRow(
                id=q_id,
                quiz_id=quiz_id,
                prompt=f"q{i}",
                explanation="",
                sort_order=i,
            )
        )
        rows.append(QuizOptionRow(id=uuid.uuid4(), question_id=q_id, text="a", is_correct=True))
        rows.append(QuizOptionRow(id=uuid.uuid4(), question_id=q_id, text="b", is_correct=False))
    return rows


@pytest_asyncio.fixture
async def seeded(_prepared_schema: None) -> AsyncIterator[None]:
    factory = get_session_factory()
    async with factory() as s:
        s.add(CategoryRow(id=_CAT, slug="programming", name="Programming", created_at=_NOW))
        s.add_all(
            [
                _course(_COURSE_PUB, "alpha", "published", category_id=_CAT),
                _course(_COURSE_PUB2, "beta", "published"),
                _course(_COURSE_DRAFT, "draft-course", "draft"),
                _lesson(_LESSON_PUB, _COURSE_PUB, "Alpha Lesson"),
                _lesson(_LESSON_PUB2, _COURSE_PUB2, "Beta Lesson"),
                _lesson(_LESSON_DRAFT, _COURSE_DRAFT, "Draft Lesson"),
            ]
        )
        s.add_all(_quiz_with_two_questions(_QUIZ_PUB, _LESSON_PUB))
        s.add_all(_quiz_with_two_questions(_QUIZ_PUB2, _LESSON_PUB2))
        s.add_all(_quiz_with_two_questions(_QUIZ_DRAFT, _LESSON_DRAFT))
        # Two attempts by the learner on the alpha quiz; the later one wins.
        s.add_all(
            [
                QuizAttemptRow(
                    id=uuid.uuid4(),
                    user_id=_USER,
                    quiz_id=_QUIZ_PUB,
                    lesson_id=_LESSON_PUB,
                    score=50,
                    passed=False,
                    attempt_number=1,
                    answers={},
                    submitted_at=_NOW,
                ),
                QuizAttemptRow(
                    id=uuid.uuid4(),
                    user_id=_USER,
                    quiz_id=_QUIZ_PUB,
                    lesson_id=_LESSON_PUB,
                    score=90,
                    passed=True,
                    attempt_number=2,
                    answers={},
                    submitted_at=_NOW,
                ),
            ]
        )
        await s.commit()
    yield


@pytest.fixture
def learner_client(app: FastAPI) -> TestClient:
    app.dependency_overrides[require_principal] = _learner
    return TestClient(app)


def test_browse_lists_published_quizzes_only(seeded: None, learner_client: TestClient) -> None:
    resp = learner_client.get("/api/v1/quizzes")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    slugs = [it["courseSlug"] for it in body["items"]]
    assert slugs == ["alpha", "beta"]  # draft excluded, ordered by slug
    assert body["nextCursor"] is None
    # question_count + metadata populated.
    alpha = body["items"][0]
    assert alpha["questionCount"] == 2
    assert alpha["lessonTitle"] == "Alpha Lesson"
    assert alpha["passingScore"] == 70


def test_last_attempt_is_the_latest(seeded: None, learner_client: TestClient) -> None:
    body = learner_client.get("/api/v1/quizzes").json()
    alpha = next(it for it in body["items"] if it["courseSlug"] == "alpha")
    assert alpha["lastAttempt"]["score"] == 90
    assert alpha["lastAttempt"]["attemptNumber"] == 2
    assert alpha["lastAttempt"]["passed"] is True
    # Beta has no attempt for this learner.
    beta = next(it for it in body["items"] if it["courseSlug"] == "beta")
    assert beta["lastAttempt"] is None


def test_filter_by_course_slug(seeded: None, learner_client: TestClient) -> None:
    body = learner_client.get("/api/v1/quizzes?courseSlug=beta").json()
    assert [it["courseSlug"] for it in body["items"]] == ["beta"]


def test_filter_by_domain_category(seeded: None, learner_client: TestClient) -> None:
    body = learner_client.get("/api/v1/quizzes?domain=programming").json()
    assert [it["courseSlug"] for it in body["items"]] == ["alpha"]


def test_pagination_with_cursor(seeded: None, learner_client: TestClient) -> None:
    first = learner_client.get("/api/v1/quizzes?limit=1").json()
    assert [it["courseSlug"] for it in first["items"]] == ["alpha"]
    assert first["nextCursor"] is not None

    second = learner_client.get(f"/api/v1/quizzes?limit=1&cursor={first['nextCursor']}").json()
    assert [it["courseSlug"] for it in second["items"]] == ["beta"]
    assert second["nextCursor"] is None


def test_malformed_cursor_starts_from_beginning(seeded: None, learner_client: TestClient) -> None:
    body = learner_client.get("/api/v1/quizzes?cursor=not-a-cursor").json()
    assert [it["courseSlug"] for it in body["items"]] == ["alpha", "beta"]


def test_limit_out_of_range_rejected(seeded: None, learner_client: TestClient) -> None:
    assert learner_client.get("/api/v1/quizzes?limit=0").status_code == 422
    assert learner_client.get("/api/v1/quizzes?limit=101").status_code == 422
