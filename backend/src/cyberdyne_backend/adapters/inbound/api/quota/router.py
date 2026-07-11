"""Admin quota endpoint — reset a user's usage counters.

Lets an editor/admin clear a user's current-period usage (e.g. unblock a
test account that hit its free-tier cap) without a DB reset. Guarded by
``require_editor``.
"""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from cyberdyne_backend.adapters.inbound.middleware.auth import require_editor
from cyberdyne_backend.application.quota import ResetQuota
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.quota import QuotaMeter

router = APIRouter(prefix="/api/v1/admin/quota", tags=["admin", "quota"])


async def get_reset_quota_uc() -> ResetQuota:  # pragma: no cover - override target
    raise NotImplementedError


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ResetQuotaRequest(_CamelModel):
    user_id: UUID
    # Which meter to reset; omit to reset all meters for the user.
    meter: str | None = None


class ResetQuotaResponse(_CamelModel):
    user_id: UUID
    reset: list[str]


@router.post("/reset", response_model=ResetQuotaResponse, response_model_by_alias=True)
async def reset_quota(
    body: ResetQuotaRequest,
    use_case: Annotated[ResetQuota, Depends(get_reset_quota_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> ResetQuotaResponse:
    meter: QuotaMeter | None = None
    if body.meter is not None:
        try:
            meter = QuotaMeter(body.meter)
        except ValueError as exc:
            valid = [m.value for m in QuotaMeter]
            raise HTTPException(
                status_code=422, detail=f"unknown meter {body.meter!r}; valid: {valid}"
            ) from exc
    reset = await use_case.execute(user_id=body.user_id, meter=meter)
    return ResetQuotaResponse(user_id=body.user_id, reset=[m.value for m in reset])
