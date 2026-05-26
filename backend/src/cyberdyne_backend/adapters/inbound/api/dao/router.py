"""DAO treasury endpoints — bundled overview backing the DaoView."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from cyberdyne_backend.adapters.inbound.api.dao.schemas import (
    AaveReservePositionResponse,
    DaoOverviewResponse,
    TokenBalanceResponse,
    TreasurySnapshotResponse,
    UniswapV4PositionResponse,
)
from cyberdyne_backend.application.dao_treasury import GetDaoOverview
from cyberdyne_backend.domain.dao_treasury import (
    ChainReadError,
    DaoOverview,
    TreasuryUnconfiguredError,
)

router = APIRouter(prefix="/api/v1/dao", tags=["dao"])


async def get_dao_overview_uc() -> GetDaoOverview:  # pragma: no cover - override target
    raise NotImplementedError


def _to_response(overview: DaoOverview) -> DaoOverviewResponse:
    s = overview.snapshot
    return DaoOverviewResponse(
        snapshot=TreasurySnapshotResponse(
            treasury_address=s.treasury_address,
            chain_id=s.chain_id,
            snapshot_at=s.snapshot_at,
            token_balances=[
                TokenBalanceResponse(
                    symbol=b.symbol,
                    name=b.name,
                    address=b.address,
                    balance=float(b.balance),
                    usd_value=float(b.usd_value),
                    change_24h_pct=float(b.change_24h_pct),
                    icon=b.icon,
                )
                for b in s.token_balances
            ],
            aave_positions=[
                AaveReservePositionResponse(
                    symbol=p.symbol,
                    a_token_balance=float(p.a_token_balance),
                    variable_debt=float(p.variable_debt),
                    supply_apy=float(p.supply_apy),
                    borrow_apy=float(p.borrow_apy),
                    usd_value_supplied=float(p.usd_value_supplied),
                    usd_value_borrowed=float(p.usd_value_borrowed),
                )
                for p in s.aave_positions
            ],
            uniswap_positions=[
                UniswapV4PositionResponse(
                    position_id=p.position_id,
                    pool_id=p.pool_id,
                    token0_symbol=p.token0_symbol,
                    token1_symbol=p.token1_symbol,
                    token0_amount=float(p.token0_amount),
                    token1_amount=float(p.token1_amount),
                    fee_tier_bps=p.fee_tier_bps,
                    tick_lower=p.tick_lower,
                    tick_upper=p.tick_upper,
                    in_range=p.in_range,
                    usd_value=float(p.usd_value),
                    uncollected_fees_usd=float(p.uncollected_fees_usd),
                )
                for p in s.uniswap_positions
            ],
            total_usd_value=float(s.total_usd_value),
        ),
        holders=overview.holders,
    )


@router.get(
    "/overview",
    response_model=DaoOverviewResponse,
    response_model_by_alias=True,
)
async def get_overview(
    use_case: Annotated[GetDaoOverview, Depends(get_dao_overview_uc)],
) -> DaoOverviewResponse:
    try:
        overview = await use_case.execute()
    except TreasuryUnconfiguredError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ChainReadError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return _to_response(overview)


__all__ = ["get_dao_overview_uc", "router"]
