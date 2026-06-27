"""Global Agent Chat endpoints (issue #234).

A top-level assistant for signed-in learners, reachable with NO course open:

  - ``POST /api/v1/agent/sessions`` — create a user-scoped chat session
    (reuses the chat ``StartChatSession`` / ``ChatRepository``).
  - ``POST /api/v1/agent/sessions/{id}/messages`` — run one answer turn.
    Guarded by ``require_principal`` (this agent needs a learner) and the
    TUTOR_MESSAGES quota (text turns count toward the AI-message allowance).
    Returns the assistant message plus ``courseRefs`` and an optional
    ``unmatchedTopic``.
  - ``GET /api/v1/agent/sessions/{id}`` — history (reuses ``GetChatHistory``).
"""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from cyberdyne_backend.adapters.inbound.api.agent_chat.schemas import (
    AgentMessageRequest,
    AgentTurnResponse,
    ChatHistoryResponse,
    CourseRefView,
    NotebookActionView,
    StartSessionResponse,
    UnmatchedTopicView,
)
from cyberdyne_backend.adapters.inbound.api.ai_chat.router import _message_response
from cyberdyne_backend.adapters.inbound.api.quota.dependencies import QuotaGuard
from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.application.agent_chat import AnswerAgentTurn, AnswerTurnResult
from cyberdyne_backend.application.ai_chat import (
    MAX_CHAT_HISTORY_LIMIT,
    GetChatHistory,
    StartChatSession,
)
from cyberdyne_backend.domain.ai_chat import ChatProviderError, ChatSessionNotFoundError
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.quota import QuotaMeter

router = APIRouter(prefix="/api/v1/agent", tags=["agent"])

# Text turns count toward the same AI-message allowance as the tutor (#230).
_agent_quota = QuotaGuard(QuotaMeter.TUTOR_MESSAGES)


async def get_agent_start_session_uc() -> StartChatSession:  # pragma: no cover - override
    raise NotImplementedError


async def get_agent_turn_uc() -> AnswerAgentTurn:  # pragma: no cover - override
    raise NotImplementedError


async def get_agent_history_uc() -> GetChatHistory:  # pragma: no cover - override
    raise NotImplementedError


def _require_user(principal: object) -> UserPrincipal:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    return principal


def _turn_response(result: AnswerTurnResult) -> AgentTurnResponse:
    return AgentTurnResponse(
        message=_message_response(result.message),
        course_refs=[
            CourseRefView(
                course_slug=ref.course_slug,
                lesson_id=ref.lesson_id,
                score=ref.score,
                match_reason=ref.match_reason,
            )
            for ref in result.course_refs
        ],
        unmatched_topic=(
            UnmatchedTopicView(
                topic=result.unmatched_topic.topic,
                subject=result.unmatched_topic.subject,
            )
            if result.unmatched_topic is not None
            else None
        ),
        notebook_action=(
            NotebookActionView(
                op=result.notebook_action.op,
                body=result.notebook_action.body,
                title=result.notebook_action.title,
                note_type=result.notebook_action.note_type,
                target_note_id=result.notebook_action.target_note_id,
            )
            if result.notebook_action is not None
            else None
        ),
    )


@router.post(
    "/sessions",
    response_model=StartSessionResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def start_session(
    use_case: Annotated[StartChatSession, Depends(get_agent_start_session_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> StartSessionResponse:
    user = _require_user(principal)
    session = await use_case.execute(user_id=user.user_id)
    return StartSessionResponse(session_id=session.id, created_at=session.created_at)


@router.post(
    "/sessions/{session_id}/messages",
    response_model=AgentTurnResponse,
    response_model_by_alias=True,
    dependencies=[Depends(_agent_quota)],
)
async def send_message(
    session_id: UUID,
    body: AgentMessageRequest,
    use_case: Annotated[AnswerAgentTurn, Depends(get_agent_turn_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> AgentTurnResponse:
    _require_user(principal)
    try:
        result = await use_case.execute(
            session_id=session_id,
            user_content=body.content,
            attachments=tuple(body.attachments),
        )
    except ChatSessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ChatProviderError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return _turn_response(result)


@router.get(
    "/sessions/{session_id}",
    response_model=ChatHistoryResponse,
    response_model_by_alias=True,
)
async def get_history(
    session_id: UUID,
    use_case: Annotated[GetChatHistory, Depends(get_agent_history_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
    limit: Annotated[int | None, Query(ge=1, le=MAX_CHAT_HISTORY_LIMIT)] = None,
    before: Annotated[str | None, Query()] = None,
) -> ChatHistoryResponse:
    """Session history, oldest message first. Without ``limit`` the whole
    history is returned (unchanged). With ``limit`` the most-recent N
    messages are returned plus a ``nextCursor``; pass it back as ``before``
    to load the previous (older) page — so a long conversation no longer
    transfers in full on every open."""
    _require_user(principal)
    try:
        page = await use_case.execute(session_id, limit=limit, before=before)
    except ChatSessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return ChatHistoryResponse(
        session_id=session_id,
        messages=[_message_response(m) for m in page.messages],
        next_cursor=page.next_cursor,
    )


__all__ = [
    "get_agent_history_uc",
    "get_agent_start_session_uc",
    "get_agent_turn_uc",
    "router",
]
