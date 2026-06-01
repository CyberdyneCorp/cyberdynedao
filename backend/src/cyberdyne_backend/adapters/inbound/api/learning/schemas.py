"""Pydantic schemas for the learning endpoints."""

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


class LearningModuleResponse(_CamelModel):
    slug: str
    title: str
    category: str
    description: str
    level: Literal["Beginner", "Intermediate", "Advanced"] | str
    duration: str
    icon: str
    topics: list[str]


class LearningPathResponse(_CamelModel):
    slug: str
    title: str
    description: str
    module_slugs: list[str]
    estimated_time: str
    icon: str


class EnrollmentResponse(_CamelModel):
    id: UUID
    user_id: UUID
    path_slug: str
    started_at: datetime
    status: Literal["active", "completed", "dropped"]
    due_at: datetime | None = None


class ModuleProgressResponse(_CamelModel):
    module_slug: str
    percent: int
    started_at: datetime
    completed_at: datetime | None = None


class CertificateResponse(_CamelModel):
    id: UUID
    user_id: UUID
    path_slug: str
    issued_at: datetime
    verification_hash: str
    signed_payload: str


DeadlineStatusLiteral = Literal["none", "upcoming", "urgent", "overdue"]


class EnrollmentDeadlineResponse(_CamelModel):
    path_slug: str
    due_at: datetime | None = None
    status: DeadlineStatusLiteral
    days_remaining: int | None = None


class SetDeadlineRequest(_CamelModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )

    # null clears the deadline.
    due_at: datetime | None = None


class MyLearningStateResponse(_CamelModel):
    enrollments: list[EnrollmentResponse]
    progress: list[ModuleProgressResponse]
    certificates: list[CertificateResponse]


class UpdateProgressRequest(_CamelModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )

    percent: int = Field(ge=0, le=100)
