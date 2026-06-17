"""Pydantic schemas for the achievements endpoint."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class ProgressResponse(_CamelModel):
    current: int
    target: int


class AchievementResponse(_CamelModel):
    id: str
    key: str
    title: str
    description: str
    icon: str
    # Set once earned; null while in progress.
    earned_at: datetime | None
    progress: ProgressResponse
