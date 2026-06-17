"""End-to-end test for the Skill Map endpoint (issue #165).

Seeds a category hierarchy (Engineering Math → Linear Algebra,
Differential Equations; plus a top-level Programming), published courses
with lessons + the learner's progress, and a quiz attempt — then asserts
GET /api/v1/skills/me derives the expected mastery + weak areas.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.adapters.outbound.persistence.courses.models import (
    CategoryRow,
    CourseRow,
    LessonProgressRow,
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

_USER = uuid.UUID("77777777-7777-7777-7777-777777777777")
_NOW = datetime(2026, 1, 1, tzinfo=UTC)

_MATH = uuid.uuid4()
_LINALG = uuid.uuid4()
_DIFFEQ = uuid.uuid4()
_PROG = uuid.uuid4()


def _learner() -> UserPrincipal:
    return UserPrincipal(
        user_id=_USER,
        username="learner",
        scopes=frozenset(),
        audience=None,
        expires_at=datetime(2999, 1, 1, tzinfo=UTC),
    )


def _course(id_, slug, category_id, status="published") -> CourseRow:
    return CourseRow(
        id=id_,
        slug=slug,
        title=slug,
        description="d",
        level="Beginner",
        status=status,
        mandatory=False,
        sort_order=1,
        category_id=category_id,
        created_at=_NOW,
    )


def _lesson(id_, course_id) -> LessonRow:
    return LessonRow(
        id=id_,
        course_id=course_id,
        title="L",
        lesson_type="text",
        sort_order=1,
        created_at=_NOW,
    )


def _progress(course_id, lesson_id, percent) -> LessonProgressRow:
    return LessonProgressRow(
        id=uuid.uuid4(),
        user_id=_USER,
        course_id=course_id,
        lesson_id=lesson_id,
        percent=percent,
        started_at=_NOW,
    )


# Course / lesson ids reused across the seed + assertions.
_LINALG_COURSE = uuid.uuid4()
_DIFFEQ_COURSE = uuid.uuid4()
_PROG_COURSE = uuid.uuid4()
_LIN_L1, _LIN_L2 = uuid.uuid4(), uuid.uuid4()
_DIF_L1, _DIF_L2 = uuid.uuid4(), uuid.uuid4()
_PROG_L1 = uuid.uuid4()
_LIN_QUIZ = uuid.uuid4()


@pytest.fixture
def client(app: FastAPI, _prepared_schema: None) -> TestClient:
    app.dependency_overrides[require_principal] = lambda: _learner()
    return TestClient(app)


@pytest.fixture(autouse=True)
def _seed(_prepared_schema: None) -> None:
    import asyncio

    async def run() -> None:
        factory = get_session_factory()
        async with factory() as s:
            s.add_all(
                [
                    CategoryRow(id=_MATH, slug="eng-math", name="Engineering Math", created_at=_NOW),
                    CategoryRow(id=_LINALG, slug="linalg", name="Linear Algebra", parent_id=_MATH, created_at=_NOW),
                    CategoryRow(id=_DIFFEQ, slug="diffeq", name="Differential Equations", parent_id=_MATH, created_at=_NOW),
                    CategoryRow(id=_PROG, slug="programming", name="Programming", created_at=_NOW),
                ]
            )
            s.add_all(
                [
                    _course(_LINALG_COURSE, "linalg-101", _LINALG),
                    _course(_DIFFEQ_COURSE, "diffeq-101", _DIFFEQ),
                    _course(_PROG_COURSE, "py-101", _PROG),
                    _course(uuid.uuid4(), "draft-x", _LINALG, status="draft"),
                    _lesson(_LIN_L1, _LINALG_COURSE),
                    _lesson(_LIN_L2, _LINALG_COURSE),
                    _lesson(_DIF_L1, _DIFFEQ_COURSE),
                    _lesson(_DIF_L2, _DIFFEQ_COURSE),
                    _lesson(_PROG_L1, _PROG_COURSE),
                ]
            )
            s.add_all(
                [
                    # Linear Algebra: both lessons complete -> completion 1.0
                    _progress(_LINALG_COURSE, _LIN_L1, 100),
                    _progress(_LINALG_COURSE, _LIN_L2, 100),
                    # Differential Eq: 20 + 30 -> completion 0.25
                    _progress(_DIFFEQ_COURSE, _DIF_L1, 20),
                    _progress(_DIFFEQ_COURSE, _DIF_L2, 30),
                    # Programming: no progress -> 0
                ]
            )
            # Linear Algebra quiz, best attempt 80.
            q_id = uuid.uuid4()
            opt = uuid.uuid4()
            s.add_all(
                [
                    QuizRow(id=_LIN_QUIZ, lesson_id=_LIN_L1, passing_score=70, created_at=_NOW),
                    QuizQuestionRow(id=q_id, quiz_id=_LIN_QUIZ, prompt="q", explanation="", sort_order=0),
                    QuizOptionRow(id=opt, question_id=q_id, text="a", is_correct=True),
                    QuizAttemptRow(
                        id=uuid.uuid4(), user_id=_USER, quiz_id=_LIN_QUIZ, lesson_id=_LIN_L1,
                        score=60, passed=False, attempt_number=1, answers={}, submitted_at=_NOW,
                    ),
                    QuizAttemptRow(
                        id=uuid.uuid4(), user_id=_USER, quiz_id=_LIN_QUIZ, lesson_id=_LIN_L1,
                        score=80, passed=True, attempt_number=2, answers={}, submitted_at=_NOW,
                    ),
                ]
            )
            await s.commit()

    asyncio.run(run())


def test_skill_map_mastery_and_domains(client: TestClient) -> None:
    resp = client.get("/api/v1/skills/me")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    by_id = {s["id"]: s for s in body["skills"]}

    # Linear Algebra: completion 1.0 blended with best quiz 80 ->
    # 0.6*1.0 + 0.4*0.8 = 0.92 -> 92.
    assert by_id["linalg"]["mastery"] == 92
    assert by_id["linalg"]["domain"] == "Engineering Math"
    assert by_id["linalg"]["weak"] is False
    assert by_id["linalg"]["courseCount"] == 1  # draft excluded

    # Differential Equations: completion 0.25, no quiz -> 25, weak.
    assert by_id["diffeq"]["mastery"] == 25
    assert by_id["diffeq"]["domain"] == "Engineering Math"
    assert by_id["diffeq"]["weak"] is True

    # Programming (top-level): domain is itself; 0% -> weak.
    assert by_id["programming"]["domain"] == "Programming"
    assert by_id["programming"]["mastery"] == 0
    assert by_id["programming"]["weak"] is True


def test_weak_areas_and_suggestions(client: TestClient) -> None:
    body = client.get("/api/v1/skills/me").json()
    assert set(body["weakAreas"]) == {"diffeq", "programming"}
    # Weakest first: programming (0) before diffeq (25).
    assert body["suggestions"] == ["py-101", "diffeq-101"]


def test_skills_grouped_by_domain(client: TestClient) -> None:
    body = client.get("/api/v1/skills/me").json()
    # Engineering Math (Differential Equations, Linear Algebra) then Programming.
    assert [s["id"] for s in body["skills"]] == ["diffeq", "linalg", "programming"]
