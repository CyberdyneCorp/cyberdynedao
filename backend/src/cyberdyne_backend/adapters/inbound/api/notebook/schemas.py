"""Pydantic schemas for the notebook notes endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

NoteTypeLiteral = Literal["lesson", "lab", "code", "simulation", "theory", "problem"]


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class _StrictCamelModel(_CamelModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, extra="forbid")


class NoteResponse(_CamelModel):
    id: UUID
    title: str
    type: NoteTypeLiteral
    body: str
    course_slug: str | None = None
    lesson_id: UUID | None = None
    code: str | None = None
    language: str | None = None
    run_result: dict[str, object] | None = None
    plot_refs: list[str] = []
    tags: list[str] = []
    created_at: datetime
    updated_at: datetime | None = None


class NoteListResponse(_CamelModel):
    items: list[NoteResponse]
    next_cursor: str | None = None


class NoteWriteRequest(_StrictCamelModel):
    title: str = Field(min_length=1, max_length=200)
    type: NoteTypeLiteral
    body: str = ""
    course_slug: str | None = Field(default=None, max_length=128)
    lesson_id: UUID | None = None
    code: str | None = None
    language: str | None = Field(default=None, max_length=32)
    run_result: dict[str, object] | None = None
    plot_refs: list[str] = Field(default_factory=list, max_length=50)
    tags: list[str] = Field(default_factory=list, max_length=50)
