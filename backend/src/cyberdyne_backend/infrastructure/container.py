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
from cyberdyne_backend.adapters.outbound.captcha.providers import (
    AlwaysPassCaptchaProvider,
    CloudflareTurnstileProvider,
)
from cyberdyne_backend.adapters.outbound.email.notifiers import LoggingEmailNotifier
from cyberdyne_backend.domain.auth_identity import AuthPort
from cyberdyne_backend.domain.leads import CaptchaPort, EmailNotifierPort
from cyberdyne_backend.infrastructure.settings import Settings


class Container:
    """Per-process singleton of long-lived clients + adapters."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._http_client: httpx.AsyncClient | None = None
        self._auth_port: AuthPort | None = None
        self._service_token_provider: ServiceTokenProvider | None = None
        self._captcha_port: CaptchaPort | None = None
        self._email_notifier: EmailNotifierPort | None = None

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

    # ── Leads (Phase 2) ──────────────────────────────────────────────
    @property
    def captcha_port(self) -> CaptchaPort:
        if self._captcha_port is not None:
            return self._captcha_port
        provider = self._settings.captcha_provider
        if provider == "turnstile" and self._settings.captcha_secret is not None:
            self._captcha_port = CloudflareTurnstileProvider(
                secret=self._settings.captcha_secret.get_secret_value(),
                http_client=self.http_client,
                timeout_s=self._settings.cyberdyne_auth_request_timeout_s,
            )
        else:
            # Default: always-pass. Logs a warning in non-local envs so a
            # misconfigured production deploy doesn't silently accept
            # any body.
            self._captcha_port = AlwaysPassCaptchaProvider(environment=self._settings.environment)
        return self._captcha_port

    @property
    def email_notifier(self) -> EmailNotifierPort:
        if self._email_notifier is None:
            # Only logger-backed in Phase 2; real SMTP / Postmark lands
            # when the provider is provisioned.
            self._email_notifier = LoggingEmailNotifier()
        return self._email_notifier

    async def aclose(self) -> None:
        if self._service_token_provider is not None:
            await self._service_token_provider.stop()
        if self._http_client is not None:
            await self._http_client.aclose()
