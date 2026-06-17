"""Repository port for the activity context."""

from __future__ import annotations

from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.activity.entities import ActivityEvent


@runtime_checkable
class ActivityRepository(Protocol):
    async def record(self, event: ActivityEvent) -> ActivityEvent:
        """Persist an activity event and return it."""
        ...

    async def list_for_user(self, user_id: UUID) -> list[ActivityEvent]:
        """Every recorded event for a user. Streak + counts are derived in
        the domain, so the adapter just returns the rows."""
        ...
