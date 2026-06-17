"""Quizzes bounded context.

Lesson-attached assessments: each quiz holds 1-15 questions, every
question 2-6 options with exactly one correct, plus a static explanation
shown as feedback after grading. Grading is pure-domain; attempts are
tracked per user with retry-on-fail (monotonic attempt numbers). The
player surface never receives the correct flags or explanations until an
attempt is submitted.
"""

from cyberdyne_backend.domain.quizzes.catalog import (
    DEFAULT_CATALOG_LIMIT,
    MAX_CATALOG_LIMIT,
    LastAttempt,
    QuizCatalogPage,
    QuizSummary,
)
from cyberdyne_backend.domain.quizzes.entities import (
    DEFAULT_PASSING_SCORE,
    MAX_OPTIONS,
    MAX_QUESTIONS,
    MIN_OPTIONS,
    MIN_QUESTIONS,
    GradedAttempt,
    Question,
    QuestionOption,
    QuestionResult,
    Quiz,
    QuizAttempt,
    build_question,
    grade,
    new_attempt,
    new_quiz,
)
from cyberdyne_backend.domain.quizzes.errors import (
    InvalidAttemptError,
    InvalidQuizError,
    QuizNotFoundError,
)
from cyberdyne_backend.domain.quizzes.ports import (
    LessonCompleter,
    QuizCatalogReader,
    QuizRepository,
)

__all__ = [
    "DEFAULT_CATALOG_LIMIT",
    "DEFAULT_PASSING_SCORE",
    "MAX_CATALOG_LIMIT",
    "MAX_OPTIONS",
    "MAX_QUESTIONS",
    "MIN_OPTIONS",
    "MIN_QUESTIONS",
    "GradedAttempt",
    "InvalidAttemptError",
    "InvalidQuizError",
    "LastAttempt",
    "LessonCompleter",
    "Question",
    "QuestionOption",
    "QuestionResult",
    "Quiz",
    "QuizAttempt",
    "QuizCatalogPage",
    "QuizCatalogReader",
    "QuizNotFoundError",
    "QuizRepository",
    "QuizSummary",
    "build_question",
    "grade",
    "new_attempt",
    "new_quiz",
]
