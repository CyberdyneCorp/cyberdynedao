"""Use cases for achievements (issue #163)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from cyberdyne_backend.domain.achievements import (
    AchievementMetricsReader,
    AchievementRepository,
    AchievementStatus,
    build_achievements,
)


@dataclass(slots=True)
class GetMyAchievements:
    """Earned + in-progress achievements for a learner.

    Award-on-read: any achievement now satisfied but not yet recorded is
    persisted with the current timestamp, so its ``earnedAt`` stays stable
    on subsequent reads. Idempotent — re-reading awards nothing new.
    """

    reader: AchievementMetricsReader
    repo: AchievementRepository

    async def execute(self, user_id: UUID) -> list[AchievementStatus]:
        metrics = await self.reader.compute(user_id)
        earned = await self.repo.list_earned(user_id)
        now = datetime.now(tz=UTC)
        statuses, newly_earned = build_achievements(metrics, earned, now=now)
        for key in newly_earned:
            await self.repo.record_earned(user_id=user_id, key=key, earned_at=now)
        return statuses
