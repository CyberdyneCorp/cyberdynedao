"""Favorites/bookmarks + recently-viewed endpoints (learner-scoped).

Surfaced by the redesigned client sidebar (Saved / Recent / Add to
Favorites). See issue #162. All routes are scoped to the authenticated
user; no cross-user access is possible.
"""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response

from cyberdyne_backend.adapters.inbound.api.bookmarks.schemas import (
    AddFavoriteRequest,
    FavoriteResponse,
    RecentViewResponse,
    RecordRecentRequest,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.application.bookmarks import (
    DEFAULT_RECENT_LIMIT,
    MAX_RECENT_LIMIT,
    AddFavorite,
    ListFavorites,
    ListRecent,
    RecordRecentView,
    RemoveFavorite,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.bookmarks import (
    Favorite,
    FavoriteNotFoundError,
    RecentView,
    parse_bookmark_type,
)

public_router = APIRouter(prefix="/api/v1/me", tags=["me"])


# Dependency stubs — overridden in main.py.
async def get_list_favorites_uc() -> ListFavorites:  # pragma: no cover - override target
    raise NotImplementedError


async def get_add_favorite_uc() -> AddFavorite:  # pragma: no cover - override target
    raise NotImplementedError


async def get_remove_favorite_uc() -> RemoveFavorite:  # pragma: no cover - override target
    raise NotImplementedError


async def get_record_recent_uc() -> RecordRecentView:  # pragma: no cover - override target
    raise NotImplementedError


async def get_list_recent_uc() -> ListRecent:  # pragma: no cover - override target
    raise NotImplementedError


def _favorite_response(f: Favorite) -> FavoriteResponse:
    return FavoriteResponse(
        id=f.id,
        type=f.type.value,
        ref=f.ref,
        added_at=f.added_at,
    )


def _recent_response(v: RecentView) -> RecentViewResponse:
    return RecentViewResponse(
        id=v.id,
        type=v.type.value,
        ref=v.ref,
        viewed_at=v.viewed_at,
    )


def _require_user(principal: UserPrincipal) -> UserPrincipal:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    return principal


# ── Favorites ────────────────────────────────────────────────────────


@public_router.get(
    "/favorites",
    response_model=list[FavoriteResponse],
    response_model_by_alias=True,
)
async def list_favorites(
    use_case: Annotated[ListFavorites, Depends(get_list_favorites_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> list[FavoriteResponse]:
    user = _require_user(principal)
    favorites = await use_case.execute(user.user_id)
    return [_favorite_response(f) for f in favorites]


@public_router.post(
    "/favorites",
    response_model=FavoriteResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def add_favorite(
    body: AddFavoriteRequest,
    use_case: Annotated[AddFavorite, Depends(get_add_favorite_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> FavoriteResponse:
    user = _require_user(principal)
    favorite = await use_case.execute(
        user_id=user.user_id,
        type=parse_bookmark_type(body.type),
        ref=body.ref,
    )
    return _favorite_response(favorite)


@public_router.delete("/favorites/{favorite_id}", status_code=204)
async def remove_favorite(
    favorite_id: UUID,
    use_case: Annotated[RemoveFavorite, Depends(get_remove_favorite_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> Response:
    user = _require_user(principal)
    try:
        await use_case.execute(user_id=user.user_id, favorite_id=favorite_id)
    except FavoriteNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Response(status_code=204)


# ── Recently viewed ──────────────────────────────────────────────────


@public_router.get(
    "/recent",
    response_model=list[RecentViewResponse],
    response_model_by_alias=True,
)
async def list_recent(
    use_case: Annotated[ListRecent, Depends(get_list_recent_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
    limit: Annotated[int, Query(ge=1, le=MAX_RECENT_LIMIT)] = DEFAULT_RECENT_LIMIT,
) -> list[RecentViewResponse]:
    user = _require_user(principal)
    views = await use_case.execute(user.user_id, limit=limit)
    return [_recent_response(v) for v in views]


@public_router.post(
    "/recent",
    response_model=RecentViewResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def record_recent(
    body: RecordRecentRequest,
    use_case: Annotated[RecordRecentView, Depends(get_record_recent_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> RecentViewResponse:
    user = _require_user(principal)
    view = await use_case.execute(
        user_id=user.user_id,
        type=parse_bookmark_type(body.type),
        ref=body.ref,
    )
    return _recent_response(view)
