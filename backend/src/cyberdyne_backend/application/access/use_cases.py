"""Access-tier use cases — read a wallet's aggregated NFT capabilities."""

from __future__ import annotations

from dataclasses import dataclass

from cyberdyne_backend.domain.access import (
    AccessReaderPort,
    WalletAccess,
    normalize_wallet_address,
)


@dataclass(slots=True)
class GetWalletAccess:
    """Validates the address then returns its aggregated access profile."""

    reader: AccessReaderPort

    async def execute(self, address: str) -> WalletAccess:
        # Raises InvalidWalletAddressError on a malformed address.
        normalized = normalize_wallet_address(address)
        return await self.reader.read_access(normalized)
