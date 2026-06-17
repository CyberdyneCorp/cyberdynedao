"""Entities for the activity context — learner activity events + stats.

Records lightweight per-user activity events (a lesson viewed, a code/lab
run, a simulation run, a concept mastered) and derives the streak +
activity counts the redesigned Profile/Today surfaces show. See issue
#164.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from enum import StrEnum
from itertools import pairwise
from uuid import UUID

from cyberdyne_backend.domain.activity.errors import InvalidActivityKindError


class ActivityKind(StrEnum):
    """What a recorded activity event represents."""

    LESSON_VIEWED = "lesson_viewed"
    CODE_RUN = "code_run"
    SIMULATION_RUN = "simulation_run"
    CONCEPT_MASTERED = "concept_mastered"


def parse_activity_kind(raw: str) -> ActivityKind:
    try:
        return ActivityKind(raw)
    except ValueError as exc:
        allowed = ", ".join(k.value for k in ActivityKind)
        raise InvalidActivityKindError(
            f"unknown activity kind {raw!r}; expected one of: {allowed}"
        ) from exc


@dataclass(slots=True)
class ActivityEvent:
    """A single recorded learner activity.

    ``ref`` optionally identifies the subject (e.g. a lesson/concept slug)
    so distinct-subject counts (concepts mastered) don't double-count.
    """

    id: UUID
    user_id: UUID
    kind: ActivityKind
    ref: str | None
    occurred_at: datetime


@dataclass(slots=True)
class LearnerStats:
    """Derived streak + activity counts for one learner."""

    current_streak_days: int
    longest_streak_days: int
    last_active_on: date | None
    code_runs_count: int
    simulations_run: int
    concepts_mastered: int


def new_activity_event(
    *,
    user_id: UUID,
    kind: ActivityKind,
    ref: str | None = None,
    now: datetime | None = None,
) -> ActivityEvent:
    return ActivityEvent(
        id=uuid.uuid4(),
        user_id=user_id,
        kind=kind,
        ref=ref,
        occurred_at=now or datetime.now(tz=UTC),
    )


def _local_day(moment: datetime, tz_offset_minutes: int) -> date:
    """Bucket a UTC instant into a calendar day, shifted by the learner's
    timezone offset (minutes east of UTC). Naive datetimes are treated as
    UTC."""
    aware = moment if moment.tzinfo is not None else moment.replace(tzinfo=UTC)
    return (aware.astimezone(UTC) + timedelta(minutes=tz_offset_minutes)).date()


def compute_streaks(
    active_days: set[date],
    *,
    today: date,
) -> tuple[int, int]:
    """Return ``(current_streak, longest_streak)`` from a set of distinct
    active calendar days.

    The *current* streak counts consecutive days ending on ``today`` (or
    ``today - 1`` if there's no activity yet today, so a streak isn't lost
    until a full day is missed). The *longest* streak is the longest run
    of consecutive days anywhere in the history.
    """
    if not active_days:
        return 0, 0

    # Longest run of consecutive days.
    longest = 1
    run = 1
    ordered = sorted(active_days)
    for prev, cur in pairwise(ordered):
        if cur - prev == timedelta(days=1):
            run += 1
        else:
            run = 1
        longest = max(longest, run)

    # Current streak: walk back from today (grace for "not yet today").
    if today in active_days:
        anchor = today
    elif (today - timedelta(days=1)) in active_days:
        anchor = today - timedelta(days=1)
    else:
        return 0, longest

    current = 0
    cursor = anchor
    while cursor in active_days:
        current += 1
        cursor -= timedelta(days=1)
    return current, longest


def build_learner_stats(
    events: list[ActivityEvent],
    *,
    today: date,
    tz_offset_minutes: int = 0,
) -> LearnerStats:
    """Fold raw events into the derived stats. Pure — the repository
    supplies the events and the (timezone-adjusted) ``today``."""
    active_days = {_local_day(e.occurred_at, tz_offset_minutes) for e in events}
    current, longest = compute_streaks(active_days, today=today)

    code_runs = sum(1 for e in events if e.kind is ActivityKind.CODE_RUN)
    simulations = sum(1 for e in events if e.kind is ActivityKind.SIMULATION_RUN)
    # Distinct subjects so re-mastering a concept doesn't inflate the count;
    # events without a ref each count once.
    mastered_refs: set[str] = set()
    mastered_unkeyed = 0
    for e in events:
        if e.kind is ActivityKind.CONCEPT_MASTERED:
            if e.ref is None:
                mastered_unkeyed += 1
            else:
                mastered_refs.add(e.ref)

    return LearnerStats(
        current_streak_days=current,
        longest_streak_days=longest,
        last_active_on=max(active_days) if active_days else None,
        code_runs_count=code_runs,
        simulations_run=simulations,
        concepts_mastered=len(mastered_refs) + mastered_unkeyed,
    )
