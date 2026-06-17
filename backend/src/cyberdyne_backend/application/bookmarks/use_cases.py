"""Use cases for favorites/bookmarks + recently-viewed."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from cyberdyne_backend.domain.bookmarks.entities import (
    BookmarkType,
    Favorite,
    RecentView,
    new_favorite,
    new_recent_view,
)
from cyberdyne_backend.domain.bookmarks.errors import FavoriteNotFoundError
from cyberdyne_backend.domain.bookmarks.ports import BookmarkRepository

# Caps the recently-viewed page so a single request can't pull an
# unbounded history. Mirrors the client's short "Recent" list.
DEFAULT_RECENT_LIMIT = 20
MAX_RECENT_LIMIT = 100


@dataclass(slots=True)
class ListFavorites:
    repo: BookmarkRepository

    async def execute(self, user_id: UUID) -> list[Favorite]:
        return await self.repo.list_favorites_for_user(user_id)


@dataclass(slots=True)
class AddFavorite:
    """Idempotent on (user_id, type, ref)."""

    repo: BookmarkRepository

    async def execute(self, *, user_id: UUID, type: BookmarkType, ref: str) -> Favorite:
        candidate = new_favorite(user_id=user_id, type=type, ref=ref)
        return await self.repo.add_favorite(candidate)


@dataclass(slots=True)
class RemoveFavorite:
    repo: BookmarkRepository

    async def execute(self, *, user_id: UUID, favorite_id: UUID) -> None:
        removed = await self.repo.remove_favorite(user_id=user_id, favorite_id=favorite_id)
        if not removed:
            raise FavoriteNotFoundError(f"favorite {favorite_id} not found")


@dataclass(slots=True)
class RecordRecentView:
    """Upserts on (user_id, type, ref); re-viewing bumps the timestamp."""

    repo: BookmarkRepository

    async def execute(self, *, user_id: UUID, type: BookmarkType, ref: str) -> RecentView:
        candidate = new_recent_view(user_id=user_id, type=type, ref=ref)
        return await self.repo.record_recent_view(candidate)


@dataclass(slots=True)
class ListRecent:
    repo: BookmarkRepository

    async def execute(
        self, user_id: UUID, *, limit: int = DEFAULT_RECENT_LIMIT
    ) -> list[RecentView]:
        clamped = max(1, min(limit, MAX_RECENT_LIMIT))
        return await self.repo.list_recent_for_user(user_id, limit=clamped)
