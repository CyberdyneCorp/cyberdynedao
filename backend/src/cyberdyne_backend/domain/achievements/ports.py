"""Ports for the achievements context."""

from __future__ import annotations

from datetime import datetime
from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.achievements.entities import LearnerMetrics


@runtime_checkable
class AchievementMetricsReader(Protocol):
    async def compute(self, user_id: UUID) -> LearnerMetrics:
        """Current metric values for the learner, aggregated across the
        courses/quizzes/learning contexts. Read-only."""
        ...


@runtime_checkable
class AchievementRepository(Protocol):
    async def list_earned(self, user_id: UUID) -> dict[str, datetime]:
        """Already-earned achievement keys → the time they were earned."""
        ...

    async def record_earned(self, *, user_id: UUID, key: str, earned_at: datetime) -> None:
        """Persist a newly-earned achievement. Idempotent on
        ``(user_id, key)`` — a second call for the same pair is a no-op,
        so the original ``earned_at`` is preserved."""
        ...
