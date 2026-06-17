"""Unit tests for favorites/recently-viewed use cases (issue #162)."""

from __future__ import annotations

import asyncio
import uuid

import pytest

from cyberdyne_backend.application.bookmarks import (
    AddFavorite,
    ListFavorites,
    ListRecent,
    RecordRecentView,
    RemoveFavorite,
)
from cyberdyne_backend.domain.bookmarks import (
    BookmarkType,
    Favorite,
    FavoriteNotFoundError,
    RecentView,
)


class _FakeRepo:
    def __init__(self) -> None:
        self.favorites: list[Favorite] = []
        self.recent: list[RecentView] = []

    async def add_favorite(self, favorite: Favorite) -> Favorite:
        for existing in self.favorites:
            if (
                existing.user_id == favorite.user_id
                and existing.type == favorite.type
                and existing.ref == favorite.ref
            ):
                return existing
        self.favorites.append(favorite)
        return favorite

    async def list_favorites_for_user(self, user_id: uuid.UUID) -> list[Favorite]:
        rows = [f for f in self.favorites if f.user_id == user_id]
        return sorted(rows, key=lambda f: f.added_at, reverse=True)

    async def remove_favorite(
        self, *, user_id: uuid.UUID, favorite_id: uuid.UUID
    ) -> bool:
        before = len(self.favorites)
        self.favorites = [
            f
            for f in self.favorites
            if not (f.id == favorite_id and f.user_id == user_id)
        ]
        return len(self.favorites) < before

    async def record_recent_view(self, view: RecentView) -> RecentView:
        for existing in self.recent:
            if (
                existing.user_id == view.user_id
                and existing.type == view.type
                and existing.ref == view.ref
            ):
                existing.viewed_at = view.viewed_at
                return existing
        self.recent.append(view)
        return view

    async def list_recent_for_user(
        self, user_id: uuid.UUID, *, limit: int
    ) -> list[RecentView]:
        rows = [v for v in self.recent if v.user_id == user_id]
        rows.sort(key=lambda v: v.viewed_at, reverse=True)
        return rows[:limit]


def test_add_favorite_is_idempotent() -> None:
    repo = _FakeRepo()
    uc = AddFavorite(repo=repo)
    user = uuid.uuid4()

    first = asyncio.run(
        uc.execute(user_id=user, type=BookmarkType.COURSE, ref="quantum-101")
    )
    second = asyncio.run(
        uc.execute(user_id=user, type=BookmarkType.COURSE, ref="quantum-101")
    )

    assert first.id == second.id
    assert len(repo.favorites) == 1


def test_list_favorites_is_user_scoped() -> None:
    repo = _FakeRepo()
    me, other = uuid.uuid4(), uuid.uuid4()
    asyncio.run(AddFavorite(repo=repo).execute(user_id=me, type=BookmarkType.COURSE, ref="a"))
    asyncio.run(
        AddFavorite(repo=repo).execute(user_id=other, type=BookmarkType.COURSE, ref="b")
    )

    mine = asyncio.run(ListFavorites(repo=repo).execute(me))
    assert [f.ref for f in mine] == ["a"]


def test_remove_missing_favorite_raises() -> None:
    repo = _FakeRepo()
    uc = RemoveFavorite(repo=repo)
    with pytest.raises(FavoriteNotFoundError):
        asyncio.run(uc.execute(user_id=uuid.uuid4(), favorite_id=uuid.uuid4()))


def test_record_recent_bumps_existing() -> None:
    repo = _FakeRepo()
    uc = RecordRecentView(repo=repo)
    user = uuid.uuid4()

    first = asyncio.run(uc.execute(user_id=user, type=BookmarkType.LESSON, ref="l1"))
    second = asyncio.run(uc.execute(user_id=user, type=BookmarkType.LESSON, ref="l1"))

    assert len(repo.recent) == 1
    assert second.viewed_at >= first.viewed_at


def test_list_recent_clamps_limit() -> None:
    repo = _FakeRepo()
    user = uuid.uuid4()
    for i in range(5):
        asyncio.run(
            RecordRecentView(repo=repo).execute(
                user_id=user, type=BookmarkType.NOTE, ref=f"n{i}"
            )
        )

    # Over-large limits are clamped down to the available rows; a
    # non-positive limit is clamped up to at least one row.
    capped = asyncio.run(ListRecent(repo=repo).execute(user, limit=9999))
    assert len(capped) == 5
    at_least_one = asyncio.run(ListRecent(repo=repo).execute(user, limit=0))
    assert len(at_least_one) == 1
