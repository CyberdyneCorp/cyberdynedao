"""Ports the quizzes context depends on."""

from __future__ import annotations

from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.quizzes.entities import Quiz, QuizAttempt


@runtime_checkable
class QuizRepository(Protocol):
    async def get_by_lesson(self, lesson_id: UUID, *, locale: str = "en") -> Quiz:
        """Load the quiz (questions + options) for a lesson. Raises
        ``QuizNotFoundError``. A non-English ``locale`` overlays localized
        prompt/explanation/option text with per-field English fallback."""
        ...

    async def upsert(self, quiz: Quiz) -> None:
        """Insert the quiz for ``quiz.lesson_id``, or reconcile it in place
        if one already exists. The quiz aggregate owns its questions and
        options, but they are matched to existing rows by position and
        updated in place (not deleted and re-inserted) so dependent rows
        keyed on their ids — e.g. quiz translations — survive a re-save.
        The passed ``quiz`` is mutated to the persisted ids."""
        ...

    async def delete_by_lesson(self, lesson_id: UUID) -> None:
        """Delete the lesson's quiz (and its attempts). No-op if absent."""
        ...

    async def add_attempt(self, attempt: QuizAttempt) -> QuizAttempt:
        """Persist a graded attempt and return it."""
        ...

    async def list_attempts(self, *, user_id: UUID, quiz_id: UUID) -> list[QuizAttempt]:
        """A user's attempts at a quiz, oldest first."""
        ...

    async def count_attempts(self, *, user_id: UUID, quiz_id: UUID) -> int:
        """How many times the user has already attempted the quiz."""
        ...


@runtime_checkable
class LessonCompleter(Protocol):
    """Marks a lesson complete for a learner. The quizzes context owns
    this abstract seam so a passing attempt can auto-complete its lesson
    without quizzes depending on the courses context; the concrete
    implementation lives in the courses application layer."""

    async def complete_lesson(self, *, user_id: UUID, lesson_id: UUID) -> None:
        """Mark the lesson 100% complete for the learner. A no-op if the
        lesson isn't part of a course (so non-course quizzes are safe)."""
        ...
