"""Activity bounded context.

Lightweight per-user activity events backing the redesigned Profile/Today
learner metrics: study streak plus activity counts (labs/code runs,
simulations, concepts mastered). See issue #164. Streak + counts are
derived in the domain; the repository only stores and returns raw events.
"""

from cyberdyne_backend.domain.activity.entities import (
    ActivityEvent,
    ActivityKind,
    LearnerStats,
    build_learner_stats,
    compute_streaks,
    new_activity_event,
    parse_activity_kind,
)
from cyberdyne_backend.domain.activity.errors import InvalidActivityKindError
from cyberdyne_backend.domain.activity.ports import ActivityRepository

__all__ = [
    "ActivityEvent",
    "ActivityKind",
    "ActivityRepository",
    "InvalidActivityKindError",
    "LearnerStats",
    "build_learner_stats",
    "compute_streaks",
    "new_activity_event",
    "parse_activity_kind",
]
