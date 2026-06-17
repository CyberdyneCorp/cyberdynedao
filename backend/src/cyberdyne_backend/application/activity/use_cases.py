"""Use cases for learner activity + derived stats (issue #164)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import UUID

from cyberdyne_backend.domain.activity import (
    ActivityEvent,
    ActivityKind,
    ActivityRepository,
    LearnerStats,
    build_learner_stats,
    new_activity_event,
)

# Clamp the supplied timezone offset to the real-world range
# (UTC-12:00 .. UTC+14:00) so a bogus value can't shift day buckets wildly.
_MIN_TZ_OFFSET = -12 * 60
_MAX_TZ_OFFSET = 14 * 60


@dataclass(slots=True)
class RecordActivity:
    repo: ActivityRepository

    async def execute(
        self, *, user_id: UUID, kind: ActivityKind, ref: str | None = None
    ) -> ActivityEvent:
        event = new_activity_event(user_id=user_id, kind=kind, ref=ref)
        return await self.repo.record(event)


@dataclass(slots=True)
class GetLearnerStats:
    repo: ActivityRepository

    async def execute(self, user_id: UUID, *, tz_offset_minutes: int = 0) -> LearnerStats:
        offset = max(_MIN_TZ_OFFSET, min(tz_offset_minutes, _MAX_TZ_OFFSET))
        events = await self.repo.list_for_user(user_id)
        today = (datetime.now(tz=UTC) + timedelta(minutes=offset)).date()
        return build_learner_stats(events, today=today, tz_offset_minutes=offset)
