"""Repository port for the bookmarks context."""

from __future__ import annotations

from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.bookmarks.entities import Favorite, RecentView


@runtime_checkable
class BookmarkRepository(Protocol):
    # ── Favorites ─────────────────────────────────────────────────────
    async def add_favorite(self, favorite: Favorite) -> Favorite:
        """Persist a favorite. Idempotent on ``(user_id, type, ref)`` —
        returns the existing favorite if one already exists."""
        ...

    async def list_favorites_for_user(self, user_id: UUID) -> list[Favorite]:
        """Favorites for a user, newest first."""
        ...

    async def remove_favorite(self, *, user_id: UUID, favorite_id: UUID) -> bool:
        """Delete a favorite owned by the user. Returns ``True`` if a row
        was removed, ``False`` if nothing matched."""
        ...

    # ── Recently viewed ───────────────────────────────────────────────
    async def record_recent_view(self, view: RecentView) -> RecentView:
        """Record (or bump) a recently-viewed item. Upserts on
        ``(user_id, type, ref)`` — re-viewing updates ``viewed_at``."""
        ...

    async def list_recent_for_user(
        self, user_id: UUID, *, limit: int
    ) -> list[RecentView]:
        """Recently-viewed items for a user, most-recent first."""
        ...
