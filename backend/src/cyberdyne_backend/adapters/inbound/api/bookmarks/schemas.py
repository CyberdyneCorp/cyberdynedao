"""Pydantic schemas for the favorites/recently-viewed endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

BookmarkTypeLiteral = Literal["course", "lesson", "note"]


class _CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class FavoriteResponse(_CamelModel):
    id: UUID
    type: BookmarkTypeLiteral
    ref: str
    added_at: datetime


class AddFavoriteRequest(_CamelModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )

    type: BookmarkTypeLiteral
    ref: str = Field(min_length=1, max_length=128)


class RecentViewResponse(_CamelModel):
    id: UUID
    type: BookmarkTypeLiteral
    ref: str
    viewed_at: datetime


class RecordRecentRequest(_CamelModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )

    type: BookmarkTypeLiteral
    ref: str = Field(min_length=1, max_length=128)
