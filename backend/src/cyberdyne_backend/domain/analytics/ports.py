"""Ports the analytics context depends on."""

from __future__ import annotations

from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.analytics.entities import LearnerCounts, PlatformCounts


@runtime_checkable
class AnalyticsRepository(Protocol):
    async def learner_counts(self, user_id: UUID) -> LearnerCounts:
        """Raw per-user aggregates (enrollments, module progress, quiz
        attempts, certificates) for the learner dashboard."""
        ...

    async def platform_counts(self) -> PlatformCounts:
        """Raw platform-wide aggregates for the admin overview."""
        ...
