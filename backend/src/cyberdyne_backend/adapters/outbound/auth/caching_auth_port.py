"""TTL + request-coalescing decorator for ``AuthPort``.

Pattern lifted from ``geo_dashboard/backend/.../caching_auth_port.py``:

* Cache successful introspections by ``sha256(token)`` for a configurable
  TTL (default 30 s — long enough to absorb the frontend's polling
  loops, short enough that revocation latency stays bounded).
* Coalesce concurrent in-flight introspections for the same token into
  a single upstream call (5 simultaneous requests with the same token →
  1 introspect call, not 5).
* Cache only successful results — ``InvalidTokenError`` and
  ``AuthServiceUnavailableError`` go straight through so the next call
  retries upstream. No stale fallback.

In-process by design: a single Coolify replica today. When we scale
horizontally the natural upgrade is to back this with Redis.
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import time
from dataclasses import dataclass

from cyberdyne_backend.domain.auth_identity import AuthPort, Principal

logger = logging.getLogger("cyberdyne_backend.auth.cache")


@dataclass(slots=True)
class _CachedPrincipal:
    principal: Principal
    expires_at: float


class CachingAuthPort:
    """Decorates an ``AuthPort`` with a TTL cache + request coalescing."""

    def __init__(self, inner: AuthPort, ttl_s: float) -> None:
        if ttl_s <= 0:
            raise ValueError("ttl_s must be positive")
        self._inner = inner
        self._ttl = float(ttl_s)
        self._entries: dict[str, _CachedPrincipal] = {}
        # Keyed by token hash. Coalesces concurrent introspections for
        # the same token into a single upstream call.
        self._in_flight: dict[str, asyncio.Future[Principal]] = {}

    async def introspect(self, token: str) -> Principal:
        if not token:
            # Let the inner adapter own the empty-token error semantics.
            return await self._inner.introspect(token)

        key = self._key(token)
        now = time.monotonic()

        cached = self._entries.get(key)
        if cached is not None and cached.expires_at > now:
            return cached.principal
        if cached is not None:
            # Expired — drop before issuing the upstream call so the
            # entry doesn't linger if the new call fails.
            self._entries.pop(key, None)

        pending = self._in_flight.get(key)
        if pending is not None:
            return await pending

        loop = asyncio.get_running_loop()
        fut: asyncio.Future[Principal] = loop.create_future()
        self._in_flight[key] = fut
        # Leader drives the upstream call in a background task; every
        # caller (including the leader) awaits the shared future. The
        # leader pattern guarantees a single upstream call per token
        # and that any exception is always retrieved. We deliberately
        # don't keep a strong ref to the task — the future + the
        # `_in_flight` dict keep it alive for its lifetime.
        loop.create_task(self._verify_and_resolve(key, token, fut))  # noqa: RUF006
        return await fut

    async def _verify_and_resolve(
        self,
        key: str,
        token: str,
        fut: asyncio.Future[Principal],
    ) -> None:
        try:
            principal = await self._inner.introspect(token)
        except BaseException as exc:
            # Do NOT cache failures — next caller retries upstream.
            fut.set_exception(exc)
        else:
            self._entries[key] = _CachedPrincipal(
                principal=principal,
                expires_at=time.monotonic() + self._ttl,
            )
            fut.set_result(principal)
        finally:
            self._in_flight.pop(key, None)

    def invalidate(self, token: str) -> None:
        """Drop a token from the cache. Call on explicit sign-out flows."""
        self._entries.pop(self._key(token), None)

    def clear(self) -> None:
        """Drop the entire cache. Useful for tests + admin endpoints."""
        self._entries.clear()

    @staticmethod
    def _key(token: str) -> str:
        # Hash so we never hold raw bearer tokens in memory longer than
        # the introspection call itself takes.
        return hashlib.sha256(token.encode("utf-8")).hexdigest()
