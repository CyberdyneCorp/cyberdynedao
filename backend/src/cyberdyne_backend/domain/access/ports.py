"""Ports for the access-tier context."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from cyberdyne_backend.domain.access.entities import WalletAccess


@runtime_checkable
class AccessReaderPort(Protocol):
    """Reads the aggregated CyberdyneAccessNFT capabilities for an address.

    Implementations may cache; callers pass an already-normalized
    (lower-cased, validated) address. A read failure should raise
    ``AccessReadError``.
    """

    async def read_access(self, address: str) -> WalletAccess: ...
