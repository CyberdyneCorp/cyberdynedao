"""Learner-feedback endpoints (issue #233).

A general feedback channel — problem reports and feature requests — open to
every signed-in learner (free and Pro; not gated). Admins read the queue for
triage. Course/topic *requests* are a separate concern (the demand registry,
issue #232); this channel is problems + features only.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from cyberdyne_backend.adapters.inbound.api.feedback.schemas import (
    FeedbackKindLiteral,
    FeedbackResponse,
    FeedbackStatusLiteral,
    SubmitFeedbackRequest,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import (
    require_editor,
    require_principal,
)
from cyberdyne_backend.application.feedback import ListFeedback, SubmitFeedback
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.feedback import (
    Feedback,
    parse_feedback_kind,
    parse_feedback_status,
)

public_router = APIRouter(prefix="/api/v1", tags=["feedback"])
admin_router = APIRouter(prefix="/api/v1/admin", tags=["admin-feedback"])


# Dependency stubs — overridden in main.py.
async def get_submit_feedback_uc() -> SubmitFeedback:  # pragma: no cover - override target
    raise NotImplementedError


async def get_list_feedback_uc() -> ListFeedback:  # pragma: no cover - override target
    raise NotImplementedError


def _response(f: Feedback) -> FeedbackResponse:
    return FeedbackResponse(
        id=f.id,
        kind=f.kind.value,
        status=f.status.value,
        message=f.message,
        course_id=f.course_id,
        lesson_id=f.lesson_id,
        app_version=f.app_version,
        platform=f.platform,
        created_at=f.created_at,
        updated_at=f.updated_at,
    )


def _require_user(principal: UserPrincipal) -> UserPrincipal:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    return principal


@public_router.post(
    "/feedback",
    response_model=FeedbackResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def submit_feedback(
    body: SubmitFeedbackRequest,
    use_case: Annotated[SubmitFeedback, Depends(get_submit_feedback_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> FeedbackResponse:
    user = _require_user(principal)
    feedback = await use_case.execute(
        user_id=user.user_id,
        kind=parse_feedback_kind(body.kind),
        message=body.message,
        course_id=body.course_id,
        lesson_id=body.lesson_id,
        app_version=body.app_version,
        platform=body.platform,
    )
    return _response(feedback)


@admin_router.get(
    "/feedback",
    response_model=list[FeedbackResponse],
    response_model_by_alias=True,
)
async def list_feedback(
    use_case: Annotated[ListFeedback, Depends(get_list_feedback_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
    kind: Annotated[FeedbackKindLiteral | None, Query()] = None,
    status: Annotated[FeedbackStatusLiteral | None, Query()] = None,
) -> list[FeedbackResponse]:
    items = await use_case.execute(
        kind=parse_feedback_kind(kind) if kind is not None else None,
        status=parse_feedback_status(status) if status is not None else None,
    )
    return [_response(f) for f in items]
