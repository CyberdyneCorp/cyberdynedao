"""Enrollment deadline status.

A deadline is a ``due_at`` instant on an enrollment. The status the UI
shows is derived purely from ``due_at`` relative to *now*:

  * ``none``     — no deadline set
  * ``overdue``  — the due date has passed
  * ``urgent``   — due within ``urgent_within_days`` (default 3)
  * ``upcoming`` — due further out

Pure domain: a function over (due_at, now) plus a small value object. The
``days_remaining`` field is negative once overdue.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum

URGENT_WITHIN_DAYS = 3


class DeadlineStatus(StrEnum):
    NONE = "none"
    UPCOMING = "upcoming"
    URGENT = "urgent"
    OVERDUE = "overdue"


def deadline_status(
    due_at: datetime | None,
    *,
    now: datetime,
    urgent_within_days: int = URGENT_WITHIN_DAYS,
) -> DeadlineStatus:
    if due_at is None:
        return DeadlineStatus.NONE
    if due_at <= now:
        return DeadlineStatus.OVERDUE
    if due_at - now <= timedelta(days=urgent_within_days):
        return DeadlineStatus.URGENT
    return DeadlineStatus.UPCOMING


def days_remaining(due_at: datetime | None, *, now: datetime) -> int | None:
    """Whole days until ``due_at`` (negative if overdue, None if unset).

    Rounds away from now, so any remaining fraction counts as a day:
    1h out -> ``1``, 25h out -> ``2``; 1h overdue -> ``-1``."""
    if due_at is None:
        return None
    delta = due_at - now
    if delta.total_seconds() >= 0:
        return math.ceil(delta.total_seconds() / 86400)
    return -math.ceil(-delta.total_seconds() / 86400)


@dataclass(frozen=True, slots=True)
class EnrollmentDeadline:
    path_slug: str
    due_at: datetime | None
    status: DeadlineStatus
    days_remaining: int | None
