"""DAO treasury read-model entities.

All values are read-only snapshots — no setters, no domain methods that
mutate. Anything in this context is rendered, not edited.

Money is carried as ``Decimal`` so amounts and USD values don't drift
through float arithmetic. The web layer converts to ``float`` at the
schema boundary.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class TokenBalance:
    """ERC-20 balance held by the treasury address."""

    symbol: str
    name: str
    address: str  # checksummed contract address
    balance: Decimal  # raw amount in human units (already decimals-shifted)
    usd_value: Decimal
    change_24h_pct: Decimal  # signed percent, e.g. 2.34 means +2.34%
    icon: str = ""


@dataclass(frozen=True, slots=True)
class AaveReservePosition:
    """A supply or borrow position on AAVE v3."""

    symbol: str
    a_token_balance: Decimal  # supplied (aTokens), 0 if pure borrower
    variable_debt: Decimal  # variable-rate debt, 0 if pure supplier
    supply_apy: Decimal  # decimal fraction, e.g. 0.0423 = 4.23%
    borrow_apy: Decimal
    usd_value_supplied: Decimal
    usd_value_borrowed: Decimal


@dataclass(frozen=True, slots=True)
class UniswapV4Position:
    """A Uniswap v4 LP position held by the treasury."""

    position_id: str  # NFT tokenId as a string
    pool_id: str
    token0_symbol: str
    token1_symbol: str
    token0_amount: Decimal
    token1_amount: Decimal
    fee_tier_bps: int  # e.g. 30 = 0.30%
    tick_lower: int
    tick_upper: int
    in_range: bool
    usd_value: Decimal
    uncollected_fees_usd: Decimal


@dataclass(frozen=True, slots=True)
class TreasurySnapshot:
    """Snapshot of the treasury at a point in time.

    ``snapshot_at`` is the moment the chain reads were completed (not
    the on-chain block timestamp; we don't pin to a block in v1).
    """

    treasury_address: str
    chain_id: int  # 8453 = Base mainnet
    snapshot_at: datetime
    token_balances: tuple[TokenBalance, ...]
    aave_positions: tuple[AaveReservePosition, ...]
    uniswap_positions: tuple[UniswapV4Position, ...]

    @property
    def total_usd_value(self) -> Decimal:
        tokens = sum((b.usd_value for b in self.token_balances), Decimal(0))
        aave = sum(
            (p.usd_value_supplied - p.usd_value_borrowed for p in self.aave_positions),
            Decimal(0),
        )
        uni = sum((p.usd_value for p in self.uniswap_positions), Decimal(0))
        return Decimal(tokens) + Decimal(aave) + Decimal(uni)


@dataclass(frozen=True, slots=True)
class DaoOverview:
    """Bundled response backing the DaoView + InvestmentsView screens."""

    snapshot: TreasurySnapshot
    holders: int = 0
    # Extension slot for governance metadata once the DAO ships (proposal
    # count, voter participation, etc.). Defers to Phase 6+.
    extras: dict[str, object] = field(default_factory=dict)
