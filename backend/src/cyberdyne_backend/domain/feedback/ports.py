"""Repository port for the learner-feedback context."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from cyberdyne_backend.domain.feedback.entities import (
    Feedback,
    FeedbackKind,
    FeedbackStatus,
)


@runtime_checkable
class FeedbackRepository(Protocol):
    async def add(self, feedback: Feedback) -> Feedback:
        """Persist a feedback item and return it."""
        ...

    async def list_all(
        self,
        *,
        kind: FeedbackKind | None = None,
        status: FeedbackStatus | None = None,
    ) -> list[Feedback]:
        """All feedback for triage, newest first, optionally filtered by
        ``kind`` and/or ``status``."""
        ...
