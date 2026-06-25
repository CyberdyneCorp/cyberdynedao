"""FastAPI auth middleware + scope dependencies.

Resolves ``request.state.principal: Principal | None`` for every
request. Token source priority: ``Authorization: Bearer …`` header
first, then ``access_token`` cookie (browser sessions). Missing token
is fine — the principal stays ``None`` and downstream code decides
whether to allow it.

The ``require_principal`` and ``require_editor`` dependencies enforce
auth on routes that need it; routes that don't depend on them stay
public.
"""

from __future__ import annotations

import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Request, Response, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from cyberdyne_backend.domain.auth_identity import (
    AuthPort,
    AuthServiceUnavailableError,
    InvalidTokenError,
    Principal,
    UserPrincipal,
    UserProfilePort,
)

logger = logging.getLogger("cyberdyne_backend.auth.middleware")

BEARER_PREFIX = "Bearer "
EDITOR_SCOPE = "editor"

# OpenAPI/Swagger contract only. Enforcement lives in the middleware (which
# also accepts the ``access_token`` cookie) + the guards below; this scheme
# exists purely so FastAPI declares an ``HTTPBearer`` security scheme and
# renders the "Authorize" button plus per-route padlocks on every operation
# that depends on a guard. ``auto_error=False`` keeps the middleware/guards as
# the single source of the 401 — this dependency never raises on its own.
bearer_scheme = HTTPBearer(auto_error=False)
# A guard depends on this so the operation inherits the security requirement.
BearerCredentials = Annotated[HTTPAuthorizationCredentials | None, Security(bearer_scheme)]


def extract_token(request: Request) -> str | None:
    """Pull the bearer token from the Authorization header or the
    ``access_token`` cookie. Public so non-middleware code (e.g. the
    chat profile lookup) can reuse the same precedence rules."""
    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.startswith(BEARER_PREFIX):
        return auth_header[len(BEARER_PREFIX) :].strip() or None
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        return cookie_token
    return None


# Backwards-compatible private alias (internal callers below).
_extract_token = extract_token


class AuthMiddleware(BaseHTTPMiddleware):
    """Resolves a principal per request and stashes it on ``request.state``.

    On a *valid* token: ``request.state.principal`` is the resolved
    principal. On *missing* or *invalid* token: ``request.state.principal``
    is None and the request proceeds — the route's guard decides whether
    to allow it. On an *unavailable upstream* (JWKS unreachable with no
    cached key): returns 503.

    The middleware *resolves*, it doesn't *enforce*. An invalid token is
    treated like no token rather than a hard 401 so that public endpoints
    keep working when a stale token rides along (e.g. the SvelteKit course
    catalogue auto-attaches the bearer to every request). Protected routes
    still reject anonymous callers via ``require_principal`` (401), which
    is what the iOS client keys its token-refresh on — so the refresh flow
    is preserved while public reads no longer break on a stale token.
    """

    def __init__(self, app: object, auth_port: AuthPort) -> None:
        super().__init__(app)  # type: ignore[arg-type]
        self._auth_port = auth_port

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        token = _extract_token(request)
        if token is None:
            request.state.principal = None
            return await call_next(request)
        try:
            principal = await self._auth_port.introspect(token)
        except InvalidTokenError as exc:
            logger.debug("ignoring invalid token, proceeding anonymously: %s", exc)
            request.state.principal = None
            return await call_next(request)
        except AuthServiceUnavailableError as exc:
            logger.warning("auth upstream unavailable: %s", exc)
            return Response(
                content='{"detail":"auth service unavailable"}',
                status_code=503,
                media_type="application/json",
            )
        request.state.principal = principal
        return await call_next(request)


# ── Dependencies ─────────────────────────────────────────────────────


def require_principal(
    request: Request,
    _credentials: BearerCredentials = None,
) -> Principal:
    """Asserts that the middleware resolved a principal; 401 otherwise.

    ``_credentials`` is unused at runtime (the middleware already resolved
    the token from the header *or* cookie); it's declared only so FastAPI
    attaches the ``HTTPBearer`` scheme to every operation guarded here.
    """
    principal: Principal | None = getattr(request.state, "principal", None)
    if principal is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="authentication required"
        )
    return principal


def get_user_profile_port() -> UserProfilePort | None:
    """Provider seam for the ``/users/me`` profile port.

    The app factory overrides this with the container's cached client.
    Defaults to ``None`` so guards that depend on it degrade to
    introspection-only when the port isn't wired (e.g. minimal test
    apps that don't need the profile fallback).
    """
    return None


async def require_editor(
    request: Request,
    profile_port: Annotated[UserProfilePort | None, Depends(get_user_profile_port)] = None,
    _credentials: BearerCredentials = None,
) -> UserPrincipal:
    """Asserts the caller may author content.

    Service tokens (``ServicePrincipal``) are rejected — authoring is
    gated to human reviewers. A user passes when any of:

    - the token carries the ``editor`` scope,
    - the introspection response flags the user as an admin, or
    - the user's ``/users/me`` profile flags them as an admin.

    The admin path exists because CyberdyneAuth's on-chain policy
    engine — which would otherwise grant the ``editor`` scope — is
    currently disabled, so it doesn't surface scopes on user tokens.
    Admins are recognised by the ``is_superuser`` / ``is_admin`` flag
    instead. That flag may live on the introspection response or only
    on ``/users/me`` depending on the auth-server version, so we check
    introspection first (free — already resolved by the middleware) and
    fall back to a best-effort, cached profile lookup only when needed.
    """
    principal = require_principal(request)
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user token required (service tokens cannot edit asks)",
        )
    if EDITOR_SCOPE in principal.scopes or principal.is_admin:
        return principal

    # Introspection didn't authorise the caller. CyberdyneAuth may only
    # surface the admin flag on /users/me, so try that before rejecting.
    if profile_port is not None:
        token = extract_token(request)
        if token:
            profile = await profile_port.get_profile(token)
            if profile is not None and profile.is_admin:
                return principal

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="editor scope or admin required",
    )
