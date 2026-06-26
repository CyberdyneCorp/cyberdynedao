"""AI chat domain entities."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID


class ChatRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass(frozen=True, slots=True)
class ToolCall:
    """A single tool invocation request emitted by the assistant."""

    id: str  # provider-assigned (OpenAI gives ``call_…``)
    name: str
    arguments_json: str


@dataclass(frozen=True, slots=True)
class AttachmentRef:
    """A file a learner attached to a user turn — the durable upload id
    plus the display metadata the frontend renders (issue #220)."""

    id: UUID
    filename: str
    content_type: str


@dataclass(slots=True)
class ChatMessage:
    id: UUID
    session_id: UUID
    role: ChatRole
    content: str
    tool_calls: tuple[ToolCall, ...] = ()
    tool_call_id: str | None = None  # set on TOOL-role messages
    tokens_in: int = 0
    tokens_out: int = 0
    model: str | None = None
    # Files the learner attached to this (user) turn — echoed back in
    # history so the frontend can render them (issue #220).
    attachments: tuple[AttachmentRef, ...] = ()
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))


@dataclass(slots=True)
class ChatSession:
    id: UUID
    user_id: UUID | None  # anonymous chats allowed
    created_at: datetime
    last_message_at: datetime | None = None


def new_session(*, user_id: UUID | None = None, now: datetime | None = None) -> ChatSession:
    moment = now or datetime.now(tz=UTC)
    return ChatSession(id=uuid.uuid4(), user_id=user_id, created_at=moment)


def _new_message(
    *,
    session_id: UUID,
    role: ChatRole,
    content: str,
    tool_calls: tuple[ToolCall, ...] = (),
    tool_call_id: str | None = None,
    tokens_in: int = 0,
    tokens_out: int = 0,
    model: str | None = None,
    attachments: tuple[AttachmentRef, ...] = (),
    now: datetime | None = None,
) -> ChatMessage:
    return ChatMessage(
        id=uuid.uuid4(),
        session_id=session_id,
        role=role,
        content=content,
        tool_calls=tool_calls,
        tool_call_id=tool_call_id,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        model=model,
        attachments=attachments,
        created_at=now or datetime.now(tz=UTC),
    )


def new_user_message(
    *,
    session_id: UUID,
    content: str,
    attachments: tuple[AttachmentRef, ...] = (),
) -> ChatMessage:
    return _new_message(
        session_id=session_id,
        role=ChatRole.USER,
        content=content,
        attachments=attachments,
    )


def new_assistant_message(
    *,
    session_id: UUID,
    content: str,
    tool_calls: tuple[ToolCall, ...] = (),
    tokens_in: int = 0,
    tokens_out: int = 0,
    model: str | None = None,
) -> ChatMessage:
    return _new_message(
        session_id=session_id,
        role=ChatRole.ASSISTANT,
        content=content,
        tool_calls=tool_calls,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        model=model,
    )


def new_tool_message(*, session_id: UUID, tool_call_id: str, content: str) -> ChatMessage:
    return _new_message(
        session_id=session_id,
        role=ChatRole.TOOL,
        content=content,
        tool_call_id=tool_call_id,
    )
