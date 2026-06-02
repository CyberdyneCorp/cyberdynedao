"""Pydantic schemas for the course-recommendations endpoint."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class CourseRecommendationResponse(_CamelModel):
    slug: str
    title: str
    level: str
    reason: str


class RecommendationsResponse(_CamelModel):
    # LLM-personalized intro framing the shortlist below.
    summary: str
    courses: list[CourseRecommendationResponse]
