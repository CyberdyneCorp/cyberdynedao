"""Quizzes domain entities, invariants, and grading.

A *quiz* is attached to a lesson (1:1, by ``lesson_id``) and holds an
ordered list of *questions*, each with 2-6 *options* of which exactly
one is correct. Each question carries a static ``explanation`` shown as
contextual feedback **after** an attempt is graded — never before, so
the player surface can render the quiz without leaking answers.

Grading is pure-domain: ``grade()`` takes the quiz and a
``{question_id: option_id}`` map and returns a ``GradedAttempt`` with the
score, pass/fail against the configurable passing score, and per-question
feedback. Persisting the attempt (and assigning its attempt number) is
the application/adapter's job.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from cyberdyne_backend.domain.quizzes.errors import (
    InvalidAttemptError,
    InvalidQuizError,
)

MIN_QUESTIONS = 1
MAX_QUESTIONS = 15
MIN_OPTIONS = 2
MAX_OPTIONS = 6
DEFAULT_PASSING_SCORE = 70


@dataclass(slots=True)
class QuestionOption:
    id: UUID
    text: str
    is_correct: bool
    sort_order: int = 0


@dataclass(slots=True)
class Question:
    id: UUID
    prompt: str
    explanation: str
    sort_order: int
    options: list[QuestionOption] = field(default_factory=list)

    @property
    def correct_option_id(self) -> UUID:
        for option in self.options:
            if option.is_correct:
                return option.id
        # ``validate`` guarantees exactly one correct option, so this is
        # unreachable on a validated quiz.
        raise InvalidQuizError(f"question {self.id} has no correct option")


@dataclass(slots=True)
class Quiz:
    id: UUID
    lesson_id: UUID
    passing_score: int
    questions: list[Question] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
    updated_at: datetime | None = None

    def validate(self) -> None:
        if not MIN_QUESTIONS <= len(self.questions) <= MAX_QUESTIONS:
            raise InvalidQuizError(
                f"quiz must have {MIN_QUESTIONS}-{MAX_QUESTIONS} questions, "
                f"got {len(self.questions)}"
            )
        if not 1 <= self.passing_score <= 100:
            raise InvalidQuizError(f"passing_score must be 1-100, got {self.passing_score}")
        for question in self.questions:
            n_options = len(question.options)
            if not MIN_OPTIONS <= n_options <= MAX_OPTIONS:
                raise InvalidQuizError(
                    f"question {question.id} must have {MIN_OPTIONS}-{MAX_OPTIONS} "
                    f"options, got {n_options}"
                )
            n_correct = sum(1 for o in question.options if o.is_correct)
            if n_correct != 1:
                raise InvalidQuizError(
                    f"question {question.id} must have exactly one correct option, got {n_correct}"
                )


# ── Attempts + grading ───────────────────────────────────────────────


@dataclass(slots=True)
class QuestionResult:
    question_id: UUID
    selected_option_id: UUID | None
    correct_option_id: UUID
    is_correct: bool
    explanation: str


@dataclass(slots=True)
class GradedAttempt:
    score: int  # 0-100
    passed: bool
    results: list[QuestionResult]


@dataclass(slots=True)
class QuizAttempt:
    id: UUID
    user_id: UUID
    quiz_id: UUID
    lesson_id: UUID
    score: int
    passed: bool
    attempt_number: int
    answers: dict[str, str]  # {question_id: option_id} as strings (JSON-friendly)
    submitted_at: datetime


# ── Factories ────────────────────────────────────────────────────────


def new_quiz(
    *,
    lesson_id: UUID,
    questions: list[Question],
    passing_score: int = DEFAULT_PASSING_SCORE,
    now: datetime | None = None,
) -> Quiz:
    moment = now or datetime.now(tz=UTC)
    quiz = Quiz(
        id=uuid.uuid4(),
        lesson_id=lesson_id,
        passing_score=passing_score,
        questions=questions,
        created_at=moment,
        updated_at=moment,
    )
    quiz.validate()
    return quiz


def build_question(
    *,
    prompt: str,
    explanation: str,
    options: list[tuple[str, bool]],
    sort_order: int = 0,
) -> Question:
    """Assemble a ``Question`` from ``(text, is_correct)`` option tuples,
    minting ids. Validation happens at the quiz level via ``validate``."""
    if not prompt.strip():
        raise InvalidQuizError("question prompt cannot be empty")
    return Question(
        id=uuid.uuid4(),
        prompt=prompt.strip(),
        explanation=explanation.strip(),
        sort_order=sort_order,
        options=[
            QuestionOption(id=uuid.uuid4(), text=text.strip(), is_correct=is_correct, sort_order=i)
            for i, (text, is_correct) in enumerate(options)
        ],
    )


def grade(quiz: Quiz, answers: dict[UUID, UUID], *, strict: bool = True) -> GradedAttempt:
    """Grade ``answers`` ({question_id: option_id}) against ``quiz``.

    A question is correct iff the selected option is the one flagged
    correct. Unanswered questions count as wrong. With ``strict=True`` an
    answer referencing an unknown question or an option that doesn't
    belong to its question raises ``InvalidAttemptError``.
    """
    questions_by_id = {q.id: q for q in quiz.questions}
    if strict:
        for q_id, opt_id in answers.items():
            question = questions_by_id.get(q_id)
            if question is None:
                raise InvalidAttemptError(f"unknown question {q_id}")
            if opt_id not in {o.id for o in question.options}:
                raise InvalidAttemptError(f"option {opt_id} does not belong to question {q_id}")

    results: list[QuestionResult] = []
    correct_count = 0
    for question in quiz.questions:
        selected = answers.get(question.id)
        correct_id = question.correct_option_id
        is_correct = selected == correct_id
        if is_correct:
            correct_count += 1
        results.append(
            QuestionResult(
                question_id=question.id,
                selected_option_id=selected,
                correct_option_id=correct_id,
                is_correct=is_correct,
                explanation=question.explanation,
            )
        )

    total = len(quiz.questions)
    score = round(correct_count / total * 100) if total else 0
    return GradedAttempt(score=score, passed=score >= quiz.passing_score, results=results)


def new_attempt(
    *,
    user_id: UUID,
    quiz: Quiz,
    graded: GradedAttempt,
    answers: dict[UUID, UUID],
    attempt_number: int,
    now: datetime | None = None,
) -> QuizAttempt:
    return QuizAttempt(
        id=uuid.uuid4(),
        user_id=user_id,
        quiz_id=quiz.id,
        lesson_id=quiz.lesson_id,
        score=graded.score,
        passed=graded.passed,
        attempt_number=attempt_number,
        answers={str(k): str(v) for k, v in answers.items()},
        submitted_at=now or datetime.now(tz=UTC),
    )
