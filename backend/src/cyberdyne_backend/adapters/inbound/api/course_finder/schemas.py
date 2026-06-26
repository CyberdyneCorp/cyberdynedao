"""Pydantic schemas for the Scan-to-Learn endpoint (issue #231)."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ScanQuerySchema(_CamelModel):
    """The question the vision step extracted from the photo."""

    question: str
    subject: str | None = None
    keywords: list[str] = []


class CourseMatchSchema(_CamelModel):
    """One ranked catalog hit. ``lessonId`` is set for a deep-linkable lesson."""

    course_slug: str
    lesson_id: UUID | None = None
    score: float
    match_reason: str


class ScanResponse(_CamelModel):
    """Result of a scan: the extracted query and any ranked matches. When
    ``noMatch`` is true the client can offer to request the course."""

    query: ScanQuerySchema
    matches: list[CourseMatchSchema]
    no_match: bool
