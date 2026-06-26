"""FastAPI dependencies that enforce server-side quota / Pro fair-use.

DAO enforces the free-tier caps and Pro fair-use soft caps for the
token/compute-heavy features regardless of what the client shows (issue #230):

- :class:`QuotaGuard` — attach to an endpoint to meter it. A non-Pro user over
  the free cap gets **402** (paywall); a Pro user over the soft cap gets
  **429** (slow-down). Anonymous/service callers are skipped (the per-IP
  limiter / auth guards cover those). Allowed requests get ``X-Quota-*`` headers
  so the client can render a meter.
- :func:`require_pro` — gate a Pro-only feature (certificate issuance); a
  non-Pro user gets **402**.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, HTTPException, Response

from cyberdyne_backend.adapters.inbound.middleware.auth import (
    optional_principal,
    require_principal,
)
from cyberdyne_backend.application.quota import EnforceQuota
from cyberdyne_backend.domain.auth_identity import Principal, UserPrincipal
from cyberdyne_backend.domain.quota import (
    FairUseThrottledError,
    FreeQuotaExceededError,
    QuotaDecision,
    QuotaError,
    QuotaMeter,
)


async def get_enforce_quota_uc() -> EnforceQuota:  # pragma: no cover - override target
    raise NotImplementedError


def _error_headers(exc: QuotaError) -> dict[str, str]:
    reset_epoch = int(exc.reset_at.timestamp())
    headers = {
        "X-Quota-Meter": exc.meter.value,
        "X-Quota-Limit": str(exc.limit),
        "X-Quota-Remaining": "0",
        "X-Quota-Reset": str(reset_epoch),
    }
    return headers


def _quota_http_error(status_code: int, code: str, exc: QuotaError) -> HTTPException:
    headers = _error_headers(exc)
    if status_code == 429:
        remaining_s = int((exc.reset_at - datetime.now(tz=UTC)).total_seconds())
        headers["Retry-After"] = str(max(0, remaining_s))
    return HTTPException(
        status_code=status_code,
        detail={
            "code": code,
            "meter": exc.meter.value,
            "limit": exc.limit,
            "resetAt": exc.reset_at.isoformat(),
        },
        headers=headers,
    )


def _set_quota_headers(response: Response, decision: QuotaDecision) -> None:
    response.headers["X-Quota-Meter"] = decision.meter.value
    response.headers["X-Quota-Reset"] = str(int(decision.reset_at.timestamp()))
    if decision.limit is not None:
        response.headers["X-Quota-Limit"] = str(decision.limit)
        response.headers["X-Quota-Remaining"] = str(decision.remaining or 0)


class QuotaGuard:
    """Per-user quota enforcement for one meter, used as a route dependency:
    ``dependencies=[Depends(QuotaGuard(QuotaMeter.TUTOR_MESSAGES))]``."""

    def __init__(self, meter: QuotaMeter) -> None:
        self._meter = meter

    async def __call__(
        self,
        response: Response,
        enforcer: Annotated[EnforceQuota, Depends(get_enforce_quota_uc)],
        principal: Annotated[UserPrincipal | None, Depends(optional_principal)],
    ) -> None:
        if principal is None:
            return  # anonymous/service — not subject to per-user quota
        try:
            decision = await enforcer.execute(
                user_id=principal.user_id, meter=self._meter, is_pro=principal.is_pro
            )
        except FreeQuotaExceededError as exc:
            raise _quota_http_error(402, "quota_exceeded", exc) from exc
        except FairUseThrottledError as exc:
            raise _quota_http_error(429, "fair_use_throttled", exc) from exc
        _set_quota_headers(response, decision)


def require_pro(
    principal: Annotated[Principal, Depends(require_principal)],
) -> UserPrincipal:
    """Gate a Pro-only feature. A non-Pro (or non-user) caller gets 402 so the
    client can show the paywall."""
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    if not principal.is_pro:
        raise HTTPException(
            status_code=402,
            detail={"code": "pro_required", "feature": "certificate"},
        )
    return principal
