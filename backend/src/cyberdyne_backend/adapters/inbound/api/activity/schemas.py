"""Pydantic schemas for the activity + learner-stats endpoints."""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

ActivityKindLiteral = Literal[
    "lesson_viewed", "code_run", "simulation_run", "concept_mastered"
]


class _CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class RecordActivityRequest(_CamelModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )

    kind: ActivityKindLiteral
    ref: str | None = Field(default=None, max_length=128)


class ActivityEventResponse(_CamelModel):
    id: UUID
    kind: ActivityKindLiteral
    ref: str | None
    occurred_at: datetime


class LearnerStatsResponse(_CamelModel):
    current_streak_days: int
    longest_streak_days: int
    last_active_on: date | None
    code_runs_count: int
    simulations_run: int
    concepts_mastered: int
