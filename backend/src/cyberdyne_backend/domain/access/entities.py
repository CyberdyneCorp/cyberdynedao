"""Access-tier read-model entities — the CyberdyneAccessNFT capability set.

The on-chain ``CyberdyneAccessNFT`` grants per-address capabilities (the
frontend reads them via ``getUserPermissions`` and ORs the booleans across
every token the address holds). This context mirrors that aggregated view
server-side so the chat agent's ``get_user_tier`` tool and any future
NFT-gated endpoint share one source of truth instead of each re-reading the
chain. Read-only — nothing here mutates on-chain state.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from cyberdyne_backend.domain.access.errors import InvalidWalletAddressError

_ADDRESS_RE = re.compile(r"^0x[0-9a-fA-F]{40}$")


def normalize_wallet_address(address: str) -> str:
    """Validate an EVM address and return it lower-cased for stable keying.

    Raises ``InvalidWalletAddressError`` for anything that isn't a
    ``0x``-prefixed 40-hex-character address.
    """
    candidate = (address or "").strip()
    if not _ADDRESS_RE.match(candidate):
        raise InvalidWalletAddressError(f"not a valid EVM address: {address!r}")
    return candidate.lower()


@dataclass(frozen=True, slots=True)
class AccessTraits:
    """The six boolean capabilities carried by the access NFT, aggregated
    (logical OR) across every token an address holds — same shape as the
    frontend ``NFTTraits``."""

    learning: bool = False
    frontend: bool = False
    backend: bool = False
    blog_creator: bool = False
    admin: bool = False
    marketplace: bool = False

    @property
    def any(self) -> bool:
        return any(
            (
                self.learning,
                self.frontend,
                self.backend,
                self.blog_creator,
                self.admin,
                self.marketplace,
            )
        )


@dataclass(frozen=True, slots=True)
class WalletAccess:
    """Aggregated access profile for one wallet address."""

    address: str
    has_access_nft: bool
    token_count: int
    traits: AccessTraits

    @classmethod
    def none(cls, address: str) -> WalletAccess:
        """A wallet that holds no access NFT — every capability denied."""
        return cls(
            address=address,
            has_access_nft=False,
            token_count=0,
            traits=AccessTraits(),
        )
