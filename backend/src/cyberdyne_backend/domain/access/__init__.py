"""Access-tier read-models — bounded context.

Server-side mirror of the CyberdyneAccessNFT capability set, so the chat
agent and future NFT-gated endpoints share one aggregation instead of each
re-reading the chain. v1 ships a deterministic stub reader (no NFT for any
address); the web3py-backed reader lands with the chain-reader work once
``BASE_RPC_URL`` + the access-NFT contract address are configured.
"""

from cyberdyne_backend.domain.access.entities import (
    AccessTraits,
    WalletAccess,
    normalize_wallet_address,
)
from cyberdyne_backend.domain.access.errors import (
    AccessReadError,
    InvalidWalletAddressError,
)
from cyberdyne_backend.domain.access.ports import AccessReaderPort

__all__ = [
    "AccessReadError",
    "AccessReaderPort",
    "AccessTraits",
    "InvalidWalletAddressError",
    "WalletAccess",
    "normalize_wallet_address",
]
