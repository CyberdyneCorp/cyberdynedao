"""In-memory per-key sliding-window rate limiter for inbound routes.

A coarse abuse/cost guard, NOT a distributed quota: state is per-replica
and resets on restart. Used to cap chat turns so a single client can't
burn LLM tokens in a loop (issue #7).
"""

from __future__ import annotations

import time

from fastapi import HTTPException


class SlidingWindowRateLimiter:
    """Allow at most ``limit`` events per ``window_s`` seconds per key."""

    def __init__(
        self,
        *,
        limit: int,
        window_s: float,
        detail: str = "rate limit exceeded; slow down",
    ) -> None:
        self._limit = limit
        self._window_s = window_s
        self._detail = detail
        self._hits: dict[str, list[float]] = {}

    def check(self, key: str | None, *, now: float | None = None) -> None:
        """Record a hit for ``key`` and raise ``HTTPException(429)`` if it
        exceeds the limit. A ``None`` key (e.g. a stripped proxy header)
        is allowed through — the per-IP cap can't apply without an IP."""
        if key is None:
            return
        moment = now if now is not None else time.monotonic()
        bucket = self._hits.setdefault(key, [])
        cutoff = moment - self._window_s
        bucket[:] = [t for t in bucket if t > cutoff]
        if len(bucket) >= self._limit:
            raise HTTPException(status_code=429, detail=self._detail)
        bucket.append(moment)
