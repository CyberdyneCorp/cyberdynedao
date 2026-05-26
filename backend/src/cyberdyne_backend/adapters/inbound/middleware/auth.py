"""FastAPI auth middleware.

Resolves ``request.state.principal: Principal | None`` for every
request. Token source priority: ``Authorization: Bearer …`` header
first, then ``access_token`` cookie (browser sessions). Missing token
is fine — the principal stays ``None`` and downstream code decides
whether to allow it.
"""

from __future__ import annotations

import logging

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from cyberdyne_backend.domain.auth_identity import (
    AuthPort,
    AuthServiceUnavailableError,
    InvalidTokenError,
)

logger = logging.getLogger("cyberdyne_backend.auth.middleware")

BEARER_PREFIX = "Bearer "


def _extract_token(request: Request) -> str | None:
    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.startswith(BEARER_PREFIX):
        return auth_header[len(BEARER_PREFIX) :].strip() or None
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        return cookie_token
    return None


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
