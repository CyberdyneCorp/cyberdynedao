"""Repository port for per-user usage counters."""

from __future__ import annotations

from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.quota.entities import QuotaMeter


@runtime_checkable
class UsageCounterRepository(Protocol):
    async def current(self, *, user_id: UUID, meter: QuotaMeter, period_key: str) -> int:
        """Current usage count for a user in a meter's period bucket (0 if
        none)."""
        ...

    async def increment(self, *, user_id: UUID, meter: QuotaMeter, period_key: str) -> int:
        """Atomically add one to the bucket and return the new count
        (upserts the row on first use)."""
        ...

    async def reset(self, *, user_id: UUID, meter: QuotaMeter, period_key: str) -> int:
        """Clear the bucket (delete the counter row). Returns 1 if a row
        was removed, 0 if there was nothing to reset."""
        ...
