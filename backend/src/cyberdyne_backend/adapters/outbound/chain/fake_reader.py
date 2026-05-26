"""Deterministic chain reader for dev + tests.

Returns a fixed-shape snapshot that mirrors the frontend's static
fallback data so the LearnView / DaoView screens behave identically
whether the backend is wired to a real RPC or not.

Switch the active reader via ``CHAIN_READER_PROVIDER=web3py`` once
``BASE_RPC_URL`` and ``DAO_TREASURY_ADDRESS`` are set.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from cyberdyne_backend.domain.dao_treasury import (
    AaveReservePosition,
    TokenBalance,
    TreasurySnapshot,
    UniswapV4Position,
)

BASE_CHAIN_ID = 8453


class FakeChainReader:
    """Returns a stable, deterministic snapshot. ``snapshot_at`` advances
    on each call so cache-bust logic can be exercised in tests that
    use a frozen time source."""

    def __init__(self, *, now: datetime | None = None) -> None:
        self._now = now

    async def read_snapshot(self, treasury_address: str) -> TreasurySnapshot:
        moment = self._now or datetime.now(tz=UTC)
        return TreasurySnapshot(
            treasury_address=treasury_address,
            chain_id=BASE_CHAIN_ID,
            snapshot_at=moment,
            token_balances=(
                TokenBalance(
                    symbol="ETH",
                    name="Ethereum",
                    address="0x0000000000000000000000000000000000000000",
                    balance=Decimal("1247.83"),
                    usd_value=Decimal("2847352.45"),
                    change_24h_pct=Decimal("2.34"),
                    icon="⟠",
                ),
                TokenBalance(
                    symbol="USDC",
                    name="USD Coin",
                    address="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
                    balance=Decimal("425780.12"),
                    usd_value=Decimal("425780.12"),
                    change_24h_pct=Decimal("-0.01"),
                    icon="💲",
                ),
                TokenBalance(
                    symbol="cbBTC",
                    name="Coinbase Wrapped BTC",
                    address="0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf",
                    balance=Decimal("12.45"),
                    usd_value=Decimal("567845.23"),
                    change_24h_pct=Decimal("1.87"),
                    icon="₿",
                ),
            ),
            aave_positions=(
                AaveReservePosition(
                    symbol="USDC",
                    a_token_balance=Decimal("250000.00"),
                    variable_debt=Decimal("0"),
                    supply_apy=Decimal("0.0423"),
                    borrow_apy=Decimal("0.0612"),
                    usd_value_supplied=Decimal("250000.00"),
                    usd_value_borrowed=Decimal("0"),
                ),
                AaveReservePosition(
                    symbol="WETH",
                    a_token_balance=Decimal("125.50"),
                    variable_debt=Decimal("0"),
                    supply_apy=Decimal("0.0185"),
                    borrow_apy=Decimal("0.0291"),
                    usd_value_supplied=Decimal("286430.00"),
                    usd_value_borrowed=Decimal("0"),
                ),
            ),
            uniswap_positions=(
                UniswapV4Position(
                    position_id="3014821",
                    pool_id="0xabc123",
                    token0_symbol="WETH",
                    token1_symbol="USDC",
                    token0_amount=Decimal("3.2"),
                    token1_amount=Decimal("316.96"),
                    fee_tier_bps=30,
                    tick_lower=-887220,
                    tick_upper=887220,
                    in_range=False,
                    usd_value=Decimal("12607.79"),
                    uncollected_fees_usd=Decimal("7.91"),
                ),
                UniswapV4Position(
                    position_id="3014822",
                    pool_id="0xdef456",
                    token0_symbol="USDC",
                    token1_symbol="USDT",
                    token0_amount=Decimal("7500.25"),
                    token1_amount=Decimal("7499.75"),
                    fee_tier_bps=5,
                    tick_lower=-100,
                    tick_upper=100,
                    in_range=True,
                    usd_value=Decimal("15000.00"),
                    uncollected_fees_usd=Decimal("12.34"),
                ),
            ),
        )
