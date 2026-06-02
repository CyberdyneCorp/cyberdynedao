"""End-to-end API tests for the quiz endpoints.

Drives router → use case → SQLAlchemy → in-memory sqlite. A course +
quiz-type lesson is created via the courses admin API so the quiz hangs
off a real ``lessons`` row, then the quiz is authored, played, and
graded. Verifies the player view never leaks correct flags/explanations.
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
    user_id=uuid.UUID("11111111-1111-1111-1111-111111111111"),
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
    # Editor for admin routes; a plain learner for player routes.
    app.dependency_overrides[require_editor] = _editor
    app.dependency_overrides[require_principal] = lambda: _LEARNER
    return TestClient(app)


def _make_quiz_lesson(client: TestClient) -> str:
    """Create a course + quiz-type lesson, return the lesson id."""
    assert (
        client.post(
            "/api/v1/admin/courses",
            json={"title": "Quiz Course", "description": "d", "level": "Beginner"},
        ).status_code
        == 201
    )
    lesson = client.post(
        "/api/v1/admin/courses/quiz-course/lessons",
        json={"title": "Assessment", "lessonType": "quiz"},
    )
    assert lesson.status_code == 201, lesson.text
    return lesson.json()["id"]


_QUIZ_BODY = {
    "passingScore": 70,
    "questions": [
        {
            "prompt": "2 + 2 = ?",
            "explanation": "Addition.",
            "options": [
                {"text": "3", "isCorrect": False},
                {"text": "4", "isCorrect": True},
            ],
        },
        {
            "prompt": "Sky colour?",
            "explanation": "Rayleigh scattering.",
            "options": [
                {"text": "Blue", "isCorrect": True},
                {"text": "Green", "isCorrect": False},
            ],
        },
    ],
}


@pytest.mark.usefixtures("_prepared_schema")
def test_quiz_lifecycle_and_no_answer_leak(authed_client: TestClient) -> None:
    lesson_id = _make_quiz_lesson(authed_client)

    # Author the quiz.
    put = authed_client.put(f"/api/v1/admin/lessons/{lesson_id}/quiz", json=_QUIZ_BODY)
    assert put.status_code == 200, put.text

    # Player view: no isCorrect, no explanation anywhere.
    player = authed_client.get(f"/api/v1/lessons/{lesson_id}/quiz")
    assert player.status_code == 200
    pbody = player.json()
    assert pbody["passingScore"] == 70
    assert len(pbody["questions"]) == 2
    for q in pbody["questions"]:
        assert "explanation" not in q
        for opt in q["options"]:
            assert set(opt.keys()) == {"id", "text"}  # id + text only

    # Build correct answers from the editor view (which DOES carry flags).
    editor_view = authed_client.get(f"/api/v1/admin/lessons/{lesson_id}/quiz").json()
    answers = {
        q["id"]: next(o["id"] for o in q["options"] if o["isCorrect"])
        for q in editor_view["questions"]
    }

    # Submit a perfect attempt → passes, feedback includes explanations.
    attempt = authed_client.post(
        f"/api/v1/lessons/{lesson_id}/quiz/attempts", json={"answers": answers}
    )
    assert attempt.status_code == 201, attempt.text
    abody = attempt.json()
    assert abody["score"] == 100
    assert abody["passed"] is True
    assert abody["attemptNumber"] == 1
    assert abody["results"][0]["explanation"] == "Addition."

    # A second (empty) attempt fails and increments the attempt number.
    retry = authed_client.post(f"/api/v1/lessons/{lesson_id}/quiz/attempts", json={"answers": {}})
    assert retry.status_code == 201
    assert retry.json()["passed"] is False
    assert retry.json()["attemptNumber"] == 2

    # Attempt history reflects both.
    history = authed_client.get(f"/api/v1/lessons/{lesson_id}/quiz/attempts").json()
    assert [a["attemptNumber"] for a in history] == [1, 2]


@pytest.mark.usefixtures("_prepared_schema")
def test_ai_contextual_feedback(authed_client: TestClient) -> None:
    lesson_id = _make_quiz_lesson(authed_client)
    authed_client.put(f"/api/v1/admin/lessons/{lesson_id}/quiz", json=_QUIZ_BODY)

    editor_view = authed_client.get(f"/api/v1/admin/lessons/{lesson_id}/quiz").json()
    q0, q1 = editor_view["questions"]
    wrong = next(o["id"] for o in q0["options"] if not o["isCorrect"])
    right = next(o["id"] for o in q1["options"] if o["isCorrect"])
    answers = {q0["id"]: wrong, q1["id"]: right}

    resp = authed_client.post(
        f"/api/v1/lessons/{lesson_id}/quiz/feedback", json={"answers": answers}
    )
    assert resp.status_code == 200, resp.text
    by_q = {f["questionId"]: f for f in resp.json()}

    wrong_fb = by_q[q0["id"]]
    assert wrong_fb["isCorrect"] is False
    assert wrong_fb["aiExplanation"]  # offline canned reply, non-empty
    assert wrong_fb["staticExplanation"] == "Addition."

    right_fb = by_q[q1["id"]]
    assert right_fb["isCorrect"] is True
    assert right_fb["aiExplanation"] is None

    # Feedback is read-only: it must not record an attempt.
    assert authed_client.get(f"/api/v1/lessons/{lesson_id}/quiz/attempts").json() == []


@pytest.mark.usefixtures("_prepared_schema")
def test_feedback_missing_quiz_is_404(authed_client: TestClient) -> None:
    resp = authed_client.post(f"/api/v1/lessons/{uuid.uuid4()}/quiz/feedback", json={"answers": {}})
    assert resp.status_code == 404


@pytest.mark.usefixtures("_prepared_schema")
def test_invalid_quiz_is_422(authed_client: TestClient) -> None:
    lesson_id = _make_quiz_lesson(authed_client)
    # Two correct options on one question — schema allows it, domain rejects.
    bad = {
        "questions": [
            {
                "prompt": "q",
                "explanation": "",
                "options": [
                    {"text": "a", "isCorrect": True},
                    {"text": "b", "isCorrect": True},
                ],
            }
        ]
    }
    resp = authed_client.put(f"/api/v1/admin/lessons/{lesson_id}/quiz", json=bad)
    assert resp.status_code == 422


@pytest.mark.usefixtures("_prepared_schema")
def test_missing_quiz_is_404(authed_client: TestClient) -> None:
    assert authed_client.get(f"/api/v1/lessons/{uuid.uuid4()}/quiz").status_code == 404


@pytest.mark.usefixtures("_prepared_schema")
def test_delete_quiz(authed_client: TestClient) -> None:
    lesson_id = _make_quiz_lesson(authed_client)
    authed_client.put(f"/api/v1/admin/lessons/{lesson_id}/quiz", json=_QUIZ_BODY)
    assert authed_client.delete(f"/api/v1/admin/lessons/{lesson_id}/quiz").status_code == 204
    assert authed_client.get(f"/api/v1/lessons/{lesson_id}/quiz").status_code == 404


def test_player_requires_auth(client: TestClient) -> None:
    resp = client.get(f"/api/v1/lessons/{uuid.uuid4()}/quiz")
    assert resp.status_code in (401, 403)
