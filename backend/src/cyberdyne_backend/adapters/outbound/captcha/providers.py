"""Captcha adapters implementing ``CaptchaPort``.

Phase 2 ships two concrete adapters:

- ``AlwaysPassCaptchaProvider`` — accepts any non-empty token. Used
  in local dev, tests, and as the safe default if no captcha provider
  is configured. Logs a warning when running in non-local environments
  so misconfiguration is loud.

- ``CloudflareTurnstileProvider`` — calls Cloudflare's siteverify
  endpoint. Pure adapter, no domain dependency beyond ``CaptchaPort``.

Selection happens in the container based on ``CAPTCHA_PROVIDER`` env.
"""

from __future__ import annotations

import logging

import httpx

from cyberdyne_backend.domain.leads import CaptchaVerificationError

logger = logging.getLogger("cyberdyne_backend.captcha")

TURNSTILE_VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


class AlwaysPassCaptchaProvider:
    """Accepts any non-empty token. Safe for dev / tests."""

    def __init__(self, environment: str = "local") -> None:
        self._environment = environment

    async def verify(self, token: str, remote_ip: str | None) -> None:
        if self._environment in ("staging", "production"):
            logger.warning(
                "AlwaysPassCaptchaProvider is active in %s — set CAPTCHA_PROVIDER=turnstile",
                self._environment,
            )
        if not token:
            raise CaptchaVerificationError("captcha token missing")


class CloudflareTurnstileProvider:
    """Real Cloudflare Turnstile siteverify call."""

    def __init__(
        self,
        secret: str,
        http_client: httpx.AsyncClient,
        timeout_s: float = 5.0,
    ) -> None:
        self._secret = secret
        self._http = http_client
        self._timeout = timeout_s

    async def verify(self, token: str, remote_ip: str | None) -> None:
        if not token:
            raise CaptchaVerificationError("captcha token missing")
        data = {"secret": self._secret, "response": token}
        if remote_ip:
            data["remoteip"] = remote_ip
        try:
            response = await self._http.post(
                TURNSTILE_VERIFY_URL,
                data=data,
                timeout=self._timeout,
            )
        except httpx.HTTPError as exc:
            raise CaptchaVerificationError(f"transport error verifying captcha: {exc}") from exc
        if response.status_code != 200:
            raise CaptchaVerificationError(f"turnstile siteverify returned {response.status_code}")
        body = response.json()
        if not body.get("success"):
            raise CaptchaVerificationError(
                f"turnstile rejected token: {body.get('error-codes', [])}"
            )
