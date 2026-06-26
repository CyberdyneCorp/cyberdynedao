"""Use cases for the learner-feedback channel."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from cyberdyne_backend.domain.feedback.entities import (
    Feedback,
    FeedbackKind,
    FeedbackStatus,
    new_feedback,
)
from cyberdyne_backend.domain.feedback.ports import FeedbackRepository


@dataclass(slots=True)
class SubmitFeedback:
    """Persist a learner's problem report or feature request. Open to every
    signed-in learner (free and Pro); not gated."""

    repo: FeedbackRepository

    async def execute(
        self,
        *,
        user_id: UUID,
        kind: FeedbackKind,
        message: str,
        course_id: str | None = None,
        lesson_id: str | None = None,
        app_version: str | None = None,
        platform: str | None = None,
    ) -> Feedback:
        candidate = new_feedback(
            user_id=user_id,
            kind=kind,
            message=message,
            course_id=course_id,
            lesson_id=lesson_id,
            app_version=app_version,
            platform=platform,
        )
        return await self.repo.add(candidate)


@dataclass(slots=True)
class ListFeedback:
    """Admin triage list, newest first, optionally filtered by kind/status."""

    repo: FeedbackRepository

    async def execute(
        self,
        *,
        kind: FeedbackKind | None = None,
        status: FeedbackStatus | None = None,
    ) -> list[Feedback]:
        return await self.repo.list_all(kind=kind, status=status)
