"""Analytics bounded context.

Read-only reporting over the learning, courses, and quiz data: a
per-learner dashboard (enrolments, module progress, quiz performance,
certificates) and a platform-wide admin overview (KPIs, completion +
quiz pass rates). The repository returns raw counts; all derived figures
are computed in the domain. No tables of its own.
"""

from cyberdyne_backend.domain.analytics.entities import (
    AdminOverview,
    LearnerCounts,
    LearnerDashboard,
    PlatformCounts,
    build_admin_overview,
    build_learner_dashboard,
)
from cyberdyne_backend.domain.analytics.ports import (
    AnalyticsRepository,
)

__all__ = [
    "AdminOverview",
    "AnalyticsRepository",
    "LearnerCounts",
    "LearnerDashboard",
    "PlatformCounts",
    "build_admin_overview",
    "build_learner_dashboard",
]
