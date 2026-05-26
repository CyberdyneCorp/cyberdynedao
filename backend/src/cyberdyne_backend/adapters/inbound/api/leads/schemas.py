"""Pydantic schemas for the leads endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    """Same camelCase contract as the content schemas."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


ChannelLiteral = Literal["contact_form", "marketplace_service_inquiry", "chat_agent_handoff"]
StatusLiteral = Literal["new", "triaged", "in_progress", "closed"]
EventKindLiteral = Literal["created", "status_changed", "note_added", "owner_assigned"]


class CreateAskRequest(_CamelModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )

    name: str = Field(min_length=1, max_length=128)
    # Plain str with a minimal pattern; full RFC 5322 validation would
    # require email-validator. The captcha + admin triage are the real
    # gates against junk submissions.
    email: str = Field(min_length=3, max_length=256, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    body: str = Field(min_length=1, max_length=4000)
    channel: ChannelLiteral = "contact_form"
    product_slug: str | None = Field(default=None, max_length=64)
    source_url: str | None = Field(default=None, max_length=512)
    captcha_token: str = Field(min_length=1, max_length=4096)


class AskEventResponse(_CamelModel):
    id: UUID
    kind: EventKindLiteral
    by_user_id: UUID | None = None
    at: datetime


class AskResponse(_CamelModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )

    id: UUID
    channel: ChannelLiteral
    name: str
    email: str
    body: str
    product_slug: str | None = None
    source_url: str | None = None
    status: StatusLiteral
    owner_user_id: UUID | None = None
    notes_md: str
    created_at: datetime


class AskDetailResponse(AskResponse):
    events: list[AskEventResponse]


class AdminListAsksResponse(_CamelModel):
    items: list[AskResponse]
    total: int
    page: int
    page_size: int


class UpdateAskRequest(_CamelModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )

    new_status: StatusLiteral | None = None
    note: str | None = None
    new_owner_user_id: UUID | None = None
