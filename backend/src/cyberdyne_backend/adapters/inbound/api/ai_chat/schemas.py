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


class ToolCallView(_CamelModel):
    id: str
    name: str
    arguments_json: str


class ChatMessageResponse(_CamelModel):
    id: UUID
    session_id: UUID
    role: Literal["user", "assistant", "tool", "system"]
    content: str
    tool_calls: list[ToolCallView] = []
    tool_call_id: str | None = None
    tokens_in: int = 0
    tokens_out: int = 0
    model: str | None = None
    created_at: datetime


class ChatHistoryResponse(_CamelModel):
    session_id: UUID
    messages: list[ChatMessageResponse]
