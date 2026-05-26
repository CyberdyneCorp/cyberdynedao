"""Ports for the DAO treasury context."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from cyberdyne_backend.domain.dao_treasury.entities import TreasurySnapshot


@runtime_checkable
class ChainReaderPort(Protocol):
    """Reads on-chain state for a single treasury address.

    Implementations may cache aggressively — RPC calls are slow and
    rate-limited. Callers should treat results as eventually-consistent
    snapshots, not live data.
    """

    async def read_snapshot(self, treasury_address: str) -> TreasurySnapshot: ...
