"""DAO treasury read-models — bounded context.

Read-only view of the DAO multisig's on-chain state on Base. Sources:
- ERC-20 token balances at the treasury address
- AAVE v3 supply/borrow positions
- Uniswap v4 LP positions

v1 ships with a deterministic ``FakeChainReader`` so the frontend can
hydrate before a real DAO multisig is registered. The Web3Py-backed
reader lands once ``DAO_TREASURY_ADDRESS`` + ``BASE_RPC_URL`` are
configured.
"""

from cyberdyne_backend.domain.dao_treasury.entities import (
    AaveReservePosition,
    DaoOverview,
    TokenBalance,
    TreasurySnapshot,
    UniswapV4Position,
)
from cyberdyne_backend.domain.dao_treasury.errors import (
    ChainReadError,
    TreasuryUnconfiguredError,
)
from cyberdyne_backend.domain.dao_treasury.ports import ChainReaderPort

__all__ = [
    "AaveReservePosition",
    "ChainReadError",
    "ChainReaderPort",
    "DaoOverview",
    "TokenBalance",
    "TreasurySnapshot",
    "TreasuryUnconfiguredError",
    "UniswapV4Position",
]
