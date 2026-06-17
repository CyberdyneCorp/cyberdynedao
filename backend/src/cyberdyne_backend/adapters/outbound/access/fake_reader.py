"""Deterministic stub for the access-NFT reader.

Active until the web3py-backed reader is wired (it needs ``BASE_RPC_URL``
plus the CyberdyneAccessNFT contract address). Returns "no access NFT" for
every address by default — the honest not-provisioned state. Tests (and a
local dev fixture) can pass an explicit ``grants`` map to simulate holders.

Deliberately conservative: unlike the DAO ``FakeChainReader`` (which
fabricates treasury data so the view renders), this fabricates NO
capabilities — an access/permissions stub must never hand out a fake
``admin`` grant.
"""

from __future__ import annotations

from cyberdyne_backend.domain.access import WalletAccess


class FakeAccessReader:
    """Returns the granted profile for known addresses, else no-access."""

    def __init__(self, grants: dict[str, WalletAccess] | None = None) -> None:
        # Keyed by normalized (lower-cased) address.
        self._grants = {addr.lower(): access for addr, access in (grants or {}).items()}

    async def read_access(self, address: str) -> WalletAccess:
        return self._grants.get(address, WalletAccess.none(address))
