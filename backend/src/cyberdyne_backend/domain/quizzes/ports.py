"""Ports the quizzes context depends on."""

from __future__ import annotations

from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.quizzes.entities import Quiz, QuizAttempt


@runtime_checkable
class QuizRepository(Protocol):
    async def get_by_lesson(self, lesson_id: UUID) -> Quiz:
        """Load the quiz (questions + options) for a lesson. Raises
        ``QuizNotFoundError``."""
        ...

    async def upsert(self, quiz: Quiz) -> None:
        """Insert or fully replace the quiz for ``quiz.lesson_id`` —
        the quiz aggregate owns its questions and options, so a save
        rewrites them wholesale."""
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
