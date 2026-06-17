"""Browse/practice read-model for quizzes (issue #169).

A learner-facing catalogue view that lists quizzes *across* lessons and
courses — independent of navigating into a single lesson. This is a pure
read model: it carries denormalized course/lesson metadata plus the
requesting learner's most-recent attempt, and owns no persistence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

# Browse paging caps. Kept here so the use case and adapter agree.
DEFAULT_CATALOG_LIMIT = 20
MAX_CATALOG_LIMIT = 100


@dataclass(slots=True)
class LastAttempt:
    """A learner's most recent attempt at a quiz (summary only)."""

    score: int
    passed: bool
    attempt_number: int
    submitted_at: datetime


@dataclass(slots=True)
class QuizSummary:
    """One browsable quiz with the metadata the Quizzes nav needs."""

    quiz_id: UUID
    lesson_id: UUID
    lesson_title: str
    course_slug: str
    course_title: str
    category_slug: str | None
    passing_score: int
    question_count: int
    last_attempt: LastAttempt | None = None


@dataclass(slots=True)
class QuizCatalogPage:
    """A page of browsable quizzes plus an opaque forward cursor.

    ``next_cursor`` is ``None`` on the last page.
    """

    items: list[QuizSummary] = field(default_factory=list)
    next_cursor: str | None = None
