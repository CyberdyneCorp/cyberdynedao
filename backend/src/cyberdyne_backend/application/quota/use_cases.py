"""Quota / fair-use enforcement use case."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from cyberdyne_backend.domain.quota.entities import (
    QuotaDecision,
    QuotaMeter,
    period_key,
    period_reset,
    policy_for,
)
from cyberdyne_backend.domain.quota.errors import (
    FairUseThrottledError,
    FreeQuotaExceededError,
)
from cyberdyne_backend.domain.quota.ports import UsageCounterRepository


def _utcnow() -> datetime:
    return datetime.now(tz=UTC)


@dataclass(slots=True)
class EnforceQuota:
    """Check a user's usage against the meter's cap and, if allowed, consume
    one unit. Raises :class:`FreeQuotaExceededError` (→ 402) for a non-Pro user
    over the free cap, or :class:`FairUseThrottledError` (→ 429) for a Pro user
    over the fair-use soft cap. Returns a :class:`QuotaDecision` with the
    remaining count + reset window when allowed.

    Read-then-increment is intentionally not transactional: per-user counters
    contend rarely, and a tiny overcount under concurrency is acceptable for a
    cost-control cap. Blocked requests do NOT consume quota."""

    repo: UsageCounterRepository
    now: Callable[[], datetime] = field(default=_utcnow)

    async def execute(self, *, user_id: UUID, meter: QuotaMeter, is_pro: bool) -> QuotaDecision:
        policy = policy_for(meter)
        moment = self.now()
        bucket = period_key(policy.period, moment)
        reset_at = period_reset(policy.period, moment)
        limit = policy.pro_limit if is_pro else policy.free_limit

        if limit is None:  # unlimited for this user (Pro, no soft cap)
            await self.repo.increment(user_id=user_id, meter=meter, period_key=bucket)
            return QuotaDecision(
                meter=meter, is_pro=is_pro, limit=None, remaining=None, reset_at=reset_at
            )

        used = await self.repo.current(user_id=user_id, meter=meter, period_key=bucket)
        if used >= limit:
            if is_pro:
                raise FairUseThrottledError(meter, limit, reset_at)
            raise FreeQuotaExceededError(meter, limit, reset_at)

        new_count = await self.repo.increment(user_id=user_id, meter=meter, period_key=bucket)
        return QuotaDecision(
            meter=meter,
            is_pro=is_pro,
            limit=limit,
            remaining=max(0, limit - new_count),
            reset_at=reset_at,
        )
