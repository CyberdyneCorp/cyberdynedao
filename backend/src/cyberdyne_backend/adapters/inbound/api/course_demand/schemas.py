"""Pydantic schemas for the course/topic demand registry endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

RequestSourceLiteral = Literal["typed", "scan"]


class _CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class SubmitCourseRequestRequest(_CamelModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )

    topic: str = Field(min_length=1, max_length=256)
    source: RequestSourceLiteral
    subject: str | None = Field(default=None, max_length=128)
    source_question_text: str | None = Field(default=None, max_length=8000)
    course_id: str | None = Field(default=None, max_length=128)
    lesson_id: str | None = Field(default=None, max_length=128)


class CourseRequestResponse(_CamelModel):
    """Acknowledgement of a captured request."""

    id: UUID
    topic: str
    topic_key: str
    subject: str | None = None
    source: RequestSourceLiteral
    created_at: datetime


class DemandClusterResponse(_CamelModel):
    """One ranked demand cluster for the authoring backlog."""

    topic_key: str
    topic: str
    subject: str | None = None
    count: int
    last_requested_at: datetime
