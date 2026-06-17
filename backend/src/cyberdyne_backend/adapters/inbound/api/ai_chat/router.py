"""AI chat endpoints — sessions + send-message + history.

The frontend's existing chat terminal posts one message at a time and
renders the JSON reply. SSE streaming of the *response token deltas*
is deliberately deferred — the assistant message contains the full
content already and the frontend can fake-stream it client-side. Phase
6 follow-up turns this into a real ``text/event-stream`` once the LLM
client streams.
"""

from __future__ import annotations

import json
import logging
from collections.abc import AsyncIterator
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse

from cyberdyne_backend.adapters.inbound.api.ai_chat.schemas import (
    ChatHistoryResponse,
    ChatMessageResponse,
    SendMessageRequest,
    StartSessionResponse,
    ToolCallView,
)
from cyberdyne_backend.application.ai_chat import (
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

logger = logging.getLogger("cyberdyne_backend.ai_chat.api")

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


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
) -> ChatHistoryResponse:
    try:
        messages = await use_case.execute(session_id)
    except ChatSessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return ChatHistoryResponse(
        session_id=session_id,
        messages=[_message_response(m) for m in messages],
    )


__all__ = [
    "get_history_uc",
    "get_run_turn_uc",
    "get_start_session_uc",
    "get_stream_turn_uc",
    "router",
]
