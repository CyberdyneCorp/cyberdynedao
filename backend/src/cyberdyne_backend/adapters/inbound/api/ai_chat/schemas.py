"""Pydantic schemas for the AI chat endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class StartSessionResponse(_CamelModel):
    session_id: UUID
    created_at: datetime


class SendMessageRequest(_CamelModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )

    content: str = Field(min_length=1, max_length=4000)
    # Upload-and-analyze: the interpreter session the user uploaded files to
    # (so python_exec runs in that workspace) and the attached filenames (so
    # the agent knows what to read). Optional — absent for plain chat.
    interpreter_session_id: str | None = Field(default=None, max_length=128)
    attachments: list[str] = Field(default_factory=list, max_length=20)


class ToolCallView(_CamelModel):
    id: str
    name: str
    arguments_json: str


class AttachmentView(_CamelModel):
    """A learner-attached file on a user turn, for frontend rendering."""

    id: UUID
    filename: str
    content_type: str


class ChatMessageResponse(_CamelModel):
    id: UUID
    session_id: UUID
    role: Literal["user", "assistant", "tool", "system"]
    content: str
    tool_calls: list[ToolCallView] = []
    attachments: list[AttachmentView] = []
    tool_call_id: str | None = None
    tokens_in: int = 0
    tokens_out: int = 0
    model: str | None = None
    created_at: datetime


class ChatHistoryResponse(_CamelModel):
    session_id: UUID
    messages: list[ChatMessageResponse]


# ── Streaming (SSE) event chunks ─────────────────────────────────────
#
# `POST /api/v1/chat/sessions/{id}/messages/stream` returns
# `text/event-stream`. Each SSE event is a single `data:` line holding one
# JSON object below, terminated by a blank line (`data: <json>\n\n`).
# There is NO `[DONE]` sentinel — the terminal event is `type: "done"`,
# which carries the full persisted assistant `ChatMessageResponse`
# (including any `toolCalls`). These models exist to document the chunk
# schema (and for client codegen); the endpoint streams raw JSON, not a
# declared `response_model`. See docs/chat-streaming.md.


class StreamStatusEvent(_CamelModel):
    """A tool round is starting; `tool` is the tool name about to run."""

    type: Literal["status"] = "status"
    tool: str


class StreamDeltaEvent(_CamelModel):
    """An incremental chunk of the assistant's answer text."""

    type: Literal["delta"] = "delta"
    text: str


class StreamDoneEvent(_CamelModel):
    """Terminal event: the full persisted assistant message."""

    type: Literal["done"] = "done"
    message: ChatMessageResponse


class StreamErrorEvent(_CamelModel):
    """An error delivered in-band (the stream had already begun, so the
    HTTP status is still 200); `detail` is a human-readable message."""

    type: Literal["error"] = "error"
    detail: str
