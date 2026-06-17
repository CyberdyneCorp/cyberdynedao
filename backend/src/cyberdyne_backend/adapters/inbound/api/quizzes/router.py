"""Quiz endpoints — learner player + admin authoring.

Player routes are gated on a user principal and never expose correct
flags or explanations until an attempt is graded. Admin routes require
the ``editor`` scope and operate on the full quiz tree.
"""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from cyberdyne_backend.adapters.inbound.api.locale import resolve_locale
from cyberdyne_backend.adapters.inbound.api.quizzes.schemas import (
    AnswerFeedbackResponse,
    AttemptResultResponse,
    AttemptSummaryResponse,
    EditorOptionResponse,
    EditorQuestionResponse,
    EditorQuizResponse,
    LastAttemptResponse,
    PlayerOptionResponse,
    PlayerQuestionResponse,
    PlayerQuizResponse,
    QuestionResultResponse,
    QuizCatalogResponse,
    QuizSummaryResponse,
    SubmitAttemptRequest,
    UpsertQuizRequest,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import (
    require_editor,
    require_principal,
)
from cyberdyne_backend.application.quizzes import (
    DeleteQuiz,
    ExplainQuizAnswers,
    GetQuiz,
    ListMyAttempts,
    ListQuizCatalog,
    OptionInput,
    QuestionInput,
    SubmitQuizAttempt,
    SubmittedAttempt,
    UpsertQuiz,
    UpsertQuizCommand,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.quizzes import (
    DEFAULT_CATALOG_LIMIT,
    MAX_CATALOG_LIMIT,
    InvalidAttemptError,
    InvalidQuizError,
    Quiz,
    QuizAttempt,
    QuizCatalogPage,
    QuizNotFoundError,
)

player_router = APIRouter(prefix="/api/v1/lessons", tags=["quizzes"])
admin_router = APIRouter(prefix="/api/v1/admin/lessons", tags=["quizzes-admin"])
catalog_router = APIRouter(prefix="/api/v1/quizzes", tags=["quizzes"])


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


async def get_explain_answers_uc() -> ExplainQuizAnswers:  # pragma: no cover - override target
    raise NotImplementedError


async def get_list_catalog_uc() -> ListQuizCatalog:  # pragma: no cover - override target
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


def _catalog_response(page: QuizCatalogPage) -> QuizCatalogResponse:
    return QuizCatalogResponse(
        items=[
            QuizSummaryResponse(
                quiz_id=s.quiz_id,
                lesson_id=s.lesson_id,
                lesson_title=s.lesson_title,
                course_slug=s.course_slug,
                course_title=s.course_title,
                category_slug=s.category_slug,
                passing_score=s.passing_score,
                question_count=s.question_count,
                last_attempt=(
                    LastAttemptResponse(
                        score=s.last_attempt.score,
                        passed=s.last_attempt.passed,
                        attempt_number=s.last_attempt.attempt_number,
                        submitted_at=s.last_attempt.submitted_at,
                    )
                    if s.last_attempt is not None
                    else None
                ),
            )
            for s in page.items
        ],
        next_cursor=page.next_cursor,
    )


# ── Player ────────────────────────────────────────────────────────────


@player_router.get(
    "/{lesson_id}/quiz",
    response_model=PlayerQuizResponse,
    response_model_by_alias=True,
)
async def get_quiz_for_player(
    lesson_id: UUID,
    use_case: Annotated[GetQuiz, Depends(get_quiz_uc)],
    locale: Annotated[str, Depends(resolve_locale)],
    _principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> PlayerQuizResponse:
    try:
        quiz = await use_case.execute(lesson_id, locale=locale)
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
    locale: Annotated[str, Depends(resolve_locale)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> AttemptResultResponse:
    user = _require_user(principal)
    try:
        result = await use_case.execute(
            user_id=user.user_id,
            lesson_id=lesson_id,
            answers=body.answers,
            locale=locale,
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


@player_router.post(
    "/{lesson_id}/quiz/feedback",
    response_model=list[AnswerFeedbackResponse],
    response_model_by_alias=True,
)
async def explain_quiz_answers(
    lesson_id: UUID,
    body: SubmitAttemptRequest,
    use_case: Annotated[ExplainQuizAnswers, Depends(get_explain_answers_uc)],
    locale: Annotated[str, Depends(resolve_locale)],
    _principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> list[AnswerFeedbackResponse]:
    """AI contextual feedback: grade the submitted answers and return a
    personalized 'why it's wrong' for each incorrect question. Read-only
    (records no attempt) so a learner can ask for help freely."""
    try:
        feedback = await use_case.execute(lesson_id=lesson_id, answers=body.answers, locale=locale)
    except QuizNotFoundError as exc:
        raise HTTPException(status_code=404, detail="quiz not found") from exc
    return [
        AnswerFeedbackResponse(
            question_id=f.question_id,
            prompt=f.prompt,
            is_correct=f.is_correct,
            selected_option_id=f.selected_option_id,
            correct_option_id=f.correct_option_id,
            static_explanation=f.static_explanation,
            ai_explanation=f.ai_explanation,
        )
        for f in feedback
    ]


# ── Browse / practice catalogue ──────────────────────────────────────


@catalog_router.get(
    "",
    response_model=QuizCatalogResponse,
    response_model_by_alias=True,
)
async def browse_quizzes(
    use_case: Annotated[ListQuizCatalog, Depends(get_list_catalog_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
    course_slug: Annotated[str | None, Query(alias="courseSlug")] = None,
    domain: Annotated[str | None, Query()] = None,
    cursor: Annotated[str | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=MAX_CATALOG_LIMIT)] = DEFAULT_CATALOG_LIMIT,
) -> QuizCatalogResponse:
    """List quizzes from published courses so a learner can discover and
    start them without first opening a specific lesson. ``domain`` filters
    by the course's category slug. Reuses the existing per-lesson quiz +
    attempt endpoints to actually play a quiz (via the returned
    ``lessonId``)."""
    user = _require_user(principal)
    page = await use_case.execute(
        user_id=user.user_id,
        course_slug=course_slug,
        category_slug=domain,
        cursor=cursor,
        limit=limit,
    )
    return _catalog_response(page)


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


__all__ = ["admin_router", "catalog_router", "player_router"]
