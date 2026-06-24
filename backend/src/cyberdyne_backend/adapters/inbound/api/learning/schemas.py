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


class CertificateVerificationResponse(_CamelModel):
    valid: bool
    certificate: CertificateResponse | None = None


class SigningKeyResponse(_CamelModel):
    # `publicKey` is the base64url Ed25519 verification key for external
    # verifiers; null for HMAC (a shared secret that must not be published).
    algorithm: Literal["hmac-sha256", "ed25519"]
    public_key: str | None = None


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


class ModuleGateResponse(_CamelModel):
    module_slug: str
    level: str
    position: int
    unlocked: bool
    completed: bool
    blocked_by: str | None = None
    reason: Literal["level", "sequential"] | None = None


class EligibilityResponse(_CamelModel):
    eligible: bool
    already_enrolled: bool
    next_module: str | None = None
    reason: str | None = None


# ── Admin catalogue CRUD request schemas ─────────────────────────────

LevelLiteral = Literal["Beginner", "Intermediate", "Advanced"]


class _StrictCamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )


class CreateModuleRequest(_StrictCamelModel):
    title: str = Field(min_length=1)
    category: str = Field(min_length=1)
    description: str
    level: LevelLiteral
    duration: str = Field(min_length=1)
    icon: str = Field(min_length=1)
    topics: list[str] = Field(default_factory=list)
    slug: str | None = None


class UpdateModuleRequest(_StrictCamelModel):
    title: str | None = None
    category: str | None = None
    description: str | None = None
    level: LevelLiteral | None = None
    duration: str | None = None
    icon: str | None = None
    topics: list[str] | None = None


class CreatePathRequest(_StrictCamelModel):
    title: str = Field(min_length=1)
    description: str
    module_slugs: list[str] = Field(default_factory=list)
    estimated_time: str = Field(min_length=1)
    icon: str = Field(min_length=1)
    slug: str | None = None


class UpdatePathRequest(_StrictCamelModel):
    title: str | None = None
    description: str | None = None
    module_slugs: list[str] | None = None
    estimated_time: str | None = None
    icon: str | None = None


class ReorderPathModulesRequest(_StrictCamelModel):
    module_slugs: list[str]
