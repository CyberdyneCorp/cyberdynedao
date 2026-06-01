"""Pydantic schemas for quiz endpoints.

Two response shapes for the quiz itself:
  * **player** — option text only, no ``isCorrect``, no ``explanation``.
    This is what an unsubmitted learner sees, so answers never leak.
  * **editor** — the full tree including correct flags + explanations.
Feedback (with explanations) is returned only in the attempt result,
after grading.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from cyberdyne_backend.domain.quizzes import (
    DEFAULT_PASSING_SCORE,
    MAX_OPTIONS,
    MAX_QUESTIONS,
    MIN_OPTIONS,
    MIN_QUESTIONS,
)


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class _StrictCamelModel(_CamelModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, extra="forbid")


# ── Player responses (answers stripped) ──────────────────────────────


class PlayerOptionResponse(_CamelModel):
    id: UUID
    text: str


class PlayerQuestionResponse(_CamelModel):
    id: UUID
    prompt: str
    options: list[PlayerOptionResponse]


class PlayerQuizResponse(_CamelModel):
    lesson_id: UUID
    passing_score: int
    questions: list[PlayerQuestionResponse]


# ── Editor responses (full tree) ─────────────────────────────────────


class EditorOptionResponse(_CamelModel):
    id: UUID
    text: str
    is_correct: bool


class EditorQuestionResponse(_CamelModel):
    id: UUID
    prompt: str
    explanation: str
    options: list[EditorOptionResponse]


class EditorQuizResponse(_CamelModel):
    id: UUID
    lesson_id: UUID
    passing_score: int
    questions: list[EditorQuestionResponse]


# ── Authoring requests ───────────────────────────────────────────────


class UpsertOptionRequest(_StrictCamelModel):
    text: str = Field(min_length=1, max_length=512)
    is_correct: bool = False


class UpsertQuestionRequest(_StrictCamelModel):
    prompt: str = Field(min_length=1, max_length=1024)
    explanation: str = ""
    options: list[UpsertOptionRequest] = Field(min_length=MIN_OPTIONS, max_length=MAX_OPTIONS)


class UpsertQuizRequest(_StrictCamelModel):
    passing_score: int = Field(default=DEFAULT_PASSING_SCORE, ge=1, le=100)
    questions: list[UpsertQuestionRequest] = Field(
        min_length=MIN_QUESTIONS, max_length=MAX_QUESTIONS
    )


# ── Attempts ──────────────────────────────────────────────────────────


class SubmitAttemptRequest(_StrictCamelModel):
    # {questionId: optionId}
    answers: dict[UUID, UUID]


class QuestionResultResponse(_CamelModel):
    question_id: UUID
    selected_option_id: UUID | None
    correct_option_id: UUID
    is_correct: bool
    explanation: str


class AttemptResultResponse(_CamelModel):
    attempt_id: UUID
    score: int
    passed: bool
    attempt_number: int
    submitted_at: datetime
    results: list[QuestionResultResponse]


class AttemptSummaryResponse(_CamelModel):
    id: UUID
    score: int
    passed: bool
    attempt_number: int
    submitted_at: datetime
