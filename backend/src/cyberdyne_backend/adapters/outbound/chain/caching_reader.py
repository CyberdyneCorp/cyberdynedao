"""TTL-cached wrapper over a ``ChainReaderPort``.

On-chain reads are expensive (RPC roundtrip + multicall + price oracle
look-ups). The DaoView only needs near-real-time data, so we cache the
last snapshot per treasury address for a few minutes.

Coalesces concurrent reads: if multiple requests arrive while a fetch
is in flight, they all await the same future. Lifted verbatim from the
shape used in ``adapters/outbound/auth/caching_auth_port.py``.
"""

from __future__ import annotations

import asyncio
import time

from cyberdyne_backend.domain.dao_treasury import ChainReaderPort, TreasurySnapshot


class CachingChainReader:
    """Wraps an inner reader with a TTL cache + request coalescing."""

    def __init__(self, *, inner: ChainReaderPort, ttl_s: int) -> None:
        if ttl_s <= 0:
            raise ValueError("ttl_s must be positive")
        self._inner = inner
        self._ttl_s = ttl_s
        self._cache: dict[str, tuple[float, TreasurySnapshot]] = {}
        self._inflight: dict[str, asyncio.Future[TreasurySnapshot]] = {}

    async def read_snapshot(self, treasury_address: str) -> TreasurySnapshot:
        key = treasury_address.lower()
        now = time.monotonic()

        cached = self._cache.get(key)
        if cached is not None and now - cached[0] < self._ttl_s:
            return cached[1]

        existing = self._inflight.get(key)
        if existing is not None:
            return await existing

        loop = asyncio.get_running_loop()
        future: asyncio.Future[TreasurySnapshot] = loop.create_future()
        self._inflight[key] = future
        try:
            snapshot = await self._inner.read_snapshot(treasury_address)
        except BaseException as exc:
            future.set_exception(exc)
            raise
        else:
            self._cache[key] = (now, snapshot)
            future.set_result(snapshot)
            return snapshot
        finally:
            self._inflight.pop(key, None)

    def invalidate(self, treasury_address: str | None = None) -> None:
        """Drop cache. Without an arg drops every entry."""
        if treasury_address is None:
            self._cache.clear()
            return
        self._cache.pop(treasury_address.lower(), None)
