"""Unit tests for the DAO treasury snapshot prewarmer (issue #7)."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime

import pytest

from cyberdyne_backend.application.dao_treasury import TreasurySnapshotPrewarmer
from cyberdyne_backend.domain.dao_treasury.entities import TreasurySnapshot

pytestmark = pytest.mark.unit

_ADDR = "0xABCdef0000000000000000000000000000000001"


def _snapshot() -> TreasurySnapshot:
    return TreasurySnapshot(
        treasury_address=_ADDR,
        chain_id=8453,
        snapshot_at=datetime(2026, 6, 17, tzinfo=UTC),
        token_balances=(),
        aave_positions=(),
        uniswap_positions=(),
    )


class _CountingReader:
    def __init__(self) -> None:
        self.calls: list[str] = []

    async def read_snapshot(self, treasury_address: str) -> TreasurySnapshot:
        self.calls.append(treasury_address)
        return _snapshot()


class _FailingReader:
    async def read_snapshot(self, treasury_address: str) -> TreasurySnapshot:
        raise RuntimeError("rpc down")


class TestRefreshOnce:
    async def test_warms_cache_and_reports_success(self) -> None:
        reader = _CountingReader()
        pw = TreasurySnapshotPrewarmer(reader=reader, treasury_address=_ADDR, interval_s=300)
        assert await pw.refresh_once() is True
        assert reader.calls == [_ADDR]

    async def test_swallows_read_failure(self) -> None:
        # Regression: a transient RPC error must not kill the loop.
        pw = TreasurySnapshotPrewarmer(
            reader=_FailingReader(), treasury_address=_ADDR, interval_s=5
        )
        assert await pw.refresh_once() is False  # no raise


class TestRunForever:
    async def test_warms_then_sleeps_and_cancel_propagates(self, monkeypatch) -> None:
        reader = _CountingReader()
        pw = TreasurySnapshotPrewarmer(reader=reader, treasury_address=_ADDR, interval_s=300)

        slept: list[float] = []

        async def fake_sleep(seconds: float) -> None:
            slept.append(seconds)
            raise asyncio.CancelledError  # break the loop after the first cycle

        monkeypatch.setattr(asyncio, "sleep", fake_sleep)

        with pytest.raises(asyncio.CancelledError):
            await pw.run_forever()

        # Warmed once up front, then slept for the configured interval.
        assert reader.calls == [_ADDR]
        assert slept == [300]
