"""Pydantic schemas for the lesson-notes endpoints."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class _StrictCamelModel(_CamelModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, extra="forbid")


class LessonNoteResponse(_CamelModel):
    id: UUID
    course_slug: str
    lesson_id: str
    quote: str | None = None
    body: str
    created_at: datetime
    updated_at: datetime | None = None


class LessonNoteListResponse(_CamelModel):
    items: list[LessonNoteResponse]
    next_cursor: str | None = None


class CreateLessonNoteRequest(_StrictCamelModel):
    # Client-supplied id makes the on-device → server sync idempotent.
    id: UUID | None = None
    course_slug: str = Field(min_length=1, max_length=128)
    quote: str | None = Field(default=None, max_length=4000)
    body: str = Field(min_length=1, max_length=10000)


class UpdateLessonNoteRequest(_StrictCamelModel):
    # All optional: only provided fields change. `quote: null` clears it.
    body: str | None = Field(default=None, min_length=1, max_length=10000)
    quote: str | None = Field(default=None, max_length=4000)
