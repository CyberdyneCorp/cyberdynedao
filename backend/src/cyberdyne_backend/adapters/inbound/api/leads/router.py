"""Leads endpoints — public asks + admin triage.

- ``POST /api/v1/asks`` — public, captcha-gated, basic rate-limited.
- ``GET /api/v1/admin/asks`` — editor scope only.
- ``GET /api/v1/admin/asks/{id}`` — editor scope only, returns events.
- ``PATCH /api/v1/admin/asks/{id}`` — editor scope only.

The rate limiter is a small in-memory token bucket — fine for one
Coolify replica; PR-tracked switch to Redis once horizontal scale
matters (Open Q 8 on the roadmap).
"""

from __future__ import annotations

import time
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request

from cyberdyne_backend.adapters.inbound.api.leads.schemas import (
    AdminListAsksResponse,
    AskDetailResponse,
    AskEventResponse,
    AskResponse,
    CreateAskRequest,
    UpdateAskRequest,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import require_editor
from cyberdyne_backend.application.leads import (
    AdminListAsks,
    AdminUpdateAsk,
    CreateAsk,
)
from cyberdyne_backend.application.leads.use_cases import (
    AdminListAsksQuery,
    AdminUpdateAskCommand,
    CreateAskCommand,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.leads import (
    Ask,
    AskChannel,
    AskNotFoundError,
    AskStatus,
    AskTransitionError,
    CaptchaVerificationError,
)

# Routers — public asks + admin triage live on separate prefixes.
public_router = APIRouter(prefix="/api/v1/asks", tags=["leads"])
admin_router = APIRouter(prefix="/api/v1/admin/asks", tags=["leads-admin"])


# Dependency stubs — overridden in main.py.
async def get_create_ask_uc() -> CreateAsk:  # pragma: no cover - override target
    raise NotImplementedError("CreateAsk dependency not wired")


async def get_admin_list_asks_uc() -> AdminListAsks:  # pragma: no cover - override target
    raise NotImplementedError("AdminListAsks dependency not wired")


async def get_admin_update_ask_uc() -> AdminUpdateAsk:  # pragma: no cover - override target
    raise NotImplementedError("AdminUpdateAsk dependency not wired")


# ── In-memory rate limiter ───────────────────────────────────────────
# 5 requests per minute per IP. Per-replica; resets on restart.

_RATE_LIMIT = 5
_WINDOW_S = 60.0
_ip_hits: dict[str, list[float]] = {}


def _check_rate_limit(remote_ip: str | None) -> None:
    if remote_ip is None:
        return  # behind a stripped header — let it pass; captcha is the real gate
    now = time.monotonic()
    bucket = _ip_hits.setdefault(remote_ip, [])
    cutoff = now - _WINDOW_S
    bucket[:] = [t for t in bucket if t > cutoff]
    if len(bucket) >= _RATE_LIMIT:
        raise HTTPException(status_code=429, detail="too many ask submissions; slow down")
    bucket.append(now)


def _ask_response(ask: Ask) -> AskResponse:
    return AskResponse(
        id=ask.id,
        channel=ask.channel.value,
        name=ask.name,
        email=ask.email,
        body=ask.body,
        product_slug=ask.product_slug,
        source_url=ask.source_url,
        status=ask.status.value,
        owner_user_id=ask.owner_user_id,
        notes_md=ask.notes_md,
        created_at=ask.created_at,
    )


def _ask_detail_response(ask: Ask) -> AskDetailResponse:
    return AskDetailResponse(
        **_ask_response(ask).model_dump(by_alias=False),
        events=[
            AskEventResponse(id=e.id, kind=e.kind.value, by_user_id=e.by_user_id, at=e.at)
            for e in ask.events
        ],
    )


# ── Public POST /api/v1/asks ─────────────────────────────────────────


@public_router.post(
    "",
    response_model=AskResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def create_ask(
    request: Request,
    body: CreateAskRequest,
    use_case: Annotated[CreateAsk, Depends(get_create_ask_uc)],
) -> AskResponse:
    remote_ip = request.client.host if request.client else None
    _check_rate_limit(remote_ip)
    try:
        ask = await use_case.execute(
            CreateAskCommand(
                name=body.name,
                email=body.email,
                body=body.body,
                channel=AskChannel(body.channel),
                captcha_token=body.captcha_token,
                remote_ip=remote_ip,
                product_slug=body.product_slug,
                source_url=body.source_url,
            )
        )
    except CaptchaVerificationError as exc:
        raise HTTPException(status_code=400, detail=f"captcha rejected: {exc}") from exc
    return _ask_response(ask)


# ── Admin endpoints ──────────────────────────────────────────────────


@admin_router.get(
    "",
    response_model=AdminListAsksResponse,
    response_model_by_alias=True,
)
async def admin_list_asks(
    use_case: Annotated[AdminListAsks, Depends(get_admin_list_asks_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
    status: AskStatus | None = None,
    channel: str | None = None,
    q: str | None = None,
    page: int = 1,
    page_size: int = 50,
) -> AdminListAsksResponse:
    items, total = await use_case.execute(
        AdminListAsksQuery(
            status=status,
            channel=channel,
            query=q,
            page=max(1, page),
            page_size=min(max(1, page_size), 200),
        )
    )
    return AdminListAsksResponse(
        items=[_ask_response(a) for a in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@admin_router.patch(
    "/{ask_id}",
    response_model=AskDetailResponse,
    response_model_by_alias=True,
)
async def admin_update_ask(
    ask_id: UUID,
    body: UpdateAskRequest,
    use_case: Annotated[AdminUpdateAsk, Depends(get_admin_update_ask_uc)],
    principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> AskDetailResponse:
    try:
        ask = await use_case.execute(
            AdminUpdateAskCommand(
                ask_id=ask_id,
                by_user_id=principal.user_id,
                new_status=AskStatus(body.new_status) if body.new_status else None,
                note=body.note,
                new_owner_user_id=body.new_owner_user_id,
            )
        )
    except AskNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AskTransitionError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return _ask_detail_response(ask)


__all__ = ["admin_router", "public_router"]
