"""CyberdyneAuth RFC 7662 introspection client.

One canonical call: ``POST /api/v1/auth/introspect`` with the bearer
to be validated as ``token`` form-field. Response decoded into a
``Principal`` via ``principal_from_introspection``.

The pattern is lifted from ``geo_dashboard/backend`` (caching shape +
SHA-256 keys + request coalescing live in ``caching_auth_port``); the
*call target* moves from ``/users/me`` to ``/auth/introspect`` because
CyberdyneAuth v0.1.0 now ships RFC 7662 — single endpoint validates
either a user or a service token.
"""

from __future__ import annotations

import logging

import httpx

from cyberdyne_backend.domain.auth_identity import (
    AuthServiceUnavailableError,
    InvalidTokenError,
    Principal,
)
from cyberdyne_backend.domain.auth_identity.entities import principal_from_introspection

logger = logging.getLogger("cyberdyne_backend.auth.introspection")

INTROSPECTION_PATH = "/api/v1/auth/introspect"


class IntrospectionClient:
    """Validates bearer tokens by hitting CyberdyneAuth's introspect endpoint."""

    def __init__(
        self,
        base_url: str,
        http_client: httpx.AsyncClient,
        timeout_s: float = 5.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._http = http_client
        self._timeout = timeout_s

    async def introspect(self, token: str) -> Principal:
        if not token:
            raise InvalidTokenError("empty bearer token")
        url = f"{self._base_url}{INTROSPECTION_PATH}"
        try:
            response = await self._http.post(
                url,
                data={"token": token},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=self._timeout,
            )
        except httpx.TimeoutException as exc:
            raise AuthServiceUnavailableError(f"timeout calling introspect: {exc}") from exc
        except httpx.HTTPError as exc:
            raise AuthServiceUnavailableError(f"transport error: {exc}") from exc

        if response.status_code >= 500:
            raise AuthServiceUnavailableError(
                f"CyberdyneAuth {response.status_code}: {response.text[:240]}"
            )
        if response.status_code != 200:
            # Anything other than 200 here (401, 403, 422, …) means the
            # caller's token is not introspectable / we malformed the
            # request — treat as auth failure rather than retrying.
            raise InvalidTokenError(
                f"unexpected introspect status {response.status_code}: {response.text[:240]}"
            )
        payload = response.json()
        principal = principal_from_introspection(payload)
        if principal is None:
            raise InvalidTokenError("introspect returned active=false or unrecognised claims")
        return principal
