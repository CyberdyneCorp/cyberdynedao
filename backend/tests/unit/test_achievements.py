"""Unit tests for the achievement award engine (issue #163)."""

from __future__ import annotations

import asyncio
import uuid
from datetime import UTC, datetime

from cyberdyne_backend.application.achievements import GetMyAchievements
from cyberdyne_backend.domain.achievements import (
    ACHIEVEMENTS,
    LearnerMetrics,
    build_achievements,
)

_NOW = datetime(2026, 6, 17, 12, 0, tzinfo=UTC)


def _by_key(statuses):
    return {s.definition.key: s for s in statuses}


def test_nothing_earned_for_a_fresh_learner() -> None:
    statuses, newly = build_achievements(LearnerMetrics(), {}, now=_NOW)
    assert newly == []
    assert all(s.earned_at is None for s in statuses)
    # In-progress current values are zero, targets preserved.
    first = _by_key(statuses)["first_course"]
    assert first.current == 0
    assert first.definition.target == 1


def test_threshold_crossing_earns_and_reports_newly() -> None:
    metrics = LearnerMetrics(courses_completed=1, quizzes_passed=1)
    statuses, newly = build_achievements(metrics, {}, now=_NOW)
    by_key = _by_key(statuses)
    assert by_key["first_course"].earned_at == _NOW
    assert by_key["first_quiz"].earned_at == _NOW
    assert set(newly) == {"first_course", "first_quiz"}
    # Higher tiers remain in progress with capped current.
    assert by_key["five_courses"].earned_at is None
    assert by_key["five_courses"].current == 1


def test_existing_earned_at_is_preserved() -> None:
    earlier = datetime(2026, 1, 1, tzinfo=UTC)
    metrics = LearnerMetrics(courses_completed=3)
    statuses, newly = build_achievements(
        metrics, {"first_course": earlier}, now=_NOW
    )
    # first_course keeps its original timestamp; not re-reported as new.
    assert _by_key(statuses)["first_course"].earned_at == earlier
    assert "first_course" not in newly


def test_current_capped_at_target() -> None:
    metrics = LearnerMetrics(courses_completed=99)
    statuses, _ = build_achievements(metrics, {}, now=_NOW)
    five = _by_key(statuses)["five_courses"]
    assert five.current == 5  # capped, not 99
    assert five.earned_at == _NOW


def test_every_definition_has_a_status() -> None:
    statuses, _ = build_achievements(LearnerMetrics(), {}, now=_NOW)
    assert len(statuses) == len(ACHIEVEMENTS)


class _FakeReader:
    def __init__(self, metrics: LearnerMetrics) -> None:
        self._metrics = metrics

    async def compute(self, user_id) -> LearnerMetrics:
        return self._metrics


class _FakeRepo:
    def __init__(self) -> None:
        self.earned: dict[str, datetime] = {}
        self.record_calls = 0

    async def list_earned(self, user_id) -> dict[str, datetime]:
        return dict(self.earned)

    async def record_earned(self, *, user_id, key, earned_at) -> None:
        self.record_calls += 1
        self.earned.setdefault(key, earned_at)


def test_use_case_awards_on_read_then_is_idempotent() -> None:
    reader = _FakeReader(LearnerMetrics(courses_completed=1))
    repo = _FakeRepo()
    uc = GetMyAchievements(reader=reader, repo=repo)
    user = uuid.uuid4()

    first = asyncio.run(uc.execute(user))
    assert repo.record_calls == 1  # first_course persisted
    earned_first = {s.definition.key for s in first if s.earned_at is not None}
    assert earned_first == {"first_course"}

    # Second read awards nothing new.
    asyncio.run(uc.execute(user))
    assert repo.record_calls == 1
