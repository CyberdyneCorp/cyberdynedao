"""Unit tests for quota / Pro fair-use enforcement (issue #230)."""

from __future__ import annotations

import asyncio
import uuid
from datetime import UTC, datetime

import pytest

from cyberdyne_backend.application.quota import EnforceQuota
from cyberdyne_backend.domain.quota import (
    FairUseThrottledError,
    FreeQuotaExceededError,
    QuotaMeter,
    QuotaPeriod,
    period_key,
    period_reset,
)

pytestmark = pytest.mark.unit


class _FakeCounters:
    def __init__(self) -> None:
        self.counts: dict[tuple, int] = {}

    async def current(self, *, user_id, meter, period_key) -> int:
        return self.counts.get((user_id, meter.value, period_key), 0)

    async def increment(self, *, user_id, meter, period_key) -> int:
        key = (user_id, meter.value, period_key)
        self.counts[key] = self.counts.get(key, 0) + 1
        return self.counts[key]

    async def reset(self, *, user_id, meter, period_key) -> int:
        return 1 if self.counts.pop((user_id, meter.value, period_key), None) is not None else 0


_FIXED = datetime(2026, 6, 15, 12, 0, tzinfo=UTC)


def _enforcer(repo: _FakeCounters, now: datetime = _FIXED) -> EnforceQuota:
    return EnforceQuota(repo=repo, now=lambda: now)


def test_free_user_allowed_up_to_cap_then_402() -> None:
    repo = _FakeCounters()
    uc = _enforcer(repo)
    uid = uuid.uuid4()
    # 10 free tutor messages allowed.
    for i in range(10):
        decision = asyncio.run(
            uc.execute(user_id=uid, meter=QuotaMeter.TUTOR_MESSAGES, is_pro=False)
        )
        assert decision.limit == 10
        assert decision.remaining == 10 - (i + 1)
    # 11th is blocked with a paywall signal + reset window.
    with pytest.raises(FreeQuotaExceededError) as exc:
        asyncio.run(uc.execute(user_id=uid, meter=QuotaMeter.TUTOR_MESSAGES, is_pro=False))
    assert exc.value.limit == 10
    assert exc.value.reset_at == datetime(2026, 7, 1, tzinfo=UTC)


def test_blocked_request_does_not_consume_quota() -> None:
    repo = _FakeCounters()
    uid = uuid.uuid4()
    repo.counts[(uid, "scans", "2026-06")] = 5  # already at the free cap (5)
    uc = _enforcer(repo)
    with pytest.raises(FreeQuotaExceededError):
        asyncio.run(uc.execute(user_id=uid, meter=QuotaMeter.SCANS, is_pro=False))
    assert repo.counts[(uid, "scans", "2026-06")] == 5  # unchanged — not charged


def test_pro_user_throttled_at_soft_cap_429() -> None:
    repo = _FakeCounters()
    uid = uuid.uuid4()
    repo.counts[(uid, "tutor_messages", "2026-06")] = 500  # at the Pro soft cap
    uc = _enforcer(repo)
    with pytest.raises(FairUseThrottledError) as exc:
        asyncio.run(uc.execute(user_id=uid, meter=QuotaMeter.TUTOR_MESSAGES, is_pro=True))
    assert exc.value.limit == 500


def test_pro_user_unlimited_for_code_runs() -> None:
    # Code runs have no Pro soft cap → always allowed, no remaining reported.
    repo = _FakeCounters()
    uid = uuid.uuid4()
    repo.counts[(uid, "code_runs", "2026-06-15")] = 10_000
    uc = _enforcer(repo)
    decision = asyncio.run(uc.execute(user_id=uid, meter=QuotaMeter.CODE_RUNS, is_pro=True))
    assert decision.limit is None
    assert decision.remaining is None


def test_free_code_runs_are_daily() -> None:
    repo = _FakeCounters()
    uid = uuid.uuid4()
    uc = _enforcer(repo)
    for _ in range(20):
        asyncio.run(uc.execute(user_id=uid, meter=QuotaMeter.CODE_RUNS, is_pro=False))
    with pytest.raises(FreeQuotaExceededError) as exc:
        asyncio.run(uc.execute(user_id=uid, meter=QuotaMeter.CODE_RUNS, is_pro=False))
    assert exc.value.reset_at == datetime(2026, 6, 16, tzinfo=UTC)  # next day


