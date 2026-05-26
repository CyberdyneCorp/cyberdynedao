"""OAuth 2.0 client-credentials provider for outbound service calls.

The backend exchanges its ``client_id`` + ``client_secret`` for an
``access_token`` against CyberdyneAuth's ``POST /api/v1/auth/oauth2/token``
endpoint (RFC 6749 §4.4). The token is cached in memory and refreshed
at 90% of its TTL by a background task started on app startup.

Anywhere we make an outbound call as the backend itself (e.g. to
CyberRAG or the CyberdyneAuth admin endpoints) we ask the provider for
the current bearer.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import time
from dataclasses import dataclass

import httpx

logger = logging.getLogger("cyberdyne_backend.auth.service_token")

TOKEN_PATH = "/api/v1/auth/oauth2/token"
# Refresh just before the upstream TTL elapses so a slow refresh doesn't
# briefly expose us with no token.
REFRESH_RATIO = 0.9


class ServiceTokenError(RuntimeError):
    """Raised when the backend cannot obtain or refresh its own service token."""


@dataclass(slots=True, frozen=True)
class _IssuedToken:
    access_token: str
    expires_at_monotonic: float


class ServiceTokenProvider:
    """Mints + caches the backend's own client-credentials access token."""

    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        http_client: httpx.AsyncClient,
        scopes: str = "",
        audience: str | None = None,
        timeout_s: float = 5.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._client_id = client_id
        self._client_secret = client_secret
        self._http = http_client
        self._scopes = scopes
        self._audience = audience
        self._timeout = timeout_s
        self._token: _IssuedToken | None = None
        self._lock = asyncio.Lock()
        self._refresh_task: asyncio.Task[None] | None = None

    async def get_token(self) -> str:
        """Return a currently valid access token, minting one if needed."""
        async with self._lock:
            if self._token is None or time.monotonic() >= self._token.expires_at_monotonic:
                await self._mint_locked()
            # _mint_locked either sets _token or raises; the cast keeps
            # mypy honest without an `assert`.
            token = self._token
            if token is None:  # pragma: no cover  # defensive — _mint_locked guarantees this
                raise ServiceTokenError("token unexpectedly missing after mint")
            return token.access_token

    async def start(self) -> None:
        """Mint the first token and start the background refresh loop."""
        async with self._lock:
            await self._mint_locked()
        loop = asyncio.get_running_loop()
        self._refresh_task = loop.create_task(self._refresh_loop())

    async def stop(self) -> None:
        if self._refresh_task is not None:
            self._refresh_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._refresh_task
            self._refresh_task = None

    async def _mint_locked(self) -> None:
        url = f"{self._base_url}{TOKEN_PATH}"
        data: dict[str, str] = {"grant_type": "client_credentials"}
        if self._scopes:
            data["scope"] = self._scopes
        if self._audience:
            data["audience"] = self._audience
        try:
            response = await self._http.post(
                url,
                data=data,
                auth=(self._client_id, self._client_secret),
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=self._timeout,
            )
        except httpx.HTTPError as exc:
            raise ServiceTokenError(f"transport error from oauth2/token: {exc}") from exc

        if response.status_code != 200:
            raise ServiceTokenError(
                f"oauth2/token returned {response.status_code}: {response.text[:240]}"
            )
        payload = response.json()
        access_token = payload.get("access_token")
        expires_in = payload.get("expires_in")
        if not isinstance(access_token, str) or not access_token:
            raise ServiceTokenError("oauth2/token response missing access_token")
        if not isinstance(expires_in, int) or expires_in <= 0:
            raise ServiceTokenError("oauth2/token response missing/invalid expires_in")
        # Subtract a small safety margin from the refresh deadline.
        refresh_in = expires_in * REFRESH_RATIO
        self._token = _IssuedToken(
            access_token=access_token,
            expires_at_monotonic=time.monotonic() + refresh_in,
        )
        logger.info("service token issued; refresh_in=%.0fs", refresh_in)

    async def _refresh_loop(self) -> None:
        while True:
            try:
                if self._token is None:
                    await asyncio.sleep(1.0)
                    continue
                # Sleep until shortly before this token's refresh deadline.
                sleep_for = max(self._token.expires_at_monotonic - time.monotonic(), 1.0)
                await asyncio.sleep(sleep_for)
                async with self._lock:
                    await self._mint_locked()
            except asyncio.CancelledError:
                raise
            except ServiceTokenError as exc:
                logger.warning("service token refresh failed: %s; retrying in 30s", exc)
                await asyncio.sleep(30.0)
