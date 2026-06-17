"""Background prewarm for the DAO treasury snapshot (issue #7).

The ``CachingChainReader`` is lazy: the first request after a TTL expiry
pays the full on-chain read (RPC roundtrip + multicall + price oracle),
and a burst arriving at that moment all wait on the same in-flight fetch.
This long-lived worker keeps the cache warm by re-reading the snapshot on
an interval, so requests are (almost) always served from cache.

Mirrors the academy ``TranslationWorker`` shape: an application-layer loop
that depends only on the domain port, owns no request-scoped state, and is
started/stopped by the app lifespan.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass

from cyberdyne_backend.domain.dao_treasury import ChainReaderPort

logger = logging.getLogger("cyberdyne_backend.dao_treasury.jobs")


@dataclass(slots=True)
class TreasurySnapshotPrewarmer:
    """Periodically reads the treasury snapshot to keep the cache warm."""

    reader: ChainReaderPort
    treasury_address: str
    interval_s: float

    async def refresh_once(self) -> bool:
        """Read the snapshot once (warming the cache). Returns ``True`` on
        success. A transient read failure is logged and swallowed so the
        loop survives — the next request just pays a lazy read. Cancellation
        (``asyncio.CancelledError`` is a ``BaseException``) propagates out."""
        try:
            await self.reader.read_snapshot(self.treasury_address)
        except Exception:
            logger.warning("treasury snapshot prewarm failed; will retry", exc_info=True)
            return False
        return True

    async def run_forever(self) -> None:
        """Warm the cache immediately, then re-warm every ``interval_s``.
        Cancellation (shutdown) propagates out cleanly. The interval should
        be ≤ the cache TTL; a momentary expiry is harmless because reads
        coalesce — at worst one request pays a single lazy fetch."""
        while True:
            await self.refresh_once()
            await asyncio.sleep(self.interval_s)


__all__ = ["TreasurySnapshotPrewarmer"]
