"""Pydantic schemas for the concepts endpoints."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class _StrictCamelModel(_CamelModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, extra="forbid")


class ConceptResponse(_CamelModel):
    id: UUID
    slug: str
    title: str
    domain: str
    summary: str
    formula: str | None = None
    related_lessons: list[UUID] = []
    related_courses: list[str] = []
    created_at: datetime
    updated_at: datetime | None = None


class ConceptListResponse(_CamelModel):
    items: list[ConceptResponse]
    next_cursor: str | None = None


class ConceptWriteRequest(_StrictCamelModel):
    slug: str = Field(min_length=1, max_length=96)
    title: str = Field(min_length=1, max_length=160)
    domain: str = Field(min_length=1, max_length=64)
    summary: str = Field(min_length=1)
    formula: str | None = Field(default=None, max_length=2000)
    related_lessons: list[UUID] = Field(default_factory=list, max_length=100)
    related_courses: list[str] = Field(default_factory=list, max_length=100)
