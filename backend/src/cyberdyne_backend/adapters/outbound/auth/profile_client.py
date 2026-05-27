"""CyberdyneAuth ``GET /users/me`` profile client.

Best-effort enrichment, not an auth gate: the chat agent uses it to
personalize replies and pre-fill leads. Any upstream failure resolves
to ``None`` so the chat turn proceeds anonymously rather than 5xx-ing.

In-process TTL cache keyed by ``sha256(token)`` (same rationale as the
introspection cache — absorb the frontend's per-turn calls without
hammering CyberdyneAuth). When we scale horizontally this moves to
Redis alongside the introspection cache.
"""

from __future__ import annotations

import hashlib
import logging
import time

import httpx

from cyberdyne_backend.domain.auth_identity import UserProfile, profile_from_users_me

logger = logging.getLogger("cyberdyne_backend.auth.profile")

USERS_ME_PATH = "/api/v1/users/me"


class CyberdyneAuthProfileClient:
    def __init__(
        self,
        base_url: str,
        http_client: httpx.AsyncClient,
        ttl_s: float = 60.0,
        timeout_s: float = 5.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._http = http_client
        self._ttl = float(ttl_s)
        self._timeout = timeout_s
        self._cache: dict[str, tuple[UserProfile | None, float]] = {}

    async def get_profile(self, token: str) -> UserProfile | None:
        if not token:
            return None
        key = hashlib.sha256(token.encode("utf-8")).hexdigest()
        now = time.monotonic()
        cached = self._cache.get(key)
        if cached is not None and cached[1] > now:
            return cached[0]

        profile = await self._fetch(token)
        # Cache both hits and misses for the TTL — a miss is usually a
        # service token or an unverified account, neither of which flips
        # within a chat session.
        self._cache[key] = (profile, now + self._ttl)
        return profile

    async def _fetch(self, token: str) -> UserProfile | None:
        url = f"{self._base_url}{USERS_ME_PATH}"
        try:
            response = await self._http.get(
                url,
                headers={"Authorization": f"Bearer {token}"},
                timeout=self._timeout,
            )
        except httpx.HTTPError as exc:
            logger.warning("profile fetch transport error: %s", exc)
            return None
        if response.status_code != 200:
            logger.info("profile fetch non-200: %s", response.status_code)
            return None
        try:
            return profile_from_users_me(response.json())
        except ValueError:
            logger.warning("profile fetch returned non-JSON body")
            return None
