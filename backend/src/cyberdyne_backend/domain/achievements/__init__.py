"""Achievements bounded context.

Badges/achievements (earned + in-progress) with deterministic award
rules, surfaced on the Profile Achievements screen. See issue #163.
"""

from cyberdyne_backend.domain.achievements.entities import (
    ACHIEVEMENTS,
    AchievementDefinition,
    AchievementMetric,
    AchievementStatus,
    LearnerMetrics,
    build_achievements,
)
from cyberdyne_backend.domain.achievements.ports import (
    AchievementMetricsReader,
    AchievementRepository,
)

__all__ = [
    "ACHIEVEMENTS",
    "AchievementDefinition",
    "AchievementMetric",
    "AchievementMetricsReader",
    "AchievementRepository",
    "AchievementStatus",
    "LearnerMetrics",
    "build_achievements",
]
