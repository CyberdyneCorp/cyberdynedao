"""Tests for the DAO treasury domain + use case + caching reader."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from decimal import Decimal

import pytest

from cyberdyne_backend.adapters.outbound.chain.caching_reader import CachingChainReader
from cyberdyne_backend.adapters.outbound.chain.fake_reader import FakeChainReader
from cyberdyne_backend.application.dao_treasury import GetDaoOverview
from cyberdyne_backend.domain.dao_treasury import (
    AaveReservePosition,
    TokenBalance,
    TreasurySnapshot,
    TreasuryUnconfiguredError,
    UniswapV4Position,
)


def _snapshot(addr: str = "0xabc") -> TreasurySnapshot:
    return TreasurySnapshot(
        treasury_address=addr,
        chain_id=8453,
        snapshot_at=datetime(2026, 1, 1, tzinfo=UTC),
        token_balances=(
            TokenBalance(
                symbol="USDC",
                name="USD Coin",
                address="0xabc",
                balance=Decimal("100"),
                usd_value=Decimal("100"),
                change_24h_pct=Decimal("0"),
            ),
        ),
        aave_positions=(
            AaveReservePosition(
                symbol="USDC",
                a_token_balance=Decimal("50"),
                variable_debt=Decimal("0"),
                supply_apy=Decimal("0.04"),
                borrow_apy=Decimal("0.06"),
                usd_value_supplied=Decimal("50"),
                usd_value_borrowed=Decimal("0"),
            ),
        ),
        uniswap_positions=(
            UniswapV4Position(
                position_id="1",
                pool_id="p",
                token0_symbol="USDC",
                token1_symbol="WETH",
                token0_amount=Decimal("1000"),
                token1_amount=Decimal("0.3"),
                fee_tier_bps=30,
                tick_lower=-100,
                tick_upper=100,
                in_range=True,
                usd_value=Decimal("25"),
                uncollected_fees_usd=Decimal("0"),
            ),
        ),
    )


class TestTreasurySnapshotTotal:
    def test_sums_tokens_aave_uniswap(self) -> None:
        snap = _snapshot()
        # tokens 100 + aave (50 - 0) + uniswap 25 = 175
        assert snap.total_usd_value == Decimal("175")

    def test_uses_decimal_arithmetic(self) -> None:
        snap = _snapshot()
        # Float drift would put this near 175.00000000001; Decimal is exact.
        assert isinstance(snap.total_usd_value, Decimal)


class _CountingReader:
    def __init__(self) -> None:
        self.calls = 0

    async def read_snapshot(self, treasury_address: str) -> TreasurySnapshot:
        self.calls += 1
        return _snapshot(treasury_address)


class TestCachingChainReader:
    async def test_caches_within_ttl(self) -> None:
        inner = _CountingReader()
        cached = CachingChainReader(inner=inner, ttl_s=60)
        await cached.read_snapshot("0xabc")
        await cached.read_snapshot("0xabc")
        assert inner.calls == 1

    async def test_coalesces_concurrent_calls(self) -> None:
        slow = _SlowReader()
        cached = CachingChainReader(inner=slow, ttl_s=60)
        results = await asyncio.gather(
            cached.read_snapshot("0xabc"),
            cached.read_snapshot("0xabc"),
            cached.read_snapshot("0xabc"),
        )
        assert slow.calls == 1
        assert {r.treasury_address for r in results} == {"0xabc"}

    async def test_invalidate_clears_cache(self) -> None:
        inner = _CountingReader()
        cached = CachingChainReader(inner=inner, ttl_s=60)
        await cached.read_snapshot("0xabc")
        cached.invalidate("0xabc")
        await cached.read_snapshot("0xabc")
        assert inner.calls == 2

    async def test_invalidate_all(self) -> None:
        inner = _CountingReader()
        cached = CachingChainReader(inner=inner, ttl_s=60)
        await cached.read_snapshot("0xabc")
        await cached.read_snapshot("0xdef")
        cached.invalidate()
        await cached.read_snapshot("0xabc")
        assert inner.calls == 3

    def test_rejects_zero_ttl(self) -> None:
        with pytest.raises(ValueError):
            CachingChainReader(inner=_CountingReader(), ttl_s=0)


class _SlowReader:
    def __init__(self) -> None:
        self.calls = 0

    async def read_snapshot(self, treasury_address: str) -> TreasurySnapshot:
        self.calls += 1
        await asyncio.sleep(0)
        return _snapshot(treasury_address)


class TestFakeChainReader:
    async def test_returns_stable_shape(self) -> None:
        reader = FakeChainReader()
        snap = await reader.read_snapshot("0xtreasury")
        assert snap.treasury_address == "0xtreasury"
        assert snap.chain_id == 8453
        assert len(snap.token_balances) > 0
        assert len(snap.aave_positions) > 0
        assert len(snap.uniswap_positions) > 0


class TestGetDaoOverview:
    async def test_returns_snapshot_when_configured(self) -> None:
        uc = GetDaoOverview(
            reader=FakeChainReader(), treasury_address="0xabc", holders=42
        )
        overview = await uc.execute()
        assert overview.snapshot.treasury_address == "0xabc"
        assert overview.holders == 42

    async def test_unconfigured_raises(self) -> None:
        uc = GetDaoOverview(reader=FakeChainReader(), treasury_address=None)
        with pytest.raises(TreasuryUnconfiguredError):
            await uc.execute()
