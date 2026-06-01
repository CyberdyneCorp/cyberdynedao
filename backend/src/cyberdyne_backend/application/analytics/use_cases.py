"""Use cases for the analytics context."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from cyberdyne_backend.domain.analytics import (
    AdminOverview,
    AnalyticsRepository,
    LearnerDashboard,
    build_admin_overview,
    build_learner_dashboard,
)


@dataclass(slots=True)
class GetLearnerDashboard:
    """A signed-in learner's own dashboard."""

    repo: AnalyticsRepository

    async def execute(self, user_id: UUID) -> LearnerDashboard:
        counts = await self.repo.learner_counts(user_id)
        return build_learner_dashboard(counts)


@dataclass(slots=True)
class GetAdminOverview:
    """Platform-wide KPIs for the admin dashboard."""

    repo: AnalyticsRepository

    async def execute(self) -> AdminOverview:
        counts = await self.repo.platform_counts()
        return build_admin_overview(counts)


__all__ = [
    "GetAdminOverview",
    "GetLearnerDashboard",
]
