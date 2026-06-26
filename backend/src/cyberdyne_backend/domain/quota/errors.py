"""Domain errors for server-side quota / fair-use enforcement."""

from __future__ import annotations

from datetime import datetime

from cyberdyne_backend.domain.quota.entities import QuotaMeter


class QuotaError(RuntimeError):
    """Base for quota-enforcement failures. Carries the meter, the cap that
    was hit, and when the window resets so the inbound layer can build the
    client response (paywall / throttle notice + a quota meter)."""

    def __init__(self, meter: QuotaMeter, limit: int, reset_at: datetime) -> None:
        self.meter = meter
        self.limit = limit
        self.reset_at = reset_at
        super().__init__(
            f"{meter.value} quota of {limit} reached; resets at {reset_at.isoformat()}"
        )


class FreeQuotaExceededError(QuotaError):
    """A free-tier cap was hit → the client should show the paywall (402)."""


class FairUseThrottledError(QuotaError):
    """A Pro fair-use soft cap was hit → the client should slow down (429)."""
