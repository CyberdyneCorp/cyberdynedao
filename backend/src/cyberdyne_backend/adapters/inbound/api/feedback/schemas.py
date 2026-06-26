"""Pydantic schemas for the learner-feedback endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

FeedbackKindLiteral = Literal["problem", "feature"]
FeedbackStatusLiteral = Literal["new", "triaged", "closed"]


class _CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class SubmitFeedbackRequest(_CamelModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )

    kind: FeedbackKindLiteral
    message: str = Field(min_length=1, max_length=4000)
    course_id: str | None = Field(default=None, max_length=128)
    lesson_id: str | None = Field(default=None, max_length=128)
    app_version: str | None = Field(default=None, max_length=64)
    platform: str | None = Field(default=None, max_length=32)


class FeedbackResponse(_CamelModel):
    id: UUID
    kind: FeedbackKindLiteral
    status: FeedbackStatusLiteral
    message: str
    course_id: str | None = None
    lesson_id: str | None = None
    app_version: str | None = None
    platform: str | None = None
    created_at: datetime
    updated_at: datetime
