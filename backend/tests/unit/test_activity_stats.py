"""Unit tests for streak/stats derivation + use cases (issue #164)."""

from __future__ import annotations

import asyncio
import uuid
from datetime import UTC, date, datetime, timedelta

from cyberdyne_backend.application.activity import GetLearnerStats, RecordActivity
from cyberdyne_backend.domain.activity import (
    ActivityEvent,
    ActivityKind,
    build_learner_stats,
    compute_streaks,
    new_activity_event,
)


def _d(y: int, m: int, day: int) -> date:
    return date(y, m, day)


def test_compute_streaks_empty() -> None:
    assert compute_streaks(set(), today=_d(2026, 6, 17)) == (0, 0)


def test_current_streak_counts_back_from_today() -> None:
    days = {_d(2026, 6, 15), _d(2026, 6, 16), _d(2026, 6, 17)}
    current, longest = compute_streaks(days, today=_d(2026, 6, 17))
    assert current == 3
    assert longest == 3


def test_current_streak_grace_for_not_yet_today() -> None:
    # No activity today, but yesterday + the day before — streak holds.
    days = {_d(2026, 6, 15), _d(2026, 6, 16)}
    current, _ = compute_streaks(days, today=_d(2026, 6, 17))
    assert current == 2


def test_current_streak_breaks_after_a_missed_day() -> None:
    days = {_d(2026, 6, 13), _d(2026, 6, 14)}  # gap before today
    current, longest = compute_streaks(days, today=_d(2026, 6, 17))
    assert current == 0
    assert longest == 2


def test_longest_streak_spans_history() -> None:
    days = {
        _d(2026, 6, 1),
        _d(2026, 6, 2),
        _d(2026, 6, 3),
        _d(2026, 6, 4),  # run of 4
        _d(2026, 6, 10),  # isolated
        _d(2026, 6, 17),  # today only
    }
    current, longest = compute_streaks(days, today=_d(2026, 6, 17))
    assert current == 1
    assert longest == 4


def _evt(kind: ActivityKind, day: int, ref: str | None = None) -> ActivityEvent:
    return ActivityEvent(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        kind=kind,
        ref=ref,
        occurred_at=datetime(2026, 6, day, 12, 0, tzinfo=UTC),
    )


def test_build_stats_counts_and_distinct_concepts() -> None:
    events = [
        _evt(ActivityKind.CODE_RUN, 16),
        _evt(ActivityKind.CODE_RUN, 17),
        _evt(ActivityKind.SIMULATION_RUN, 17),
        _evt(ActivityKind.CONCEPT_MASTERED, 17, ref="ohms-law"),
        _evt(ActivityKind.CONCEPT_MASTERED, 17, ref="ohms-law"),  # dup, not counted
        _evt(ActivityKind.CONCEPT_MASTERED, 17, ref="kvl"),
    ]
    stats = build_learner_stats(events, today=_d(2026, 6, 17))
    assert stats.code_runs_count == 2
    assert stats.simulations_run == 1
    assert stats.concepts_mastered == 2  # distinct refs
    assert stats.current_streak_days == 2  # 16 + 17
    assert stats.last_active_on == _d(2026, 6, 17)


def test_tz_offset_shifts_day_bucket() -> None:
    # 23:30 UTC on the 16th is already the 17th at UTC+1 (60 min).
    late = ActivityEvent(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        kind=ActivityKind.LESSON_VIEWED,
        ref=None,
        occurred_at=datetime(2026, 6, 16, 23, 30, tzinfo=UTC),
    )
    stats = build_learner_stats([late], today=_d(2026, 6, 17), tz_offset_minutes=60)
    assert stats.last_active_on == _d(2026, 6, 17)


class _FakeRepo:
    def __init__(self) -> None:
        self.events: list[ActivityEvent] = []

    async def record(self, event: ActivityEvent) -> ActivityEvent:
        self.events.append(event)
        return event

    async def list_for_user(self, user_id) -> list[ActivityEvent]:
        return [e for e in self.events if e.user_id == user_id]


def test_record_activity_use_case() -> None:
    repo = _FakeRepo()
    user = uuid.uuid4()
    out = asyncio.run(
        RecordActivity(repo=repo).execute(user_id=user, kind=ActivityKind.CODE_RUN, ref="lesson-1")
    )
    assert out.kind is ActivityKind.CODE_RUN
    assert repo.events[0].user_id == user


def test_get_stats_clamps_tz_offset() -> None:
    repo = _FakeRepo()
    user = uuid.uuid4()
    # An out-of-range offset must not raise; it's clamped.
    stats = asyncio.run(GetLearnerStats(repo=repo).execute(user, tz_offset_minutes=99999))
    assert stats.current_streak_days == 0


def test_new_event_defaults_now() -> None:
    before = datetime.now(tz=UTC) - timedelta(seconds=1)
    e = new_activity_event(user_id=uuid.uuid4(), kind=ActivityKind.LESSON_VIEWED)
    assert e.occurred_at >= before
