"""Pydantic schemas for DAO treasury endpoints.

USD + token amounts are emitted as floats — JSON readability beats
decimal precision at the wire boundary, and the DaoView only renders
display strings anyway.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


def _f(value: Decimal) -> float:
    return float(value)


class TokenBalanceResponse(_CamelModel):
    symbol: str
    name: str
    address: str
    balance: float
    usd_value: float
    change_24h_pct: float = Field(serialization_alias="change24hPct")
    icon: str = ""


class AaveReservePositionResponse(_CamelModel):
    symbol: str
    a_token_balance: float
    variable_debt: float
    supply_apy: float
    borrow_apy: float
    usd_value_supplied: float
    usd_value_borrowed: float


class UniswapV4PositionResponse(_CamelModel):
    position_id: str
    pool_id: str
    token0_symbol: str
    token1_symbol: str
    token0_amount: float
    token1_amount: float
    fee_tier_bps: int
    tick_lower: int
    tick_upper: int
    in_range: bool
    usd_value: float
    uncollected_fees_usd: float


class TreasurySnapshotResponse(_CamelModel):
    treasury_address: str
    chain_id: int
    snapshot_at: datetime
    token_balances: list[TokenBalanceResponse]
    aave_positions: list[AaveReservePositionResponse]
    uniswap_positions: list[UniswapV4PositionResponse]
    total_usd_value: float


class DaoOverviewResponse(_CamelModel):
    snapshot: TreasurySnapshotResponse
    holders: int
