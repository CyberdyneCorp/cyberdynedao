"""Pydantic schemas for the Skill Map endpoint."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class SkillMasteryResponse(_CamelModel):
    id: str
    name: str
    domain: str
    mastery: int  # 0..100
    course_count: int
    weak: bool


class SkillMapResponse(_CamelModel):
    skills: list[SkillMasteryResponse]
    weak_areas: list[str]
    suggestions: list[str]