def test_period_key_and_reset() -> None:
    assert period_key(QuotaPeriod.MONTHLY, _FIXED) == "2026-06"
    assert period_key(QuotaPeriod.DAILY, _FIXED) == "2026-06-15"
    assert period_reset(QuotaPeriod.MONTHLY, _FIXED) == datetime(2026, 7, 1, tzinfo=UTC)
    assert period_reset(QuotaPeriod.DAILY, _FIXED) == datetime(2026, 6, 16, tzinfo=UTC)
    # December rolls over to January of the next year.
    december = datetime(2026, 12, 20, 9, 0, tzinfo=UTC)
    assert period_reset(QuotaPeriod.MONTHLY, december) == datetime(2027, 1, 1, tzinfo=UTC)


# ── Free-limit override (env-configurable caps) ──────────────────────


def test_free_limit_override_raises_cap() -> None:
    repo = _FakeCounters()
    enforcer = EnforceQuota(
        repo=repo, free_limits={QuotaMeter.TUTOR_MESSAGES: 3}, now=lambda: _FIXED
    )
    user = uuid.uuid4()

    async def run() -> None:
        # Default is 10; override to 3 → allowed 3 times, then 402.
        for _ in range(3):
            await enforcer.execute(user_id=user, meter=QuotaMeter.TUTOR_MESSAGES, is_pro=False)
        with pytest.raises(FreeQuotaExceededError) as exc:
            await enforcer.execute(user_id=user, meter=QuotaMeter.TUTOR_MESSAGES, is_pro=False)
        assert exc.value.limit == 3

    asyncio.run(run())


def test_override_only_affects_named_meter() -> None:
    repo = _FakeCounters()
    enforcer = EnforceQuota(
        repo=repo, free_limits={QuotaMeter.TUTOR_MESSAGES: 1}, now=lambda: _FIXED
    )
    user = uuid.uuid4()

    async def run() -> None:
        # scans keeps its built-in free cap (5) — override didn't touch it.
        dec = await enforcer.execute(user_id=user, meter=QuotaMeter.SCANS, is_pro=False)
        assert dec.limit == 5

    asyncio.run(run())


# ── ResetQuota (admin) ───────────────────────────────────────────────


def test_reset_one_meter_clears_usage() -> None:
    from cyberdyne_backend.application.quota import ResetQuota

    repo = _FakeCounters()
    enforcer = _enforcer(repo)
    resetter = ResetQuota(repo=repo, now=lambda: _FIXED)
    user = uuid.uuid4()

    async def run() -> None:
        for _ in range(10):
            await enforcer.execute(user_id=user, meter=QuotaMeter.TUTOR_MESSAGES, is_pro=False)
        with pytest.raises(FreeQuotaExceededError):
            await enforcer.execute(user_id=user, meter=QuotaMeter.TUTOR_MESSAGES, is_pro=False)

        reset = await resetter.execute(user_id=user, meter=QuotaMeter.TUTOR_MESSAGES)
        assert reset == [QuotaMeter.TUTOR_MESSAGES]

        # Usable again after reset.
        dec = await enforcer.execute(user_id=user, meter=QuotaMeter.TUTOR_MESSAGES, is_pro=False)
        assert dec.remaining == 9

    asyncio.run(run())


def test_reset_all_meters_reports_only_those_with_usage() -> None:
    from cyberdyne_backend.application.quota import ResetQuota

    repo = _FakeCounters()
    enforcer = _enforcer(repo)
    resetter = ResetQuota(repo=repo, now=lambda: _FIXED)
    user = uuid.uuid4()

    async def run() -> None:
        await enforcer.execute(user_id=user, meter=QuotaMeter.TUTOR_MESSAGES, is_pro=False)
        # No scans/code_runs used → only tutor_messages is reported reset.
        reset = await resetter.execute(user_id=user)
        assert reset == [QuotaMeter.TUTOR_MESSAGES]

    asyncio.run(run())


def test_reset_noop_when_nothing_used() -> None:
    from cyberdyne_backend.application.quota import ResetQuota

    resetter = ResetQuota(repo=_FakeCounters(), now=lambda: _FIXED)

    async def run() -> None:
        assert await resetter.execute(user_id=uuid.uuid4()) == []

    asyncio.run(run())
