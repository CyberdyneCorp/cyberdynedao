"""End-to-end API tests for per-lesson progress / per-course completion.

Drives router -> use case -> SQLAlchemy -> in-memory sqlite. An editor
authors + publishes a course with two lessons; a learner then records
progress and reads their course standing, including auto-completion when
every lesson hits 100%.
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

_LEARNER = UserPrincipal(
    user_id=uuid.UUID("33333333-3333-3333-3333-333333333333"),
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
def authed_client(app: FastAPI) -> TestClient:
    app.dependency_overrides[require_editor] = _editor
    app.dependency_overrides[require_principal] = lambda: _LEARNER
    return TestClient(app)


def _make_published_course(client: TestClient) -> list[str]:
    """Create a 2-lesson course, publish it, return the lesson ids."""
    assert (
        client.post(
            "/api/v1/admin/courses",
            json={"title": "Progress Course", "description": "d", "level": "Beginner"},
        ).status_code
        == 201
    )
    ids = []
    for i in range(2):
        lesson = client.post(
            "/api/v1/admin/courses/progress-course/lessons",
            json={"title": f"Lesson {i}", "lessonType": "text", "textBody": "body"},
        )
        assert lesson.status_code == 201, lesson.text
        ids.append(lesson.json()["id"])
    assert client.post("/api/v1/admin/courses/progress-course/publish").status_code == 200
    return ids


@pytest.mark.usefixtures("_prepared_schema")
def test_progress_lifecycle_and_auto_completion(authed_client: TestClient) -> None:
    lesson_ids = _make_published_course(authed_client)

    # Fresh learner: 0%, nothing completed.
    start = authed_client.get("/api/v1/courses/progress-course/progress")
    assert start.status_code == 200, start.text
    assert start.json()["percent"] == 0
    assert start.json()["totalLessons"] == 2
    assert all(not lesson["completed"] for lesson in start.json()["lessons"])

    # Complete the first lesson -> 50%, course not complete.
    half = authed_client.put(
        f"/api/v1/courses/progress-course/lessons/{lesson_ids[0]}/progress",
        json={"percent": 100},
    )
    assert half.status_code == 200, half.text
    assert half.json()["percent"] == 50
    assert half.json()["completedLessons"] == 1
    assert half.json()["completed"] is False

    # Complete the second -> 100%, course auto-completes.
    full = authed_client.put(
        f"/api/v1/courses/progress-course/lessons/{lesson_ids[1]}/progress",
        json={"percent": 100},
    )
    assert full.status_code == 200
    assert full.json()["percent"] == 100
    assert full.json()["completed"] is True

    # Read-back reflects completion.
    assert authed_client.get("/api/v1/courses/progress-course/progress").json()["completed"] is True


@pytest.mark.usefixtures("_prepared_schema")
def test_partial_percent_does_not_complete(authed_client: TestClient) -> None:
    lesson_ids = _make_published_course(authed_client)
    resp = authed_client.put(
        f"/api/v1/courses/progress-course/lessons/{lesson_ids[0]}/progress",
        json={"percent": 60},
    )
    assert resp.status_code == 200
    # 60% on a lesson is "in progress", not completed -> 0 completed lessons.
    assert resp.json()["completedLessons"] == 0
    assert resp.json()["percent"] == 0


@pytest.mark.usefixtures("_prepared_schema")
def test_percent_out_of_range_is_422(authed_client: TestClient) -> None:
    lesson_ids = _make_published_course(authed_client)
    resp = authed_client.put(
        f"/api/v1/courses/progress-course/lessons/{lesson_ids[0]}/progress",
        json={"percent": 150},
    )
    assert resp.status_code == 422


@pytest.mark.usefixtures("_prepared_schema")
def test_lesson_not_in_course_is_404(authed_client: TestClient) -> None:
    _make_published_course(authed_client)
    resp = authed_client.put(
        f"/api/v1/courses/progress-course/lessons/{uuid.uuid4()}/progress",
        json={"percent": 50},
    )
    assert resp.status_code == 404


@pytest.mark.usefixtures("_prepared_schema")
def test_passing_quiz_auto_completes_its_lesson(authed_client: TestClient) -> None:
    # Course with a single quiz-type lesson, published.
    assert (
        authed_client.post(
            "/api/v1/admin/courses",
            json={"title": "Quiz Progress", "description": "d", "level": "Beginner"},
        ).status_code
        == 201
    )
    lesson = authed_client.post(
        "/api/v1/admin/courses/quiz-progress/lessons",
        json={"title": "Assessment", "lessonType": "quiz"},
    )
    lesson_id = lesson.json()["id"]
    assert authed_client.post("/api/v1/admin/courses/quiz-progress/publish").status_code == 200

    # Author the quiz.
    quiz_body = {
        "passingScore": 70,
        "questions": [
            {
                "prompt": "2 + 2 = ?",
                "explanation": "Addition.",
                "options": [
                    {"text": "3", "isCorrect": False},
                    {"text": "4", "isCorrect": True},
                ],
            }
        ],
    }
    assert (
        authed_client.put(f"/api/v1/admin/lessons/{lesson_id}/quiz", json=quiz_body).status_code
        == 200
    )

    # Before any attempt: the quiz lesson is not complete.
    assert authed_client.get("/api/v1/courses/quiz-progress/progress").json()["completed"] is False

    # Submit a passing attempt -> the lesson auto-completes -> course completes.
    editor_view = authed_client.get(f"/api/v1/admin/lessons/{lesson_id}/quiz").json()
    answers = {
        q["id"]: next(o["id"] for o in q["options"] if o["isCorrect"])
        for q in editor_view["questions"]
    }
    attempt = authed_client.post(
        f"/api/v1/lessons/{lesson_id}/quiz/attempts", json={"answers": answers}
    )
    assert attempt.status_code == 201
    assert attempt.json()["passed"] is True

    progress = authed_client.get("/api/v1/courses/quiz-progress/progress").json()
    assert progress["completed"] is True
    assert progress["lessons"][0]["completed"] is True


@pytest.mark.usefixtures("_prepared_schema")
def test_failing_quiz_does_not_complete_lesson(authed_client: TestClient) -> None:
    assert (
        authed_client.post(
            "/api/v1/admin/courses",
            json={"title": "Quiz Fail", "description": "d", "level": "Beginner"},
        ).status_code
        == 201
    )
    lesson = authed_client.post(
        "/api/v1/admin/courses/quiz-fail/lessons",
        json={"title": "Assessment", "lessonType": "quiz"},
    )
    lesson_id = lesson.json()["id"]
    authed_client.post("/api/v1/admin/courses/quiz-fail/publish")
    authed_client.put(
        f"/api/v1/admin/lessons/{lesson_id}/quiz",
        json={
            "passingScore": 70,
            "questions": [
                {
                    "prompt": "2 + 2 = ?",
                    "explanation": "Addition.",
                    "options": [
                        {"text": "3", "isCorrect": False},
                        {"text": "4", "isCorrect": True},
                    ],
                }
            ],
        },
    )
    # Empty answers -> fail -> lesson stays incomplete.
    fail = authed_client.post(f"/api/v1/lessons/{lesson_id}/quiz/attempts", json={"answers": {}})
    assert fail.json()["passed"] is False
    assert authed_client.get("/api/v1/courses/quiz-fail/progress").json()["completed"] is False


@pytest.mark.usefixtures("_prepared_schema")
def test_dashboard_reflects_course_completion(authed_client: TestClient) -> None:
    lesson_ids = _make_published_course(authed_client)  # 2-lesson "progress-course"

    # One lesson done -> the course is in progress on the dashboard.
    authed_client.put(
        f"/api/v1/courses/progress-course/lessons/{lesson_ids[0]}/progress",
        json={"percent": 100},
    )
    mid = authed_client.get("/api/v1/analytics/me").json()
    assert mid["inProgressCourses"] == 1
    assert mid["completedCourses"] == 0

    # Both lessons done -> the course counts as completed.
    authed_client.put(
        f"/api/v1/courses/progress-course/lessons/{lesson_ids[1]}/progress",
        json={"percent": 100},
    )
    done = authed_client.get("/api/v1/analytics/me").json()
    assert done["completedCourses"] == 1
    assert done["inProgressCourses"] == 0


@pytest.mark.usefixtures("_prepared_schema")
def test_unknown_course_is_404(authed_client: TestClient) -> None:
    assert authed_client.get("/api/v1/courses/ghost/progress").status_code == 404


def test_progress_requires_auth(client: TestClient) -> None:
    assert client.get("/api/v1/courses/whatever/progress").status_code in (401, 403)
