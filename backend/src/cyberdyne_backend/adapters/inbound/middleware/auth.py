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

from fastapi import HTTPException, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from cyberdyne_backend.domain.auth_identity import (
    AuthPort,
    AuthServiceUnavailableError,
    InvalidTokenError,
    Principal,
    UserPrincipal,
)

logger = logging.getLogger("cyberdyne_backend.auth.middleware")

BEARER_PREFIX = "Bearer "
EDITOR_SCOPE = "editor"


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
    principal. On *missing* token: ``request.state.principal`` is None
    (route decides whether to allow). On an *invalid* token: returns
    401 directly. On an *unavailable upstream*: returns 503.
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
        except InvalidTokenError:
            return Response(
                content='{"detail":"invalid token"}',
                status_code=401,
                media_type="application/json",
            )
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


def require_principal(request: Request) -> Principal:
    """Asserts that the middleware resolved a principal; 401 otherwise."""
    principal: Principal | None = getattr(request.state, "principal", None)
    if principal is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="authentication required"
        )
    return principal


def require_editor(request: Request) -> UserPrincipal:
    """Asserts the caller is a user with the ``editor`` scope.

    Service tokens (``ServicePrincipal``) are rejected — admin actions
    are gated to human reviewers. Phase 1 wired scopes through
    introspection; CyberdyneAuth doesn't yet surface scopes on user
    tokens directly, so until that lands we additionally accept
    ``email``-claim allowlisting in a follow-up PR. For now the scope
    check is authoritative.
    """
    principal = require_principal(request)
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user token required (service tokens cannot edit asks)",
        )
    if EDITOR_SCOPE not in principal.scopes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="editor scope required",
        )
    return principal
