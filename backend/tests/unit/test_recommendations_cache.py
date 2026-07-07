"""Unit tests for the RecommendationsCache TTL primitive."""

from __future__ import annotations

import uuid

from cyberdyne_backend.application.recommendations import (
    LearningRecommendations,
    RecommendationsCache,
)
from cyberdyne_backend.infrastructure.container import Container
from cyberdyne_backend.infrastructure.settings import Settings


class _Clock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


def _payload(summary: str) -> LearningRecommendations:
    return LearningRecommendations(summary=summary, courses=[])


def test_miss_then_set_then_hit() -> None:
    cache = RecommendationsCache(ttl_s=100)
    user_id = uuid.uuid4()
    assert cache.get(user_id) is None  # miss

    value = _payload("hi")
    cache.set(user_id, value)
    assert cache.get(user_id) is value  # hit


def test_entry_expires_after_ttl() -> None:
    clock = _Clock()
    cache = RecommendationsCache(ttl_s=100, time_fn=clock)
    user_id = uuid.uuid4()
    cache.set(user_id, _payload("hi"))

    clock.now = 99.0
    assert cache.get(user_id) is not None  # still fresh

    clock.now = 100.0  # at/after expiry
    assert cache.get(user_id) is None


def test_keys_are_isolated_per_user() -> None:
    cache = RecommendationsCache(ttl_s=100)
    a, b = uuid.uuid4(), uuid.uuid4()
    cache.set(a, _payload("a"))
    assert cache.get(b) is None
    assert cache.get(a) is not None


def test_container_recommendations_cache_is_a_memoized_singleton() -> None:
    container = Container(Settings())
    first = container.recommendations_cache
    assert isinstance(first, RecommendationsCache)
    assert container.recommendations_cache is first  # same instance reused
