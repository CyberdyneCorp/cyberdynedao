"""Quota meters, policies, and period maths for server-side enforcement.

DAO serves the token/compute-heavy features (AI tutor chat, code execution,
Scan-to-Learn), so it enforces the free-tier caps and Pro fair-use soft caps
server-side regardless of what the client displays (issue #230). The `pro`
entitlement itself is owned by CyberdyneAuth; DAO only reads it.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum


class QuotaMeter(StrEnum):
    """A metered resource DAO serves."""

    TUTOR_MESSAGES = "tutor_messages"  # /api/v1/chat/* turns
    CODE_RUNS = "code_runs"  # /api/v1/lessons/{id}/code/run
    SCANS = "scans"  # Scan-to-Learn (issue #231)


class QuotaPeriod(StrEnum):
    DAILY = "daily"
    MONTHLY = "monthly"


@dataclass(frozen=True, slots=True)
class MeterPolicy:
    """Caps for one meter. ``free_limit`` blocks non-Pro users (402);
    ``pro_limit`` is the Pro fair-use soft cap (429), or ``None`` when Pro is
    effectively unlimited for this meter."""

    period: QuotaPeriod
    free_limit: int
    pro_limit: int | None


# Free-tier caps + Pro fair-use soft caps (issue #230). Code runs are
# unlimited for Pro (no soft cap specified); tutor messages and scans carry
# Pro soft caps to protect token cost on "unlimited".
METER_POLICIES: dict[QuotaMeter, MeterPolicy] = {
    QuotaMeter.TUTOR_MESSAGES: MeterPolicy(QuotaPeriod.MONTHLY, free_limit=10, pro_limit=500),
    QuotaMeter.CODE_RUNS: MeterPolicy(QuotaPeriod.DAILY, free_limit=20, pro_limit=None),
    QuotaMeter.SCANS: MeterPolicy(QuotaPeriod.MONTHLY, free_limit=5, pro_limit=200),
}


def policy_for(meter: QuotaMeter) -> MeterPolicy:
    return METER_POLICIES[meter]


def period_key(period: QuotaPeriod, now: datetime) -> str:
    """Stable counter bucket key for the period containing ``now`` (UTC)."""
    moment = now.astimezone(UTC)
    if period is QuotaPeriod.DAILY:
        return moment.strftime("%Y-%m-%d")
    return moment.strftime("%Y-%m")


def period_reset(period: QuotaPeriod, now: datetime) -> datetime:
    """Start of the next period (UTC) — when the counter resets."""
    moment = now.astimezone(UTC)
    if period is QuotaPeriod.DAILY:
        start_of_day = moment.replace(hour=0, minute=0, second=0, microsecond=0)
        return start_of_day + timedelta(days=1)
    start_of_month = moment.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return _add_month(start_of_month)


def _add_month(start_of_month: datetime) -> datetime:
    if start_of_month.month == 12:
        return start_of_month.replace(year=start_of_month.year + 1, month=1)
    return start_of_month.replace(month=start_of_month.month + 1)


@dataclass(frozen=True, slots=True)
class QuotaDecision:
    """Outcome of an allowed quota check, for surfacing remaining/limit/reset
    so the client can render a quota meter. ``limit``/``remaining`` are
    ``None`` when the meter is unlimited for this user (Pro, no soft cap)."""

    meter: QuotaMeter
    is_pro: bool
    limit: int | None
    remaining: int | None
    reset_at: datetime
