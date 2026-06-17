"""Wallet endpoints — public access-tier lookup backing NFTTerminal and
the chat agent's ``get_user_tier`` tool (issue #7)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from cyberdyne_backend.adapters.inbound.api.wallet.schemas import (
    AccessTraitsResponse,
    WalletAccessResponse,
)
from cyberdyne_backend.application.access import GetWalletAccess
from cyberdyne_backend.domain.access import (
    AccessReadError,
    InvalidWalletAddressError,
    WalletAccess,
)

router = APIRouter(prefix="/api/v1/wallet", tags=["wallet"])


async def get_wallet_access_uc() -> GetWalletAccess:  # pragma: no cover - override target
    raise NotImplementedError


def _to_response(access: WalletAccess) -> WalletAccessResponse:
    t = access.traits
    return WalletAccessResponse(
        address=access.address,
        has_access_nft=access.has_access_nft,
        token_count=access.token_count,
        traits=AccessTraitsResponse(
            learning=t.learning,
            frontend=t.frontend,
            backend=t.backend,
            blog_creator=t.blog_creator,
            admin=t.admin,
            marketplace=t.marketplace,
        ),
    )


@router.get(
    "/{address}/access-tier",
    response_model=WalletAccessResponse,
    response_model_by_alias=True,
)
async def get_access_tier(
    address: str,
    use_case: Annotated[GetWalletAccess, Depends(get_wallet_access_uc)],
) -> WalletAccessResponse:
    try:
        access = await use_case.execute(address)
    except InvalidWalletAddressError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except AccessReadError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return _to_response(access)


__all__ = ["get_wallet_access_uc", "router"]
