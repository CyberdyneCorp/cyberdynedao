"""Thin DI container.

Not a framework — just lazily-cached factories so adapters share
``httpx`` clients and caches. Same shape as ``geo_dashboard``'s
container module: explicit, testable, no magic.
"""

from __future__ import annotations

import httpx

from cyberdyne_backend.adapters.outbound.auth.caching_auth_port import CachingAuthPort
from cyberdyne_backend.adapters.outbound.auth.introspection_client import IntrospectionClient
from cyberdyne_backend.adapters.outbound.auth.service_token_provider import ServiceTokenProvider
from cyberdyne_backend.domain.auth_identity import AuthPort
from cyberdyne_backend.infrastructure.settings import Settings


class Container:
    """Per-process singleton of long-lived clients + adapters."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._http_client: httpx.AsyncClient | None = None
        self._auth_port: AuthPort | None = None
        self._service_token_provider: ServiceTokenProvider | None = None

    # ── HTTP ──────────────────────────────────────────────────────────
    @property
    def http_client(self) -> httpx.AsyncClient:
        if self._http_client is None:
            # Single client; connection pool reused across all outbound
            # adapters that don't bring their own.
            self._http_client = httpx.AsyncClient(
                timeout=httpx.Timeout(10.0, connect=5.0),
                limits=httpx.Limits(max_connections=64, max_keepalive_connections=16),
            )
        return self._http_client

    # ── Auth ──────────────────────────────────────────────────────────
    @property
    def auth_port(self) -> AuthPort:
        if self._auth_port is None:
            inner = IntrospectionClient(
                base_url=str(self._settings.cyberdyne_auth_base_url),
                http_client=self.http_client,
                timeout_s=self._settings.cyberdyne_auth_request_timeout_s,
            )
            self._auth_port = CachingAuthPort(
                inner=inner,
                ttl_s=self._settings.cyberdyne_auth_introspection_ttl_s,
            )
        return self._auth_port

    @property
    def service_token_provider(self) -> ServiceTokenProvider | None:
        """``None`` until the backend is registered as an OAuth client.

        Phase 1's public endpoints don't need an outbound bearer; the
        provider only spins up when both ``CYBERDYNE_AUTH_CLIENT_ID``
        and ``CYBERDYNE_AUTH_CLIENT_SECRET`` are set.
        """
        if self._service_token_provider is not None:
            return self._service_token_provider
        client_id = self._settings.cyberdyne_auth_client_id
        secret = self._settings.cyberdyne_auth_client_secret
        if not client_id or secret is None:
            return None
        self._service_token_provider = ServiceTokenProvider(
            base_url=str(self._settings.cyberdyne_auth_base_url),
            client_id=client_id,
            client_secret=secret.get_secret_value(),
            http_client=self.http_client,
            scopes=self._settings.cyberdyne_auth_oauth_scopes,
            audience=self._settings.cyberdyne_auth_oauth_audience,
            timeout_s=self._settings.cyberdyne_auth_request_timeout_s,
        )
        return self._service_token_provider

    async def aclose(self) -> None:
        if self._service_token_provider is not None:
            await self._service_token_provider.stop()
        if self._http_client is not None:
            await self._http_client.aclose()
