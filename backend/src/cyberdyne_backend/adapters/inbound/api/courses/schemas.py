"""Pydantic schemas for courses endpoints."""

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


class _StrictCamelModel(_CamelModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )


LevelLiteral = Literal["Beginner", "Intermediate", "Advanced"]
StatusLiteral = Literal["draft", "published"]
LessonTypeLiteral = Literal["video", "pdf", "presentation", "text", "quiz"]


# ── Responses ─────────────────────────────────────────────────────────


class LessonResponse(_CamelModel):
    id: UUID
    course_id: UUID
    title: str
    lesson_type: LessonTypeLiteral
    sort_order: int
    content_url: str | None = None
    text_body: str | None = None
    duration: str | None = None


class CourseSummaryResponse(_CamelModel):
    id: UUID
    slug: str
    title: str
    description: str
    level: LevelLiteral
    status: StatusLiteral
    mandatory: bool
    sort_order: int
    lesson_count: int
    created_at: datetime
    published_at: datetime | None = None


class CourseDetailResponse(CourseSummaryResponse):
    lessons: list[LessonResponse]


# ── Requests ──────────────────────────────────────────────────────────


class CreateCourseRequest(_StrictCamelModel):
    title: str = Field(min_length=1, max_length=256)
    description: str = ""
    level: LevelLiteral
    slug: str | None = Field(default=None, max_length=128)
    mandatory: bool = False
    sort_order: int = 0


class UpdateCourseRequest(_StrictCamelModel):
    title: str | None = Field(default=None, min_length=1, max_length=256)
    description: str | None = None
    mandatory: bool | None = None
    sort_order: int | None = None


class ReorderCoursesRequest(_StrictCamelModel):
    # {slug: sort_order}
    order: dict[str, int]


class CreateLessonRequest(_StrictCamelModel):
    title: str = Field(min_length=1, max_length=256)
    lesson_type: LessonTypeLiteral
    content_url: str | None = Field(default=None, max_length=2048)
    text_body: str | None = None
    duration: str | None = Field(default=None, max_length=32)
    sort_order: int = 0


class UpdateLessonRequest(_StrictCamelModel):
    title: str | None = Field(default=None, min_length=1, max_length=256)
    content_url: str | None = Field(default=None, max_length=2048)
    text_body: str | None = None
    duration: str | None = Field(default=None, max_length=32)
    sort_order: int | None = None


class ReorderLessonsRequest(_StrictCamelModel):
    # {lessonId: sort_order}
    order: dict[UUID, int]
