"""Process-scoped per-user TTL cache for course recommendations.

Course recommendations are computed once per app launch and change
rarely, yet every request pays a synchronous LLM round-trip for the
narrative summary (see ``RecommendCourses._summarize``). Caching the
whole :class:`LearningRecommendations` result for a few hours removes
that cost from the app-launch hot path.

This is a plain in-process TTL cache (no request coalescing): the call
happens roughly once per launch, so the extra complexity of coalescing
concurrent misses buys nothing. It mirrors the ``CachingChainReader`` /
``CachingAuthPort`` pattern already used in this codebase.

Caveat (issue #259): an in-process cache is per-worker. With
``uvicorn --workers N`` each worker keeps its own copy, so the hit-rate
scales down with the worker count. The Dockerfile runs a single worker
today, so the cache is effectively process-wide. Do not couple this to
#259.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from uuid import UUID

from cyberdyne_backend.application.recommendations.use_cases import LearningRecommendations


class RecommendationsCache:
    """TTL cache keyed by learner ``user_id``.

    ``time_fn`` defaults to :func:`time.monotonic` and is injectable so
    expiry can be tested without sleeping.

    Note: the key is ``user_id`` only. This flow has no locale (the
    advisor system prompt is fixed English and the router passes just the
    user id). If a locale/language parameter is ever added, it MUST be
    folded into the cache key here to avoid serving one locale's summary
    for another.
    """

    def __init__(self, *, ttl_s: float, time_fn: Callable[[], float] = time.monotonic) -> None:
        self._ttl_s = ttl_s
        self._time_fn = time_fn
        self._entries: dict[UUID, tuple[float, LearningRecommendations]] = {}

    def get(self, user_id: UUID) -> LearningRecommendations | None:
        entry = self._entries.get(user_id)
        if entry is None:
            return None
        expires_at, value = entry
        if self._time_fn() >= expires_at:
            del self._entries[user_id]
            return None
        return value

    def set(self, user_id: UUID, value: LearningRecommendations) -> None:
        self._entries[user_id] = (self._time_fn() + self._ttl_s, value)


__all__ = ["RecommendationsCache"]
