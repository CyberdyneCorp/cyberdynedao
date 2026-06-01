"""Quiz endpoints — learner player + admin authoring.

Player routes are gated on a user principal and never expose correct
flags or explanations until an attempt is graded. Admin routes require
the ``editor`` scope and operate on the full quiz tree.
"""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from cyberdyne_backend.adapters.inbound.api.quizzes.schemas import (
    AttemptResultResponse,
    AttemptSummaryResponse,
    EditorOptionResponse,
    EditorQuestionResponse,
    EditorQuizResponse,
    PlayerOptionResponse,
    PlayerQuestionResponse,
    PlayerQuizResponse,
    QuestionResultResponse,
    SubmitAttemptRequest,
    UpsertQuizRequest,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import (
    require_editor,
    require_principal,
)
from cyberdyne_backend.application.quizzes import (
    DeleteQuiz,
    GetQuiz,
    ListMyAttempts,
    OptionInput,
    QuestionInput,
    SubmitQuizAttempt,
    SubmittedAttempt,
    UpsertQuiz,
    UpsertQuizCommand,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.quizzes import (
    InvalidAttemptError,
    InvalidQuizError,
    Quiz,
    QuizAttempt,
    QuizNotFoundError,
)

player_router = APIRouter(prefix="/api/v1/lessons", tags=["quizzes"])
admin_router = APIRouter(prefix="/api/v1/admin/lessons", tags=["quizzes-admin"])


# Dependency stubs — overridden in main.py.
async def get_quiz_uc() -> GetQuiz:  # pragma: no cover - override target
    raise NotImplementedError


async def get_upsert_quiz_uc() -> UpsertQuiz:  # pragma: no cover - override target
    raise NotImplementedError


async def get_delete_quiz_uc() -> DeleteQuiz:  # pragma: no cover - override target
    raise NotImplementedError


async def get_submit_attempt_uc() -> SubmitQuizAttempt:  # pragma: no cover - override target
    raise NotImplementedError


async def get_list_attempts_uc() -> ListMyAttempts:  # pragma: no cover - override target
    raise NotImplementedError


# ── Response builders ────────────────────────────────────────────────


def _player_response(quiz: Quiz) -> PlayerQuizResponse:
    return PlayerQuizResponse(
        lesson_id=quiz.lesson_id,
        passing_score=quiz.passing_score,
        questions=[
            PlayerQuestionResponse(
                id=q.id,
                prompt=q.prompt,
                options=[PlayerOptionResponse(id=o.id, text=o.text) for o in q.options],
            )
            for q in quiz.questions
        ],
    )


def _editor_response(quiz: Quiz) -> EditorQuizResponse:
    return EditorQuizResponse(
        id=quiz.id,
        lesson_id=quiz.lesson_id,
        passing_score=quiz.passing_score,
        questions=[
            EditorQuestionResponse(
                id=q.id,
                prompt=q.prompt,
                explanation=q.explanation,
                options=[
                    EditorOptionResponse(id=o.id, text=o.text, is_correct=o.is_correct)
                    for o in q.options
                ],
            )
            for q in quiz.questions
        ],
    )


def _attempt_result(result: SubmittedAttempt) -> AttemptResultResponse:
    return AttemptResultResponse(
        attempt_id=result.attempt.id,
        score=result.graded.score,
        passed=result.graded.passed,
        attempt_number=result.attempt.attempt_number,
        submitted_at=result.attempt.submitted_at,
        results=[
            QuestionResultResponse(
                question_id=r.question_id,
                selected_option_id=r.selected_option_id,
                correct_option_id=r.correct_option_id,
                is_correct=r.is_correct,
                explanation=r.explanation,
            )
            for r in result.graded.results
        ],
    )


def _attempt_summary(attempt: QuizAttempt) -> AttemptSummaryResponse:
    return AttemptSummaryResponse(
        id=attempt.id,
        score=attempt.score,
        passed=attempt.passed,
        attempt_number=attempt.attempt_number,
        submitted_at=attempt.submitted_at,
    )


def _require_user(principal: UserPrincipal) -> UserPrincipal:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    return principal


# ── Player ────────────────────────────────────────────────────────────


@player_router.get(
    "/{lesson_id}/quiz",
    response_model=PlayerQuizResponse,
    response_model_by_alias=True,
)
async def get_quiz_for_player(
    lesson_id: UUID,
    use_case: Annotated[GetQuiz, Depends(get_quiz_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> PlayerQuizResponse:
    try:
        quiz = await use_case.execute(lesson_id)
    except QuizNotFoundError as exc:
        raise HTTPException(status_code=404, detail="quiz not found") from exc
    return _player_response(quiz)


@player_router.post(
    "/{lesson_id}/quiz/attempts",
    response_model=AttemptResultResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def submit_attempt(
    lesson_id: UUID,
    body: SubmitAttemptRequest,
    use_case: Annotated[SubmitQuizAttempt, Depends(get_submit_attempt_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> AttemptResultResponse:
    user = _require_user(principal)
    try:
        result = await use_case.execute(
            user_id=user.user_id,
            lesson_id=lesson_id,
            answers=body.answers,
        )
    except QuizNotFoundError as exc:
        raise HTTPException(status_code=404, detail="quiz not found") from exc
    except InvalidAttemptError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _attempt_result(result)


@player_router.get(
    "/{lesson_id}/quiz/attempts",
    response_model=list[AttemptSummaryResponse],
    response_model_by_alias=True,
)
async def list_my_attempts(
    lesson_id: UUID,
    use_case: Annotated[ListMyAttempts, Depends(get_list_attempts_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> list[AttemptSummaryResponse]:
    user = _require_user(principal)
    try:
        attempts = await use_case.execute(user_id=user.user_id, lesson_id=lesson_id)
    except QuizNotFoundError as exc:
        raise HTTPException(status_code=404, detail="quiz not found") from exc
    return [_attempt_summary(a) for a in attempts]


# ── Admin authoring ──────────────────────────────────────────────────


@admin_router.put(
    "/{lesson_id}/quiz",
    response_model=EditorQuizResponse,
    response_model_by_alias=True,
)
async def upsert_quiz(
    lesson_id: UUID,
    body: UpsertQuizRequest,
    use_case: Annotated[UpsertQuiz, Depends(get_upsert_quiz_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> EditorQuizResponse:
    try:
        quiz = await use_case.execute(
            lesson_id,
            UpsertQuizCommand(
                passing_score=body.passing_score,
                questions=[
                    QuestionInput(
                        prompt=q.prompt,
                        explanation=q.explanation,
                        options=[
                            OptionInput(text=o.text, is_correct=o.is_correct) for o in q.options
                        ],
                    )
                    for q in body.questions
                ],
            ),
        )
    except InvalidQuizError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _editor_response(quiz)


@admin_router.get(
    "/{lesson_id}/quiz",
    response_model=EditorQuizResponse,
    response_model_by_alias=True,
)
async def get_quiz_for_editor(
    lesson_id: UUID,
    use_case: Annotated[GetQuiz, Depends(get_quiz_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> EditorQuizResponse:
    try:
        quiz = await use_case.execute(lesson_id)
    except QuizNotFoundError as exc:
        raise HTTPException(status_code=404, detail="quiz not found") from exc
    return _editor_response(quiz)


@admin_router.delete("/{lesson_id}/quiz", status_code=204)
async def delete_quiz(
    lesson_id: UUID,
    use_case: Annotated[DeleteQuiz, Depends(get_delete_quiz_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> None:
    try:
        await use_case.execute(lesson_id)
    except QuizNotFoundError as exc:
        raise HTTPException(status_code=404, detail="quiz not found") from exc


__all__ = ["admin_router", "player_router"]
