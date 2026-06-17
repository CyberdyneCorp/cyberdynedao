"""Achievements domain — badges with deterministic award rules (#163).

An *achievement* is a static definition (key, title, icon, …) bound to a
single learner *metric* and a *target*. A learner has earned it once
their metric value reaches the target; progress toward unearned ones is
``min(current, target) / target``.

Award rules are deterministic and live entirely in ``ACHIEVEMENTS`` so
they're documented in one place. Metric values are supplied by a reader
(counts across courses/quizzes/certificates/modules); ``earned_at`` is
recorded the first time an achievement is observed earned, so it's stable
across reads.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class AchievementMetric(StrEnum):
    """The learner signal an achievement tracks."""

    COURSES_COMPLETED = "courses_completed"
    QUIZZES_PASSED = "quizzes_passed"
    PERFECT_QUIZZES = "perfect_quizzes"
    CERTIFICATES_EARNED = "certificates_earned"
    MODULES_COMPLETED = "modules_completed"


@dataclass(frozen=True, slots=True)
class AchievementDefinition:
    key: str
    title: str
    description: str
    icon: str
    metric: AchievementMetric
    target: int


# The full catalogue. Order is the display order. Deterministic + the one
# documented place award rules live.
ACHIEVEMENTS: tuple[AchievementDefinition, ...] = (
    AchievementDefinition(
        "first_course",
        "First Steps",
        "Complete your first course.",
        "🎓",
        AchievementMetric.COURSES_COMPLETED,
        1,
    ),
    AchievementDefinition(
        "five_courses",
        "Getting Serious",
        "Complete five courses.",
        "📚",
        AchievementMetric.COURSES_COMPLETED,
        5,
    ),
    AchievementDefinition(
        "ten_courses",
        "Dedicated Learner",
        "Complete ten courses.",
        "🏅",
        AchievementMetric.COURSES_COMPLETED,
        10,
    ),
    AchievementDefinition(
        "first_quiz",
        "Quiz Rookie",
        "Pass your first quiz.",
        "✅",
        AchievementMetric.QUIZZES_PASSED,
        1,
    ),
    AchievementDefinition(
        "quiz_master",
        "Quiz Master",
        "Pass ten quizzes.",
        "🧠",
        AchievementMetric.QUIZZES_PASSED,
        10,
    ),
    AchievementDefinition(
        "perfectionist",
        "Perfectionist",
        "Score 100% on five quizzes.",
        "💯",
        AchievementMetric.PERFECT_QUIZZES,
        5,
    ),
    AchievementDefinition(
        "first_certificate",
        "Certified",
        "Earn your first certificate.",
        "📜",
        AchievementMetric.CERTIFICATES_EARNED,
        1,
    ),
    AchievementDefinition(
        "scholar",
        "Scholar",
        "Earn five certificates.",
        "🏆",
        AchievementMetric.CERTIFICATES_EARNED,
        5,
    ),
    AchievementDefinition(
        "module_explorer",
        "Module Explorer",
        "Complete five modules.",
        "🧩",
        AchievementMetric.MODULES_COMPLETED,
        5,
    ),
)


@dataclass(frozen=True, slots=True)
class LearnerMetrics:
    """A learner's current value for every tracked metric."""

    courses_completed: int = 0
    quizzes_passed: int = 0
    perfect_quizzes: int = 0
    certificates_earned: int = 0
    modules_completed: int = 0

    def value(self, metric: AchievementMetric) -> int:
        return {
            AchievementMetric.COURSES_COMPLETED: self.courses_completed,
            AchievementMetric.QUIZZES_PASSED: self.quizzes_passed,
            AchievementMetric.PERFECT_QUIZZES: self.perfect_quizzes,
            AchievementMetric.CERTIFICATES_EARNED: self.certificates_earned,
            AchievementMetric.MODULES_COMPLETED: self.modules_completed,
        }[metric]


@dataclass(frozen=True, slots=True)
class AchievementStatus:
    definition: AchievementDefinition
    current: int  # capped at target for display
    earned_at: datetime | None  # set iff earned


def build_achievements(
    metrics: LearnerMetrics,
    earned_at_by_key: dict[str, datetime],
    *,
    now: datetime,
) -> tuple[list[AchievementStatus], list[str]]:
    """Compute each achievement's status from current metrics + the
    already-recorded earn times.

    Returns ``(statuses, newly_earned_keys)``. A newly-earned achievement
    gets ``earned_at = now`` and its key is reported so the caller can
    persist it (making the timestamp stable on later reads).
    """
    statuses: list[AchievementStatus] = []
    newly_earned: list[str] = []
    for definition in ACHIEVEMENTS:
        raw = metrics.value(definition.metric)
        is_earned = raw >= definition.target
        earned_at = earned_at_by_key.get(definition.key)
        if is_earned and earned_at is None:
            earned_at = now
            newly_earned.append(definition.key)
        statuses.append(
            AchievementStatus(
                definition=definition,
                current=min(raw, definition.target),
                earned_at=earned_at if is_earned else None,
            )
        )
    return statuses, newly_earned
