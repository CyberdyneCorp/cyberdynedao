"""Pydantic schemas for analytics endpoints."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class LearnerDashboardResponse(_CamelModel):
    enrolled_paths: int
    completed_paths: int
    active_paths: int
    completed_modules: int
    in_progress_modules: int
    avg_module_percent: float
    quizzes_attempted: int
    quizzes_passed: int
    quiz_pass_rate: float
    avg_quiz_score: float
    total_quiz_attempts: int
    certificates: int


class AdminOverviewResponse(_CamelModel):
    total_learners: int
    total_enrollments: int
    completed_enrollments: int
    enrollment_completion_rate: float
    published_courses: int
    draft_courses: int
    total_modules: int
    total_paths: int
    total_certificates: int
    total_quiz_attempts: int
    quiz_pass_rate: float
    avg_quiz_score: float
