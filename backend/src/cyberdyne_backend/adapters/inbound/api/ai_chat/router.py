"""AI chat endpoints — sessions + send-message + history + streaming.

Two ways to run a turn share the same persist + tool-call loop:

  - ``POST .../messages`` — buffers the whole turn and returns the final
    assistant ``ChatMessageResponse`` as JSON.
  - ``POST .../messages/stream`` — a real ``text/event-stream`` that
    relays answer-text deltas and tool-round status as they happen,
    terminated by a ``done`` event carrying the persisted assistant
    message. See ``docs/chat-streaming.md`` for the wire contract.
"""

from __future__ import annotations

import json
import logging
from collections.abc import AsyncIterator
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import StreamingResponse

from cyberdyne_backend.adapters.inbound.api.ai_chat.schemas import (
    AttachmentView,
    ChatHistoryResponse,
    ChatMessageResponse,
    SendMessageRequest,
    StartSessionResponse,
    ToolCallView,
)
from cyberdyne_backend.adapters.inbound.api.quota.dependencies import QuotaGuard
from cyberdyne_backend.adapters.inbound.api.rate_limit import SlidingWindowRateLimiter
from cyberdyne_backend.application.ai_chat import (
    MAX_CHAT_HISTORY_LIMIT,
    GetChatHistory,
    RunChatTurn,
    StartChatSession,
    StreamChatTurn,
)
from cyberdyne_backend.domain.ai_chat import (
    ChatMessage,
    ChatProviderError,
    ChatSessionNotFoundError,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.quota import QuotaMeter

logger = logging.getLogger("cyberdyne_backend.ai_chat.api")

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

# Per-IP cap on chat turns — a coarse guard against a single client
# burning LLM tokens in a loop (issue #7). Per-replica, resets on restart;
# shared across the JSON + streaming message endpoints.
_chat_rate_limiter = SlidingWindowRateLimiter(
    limit=20, window_s=60.0, detail="too many chat messages; slow down"
)


def _chat_rate_limit(request: Request) -> None:
    client = request.client
    _chat_rate_limiter.check(client.host if client is not None else None)


# Per-user free-tier cap + Pro fair-use on tutor turns (issue #230); the per-IP
# limiter above still guards anonymous traffic.
_tutor_quota = QuotaGuard(QuotaMeter.TUTOR_MESSAGES)


async def get_start_session_uc() -> StartChatSession:  # pragma: no cover
    raise NotImplementedError


async def get_run_turn_uc() -> RunChatTurn:  # pragma: no cover
    raise NotImplementedError


async def get_stream_turn_uc() -> StreamChatTurn:  # pragma: no cover
    raise NotImplementedError


async def get_history_uc() -> GetChatHistory:  # pragma: no cover
    raise NotImplementedError


def _sse(data: dict[str, object]) -> str:
    return f"data: {json.dumps(data)}\n\n"


def _message_response(m: ChatMessage) -> ChatMessageResponse:
    return ChatMessageResponse(
        id=m.id,
        session_id=m.session_id,
        role=m.role.value,
        content=m.content,
        tool_calls=[
            ToolCallView(id=tc.id, name=tc.name, arguments_json=tc.arguments_json)
            for tc in m.tool_calls
        ],
        attachments=[
            AttachmentView(id=a.id, filename=a.filename, content_type=a.content_type)
            for a in m.attachments
        ],
        tool_call_id=m.tool_call_id,
        tokens_in=m.tokens_in,
        tokens_out=m.tokens_out,
        model=m.model,
        created_at=m.created_at,
    )


@router.post(
    "/sessions",
    response_model=StartSessionResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def start_session(
    request: Request,
    use_case: Annotated[StartChatSession, Depends(get_start_session_uc)],
) -> StartSessionResponse:
    principal = getattr(request.state, "principal", None)
    user_id: UUID | None = None
    if isinstance(principal, UserPrincipal):
        user_id = principal.user_id
    session = await use_case.execute(user_id=user_id)
    return StartSessionResponse(session_id=session.id, created_at=session.created_at)


@router.post(
    "/sessions/{session_id}/messages",
    response_model=ChatMessageResponse,
    response_model_by_alias=True,
    dependencies=[Depends(_chat_rate_limit), Depends(_tutor_quota)],
)
async def send_message(
    session_id: UUID,
    body: SendMessageRequest,
    use_case: Annotated[RunChatTurn, Depends(get_run_turn_uc)],
) -> ChatMessageResponse:
    try:
        message = await use_case.execute(
            session_id=session_id,
            user_content=body.content,
            interpreter_session_id=body.interpreter_session_id,
            attachments=tuple(body.attachments),
        )
    except ChatSessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ChatProviderError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return _message_response(message)


@router.post(
    "/sessions/{session_id}/messages/stream",
    dependencies=[Depends(_chat_rate_limit), Depends(_tutor_quota)],
    responses={
        200: {
            "description": (
                "A Server-Sent Events stream (`text/event-stream`). Each event "
                "is one `data:` line holding a JSON object, terminated by a "
                "blank line: `data: <json>\\n\\n`. The `type` field "
                "discriminates the chunk: `status` (a tool round is starting), "
                "`delta` (an answer-text chunk), `done` (terminal event "
                "carrying the full persisted assistant `ChatMessageResponse`, "
                "including any `toolCalls`), or `error` (delivered in-band — "
                "the HTTP status is still 200). There is **no** `[DONE]` "
                "sentinel; `done` is the terminal marker. See "
                "docs/chat-streaming.md for the full contract + a reference "
                "transcript."
            ),
            "content": {
                "text/event-stream": {
                    "schema": {
                        "type": "string",
                        "description": (
                            "SSE byte stream. Per-chunk JSON shapes: "
                            "StreamStatusEvent | StreamDeltaEvent | "
                            "StreamDoneEvent | StreamErrorEvent."
                        ),
                    },
                    "example": (
                        'data: {"type": "status", "tool": "list_projects"}\n\n'
                        'data: {"type": "delta", "text": "We build "}\n\n'
                        'data: {"type": "delta", "text": "CyberSTAC."}\n\n'
                        'data: {"type": "done", "message": {"id": '
                        '"4f1c...", "sessionId": "9ab2...", "role": '
                        '"assistant", "content": "We build CyberSTAC.", '
                        '"toolCalls": [], "createdAt": '
                        '"2026-06-17T12:00:00Z"}}\n\n'
                    ),
                }
            },
        }
    },
)
async def stream_message(
    session_id: UUID,
    body: SendMessageRequest,
    use_case: Annotated[StreamChatTurn, Depends(get_stream_turn_uc)],
) -> StreamingResponse:
    """Server-Sent Events twin of send_message.

    Content type is ``text/event-stream``; each event is a single
    ``data: <json>\\n\\n`` line. The JSON ``type`` field discriminates:

    - ``{"type": "status", "tool": "<name>"}`` — a tool round is starting.
    - ``{"type": "delta", "text": "<chunk>"}`` — an answer-text chunk;
      concatenate ``text`` across deltas to rebuild the reply.
    - ``{"type": "done", "message": {<ChatMessageResponse>}}`` — terminal
      event with the full persisted assistant message (camelCase, includes
      ``toolCalls``). This replaces a ``[DONE]`` sentinel.
    - ``{"type": "error", "detail": "<message>"}`` — error delivered
      in-band (the stream has already begun, so HTTP status stays 200).

    See ``docs/chat-streaming.md`` for the authoritative contract and a
    reference transcript. The non-streaming ``POST .../messages`` returns
    the same final ``ChatMessageResponse`` as a plain JSON body.
    """

    async def gen() -> AsyncIterator[str]:
        try:
            async for ev in use_case.execute(
                session_id=session_id,
                user_content=body.content,
                interpreter_session_id=body.interpreter_session_id,
                attachments=tuple(body.attachments),
            ):
                if ev.kind == "delta":
                    yield _sse({"type": "delta", "text": ev.text})
                elif ev.kind == "status":
                    yield _sse({"type": "status", "tool": ev.text})
                elif ev.kind == "done" and ev.message is not None:
                    yield _sse(
                        {
                            "type": "done",
                            "message": _message_response(ev.message).model_dump(
                                by_alias=True, mode="json"
                            ),
                        }
                    )
                elif ev.kind == "error":
                    yield _sse({"type": "error", "detail": ev.text})
        except ChatSessionNotFoundError as exc:
            yield _sse({"type": "error", "detail": str(exc)})
        except ChatProviderError as exc:
            yield _sse({"type": "error", "detail": str(exc)})
        except Exception:  # never break the SSE contract mid-stream
            logger.exception("stream turn failed for session %s", session_id)
            yield _sse({"type": "error", "detail": "internal error"})

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.get(
    "/sessions/{session_id}",
    response_model=ChatHistoryResponse,
    response_model_by_alias=True,
)
async def get_history(
    session_id: UUID,
    use_case: Annotated[GetChatHistory, Depends(get_history_uc)],
    limit: Annotated[int | None, Query(ge=1, le=MAX_CHAT_HISTORY_LIMIT)] = None,
    before: Annotated[str | None, Query()] = None,
) -> ChatHistoryResponse:
    """Session history, oldest first. ``limit`` returns the most-recent N
    messages plus a ``nextCursor`` (pass back as ``before`` for the older
    page); omitting ``limit`` returns the whole history as before."""
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
    "get_history_uc",
    "get_run_turn_uc",
    "get_start_session_uc",
    "get_stream_turn_uc",
    "router",
]
