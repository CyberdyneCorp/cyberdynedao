"""Unit tests for the sliding-window rate limiter (issue #7)."""

from __future__ import annotations

import pytest
from fastapi import HTTPException

from cyberdyne_backend.adapters.inbound.api.rate_limit import SlidingWindowRateLimiter


def test_allows_up_to_limit_then_429() -> None:
    limiter = SlidingWindowRateLimiter(limit=2, window_s=60.0)
    limiter.check("1.2.3.4", now=0.0)
    limiter.check("1.2.3.4", now=1.0)
    with pytest.raises(HTTPException) as exc:
        limiter.check("1.2.3.4", now=2.0)
    assert exc.value.status_code == 429


def test_window_slides() -> None:
    limiter = SlidingWindowRateLimiter(limit=1, window_s=10.0)
    limiter.check("ip", now=0.0)
    with pytest.raises(HTTPException):
        limiter.check("ip", now=5.0)  # still inside the window
    # Once the first hit ages out of the window, a new hit is allowed.
    limiter.check("ip", now=11.0)


def test_keys_are_independent() -> None:
    limiter = SlidingWindowRateLimiter(limit=1, window_s=60.0)
    limiter.check("a", now=0.0)
    limiter.check("b", now=0.0)  # different key — not affected by "a"
    with pytest.raises(HTTPException):
        limiter.check("a", now=1.0)


def test_none_key_is_always_allowed() -> None:
    limiter = SlidingWindowRateLimiter(limit=1, window_s=60.0)
    # A stripped proxy header → no key → the per-IP cap can't apply.
    limiter.check(None, now=0.0)
    limiter.check(None, now=1.0)
    limiter.check(None, now=2.0)


def test_custom_detail_message() -> None:
    limiter = SlidingWindowRateLimiter(limit=1, window_s=60.0, detail="slow down")
    limiter.check("ip", now=0.0)
    with pytest.raises(HTTPException) as exc:
        limiter.check("ip", now=1.0)
    assert exc.value.detail == "slow down"
