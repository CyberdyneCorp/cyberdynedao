"""SQLAlchemy adapter for ``BookmarkRepository``."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.bookmarks.models import (
    FavoriteRow,
    RecentViewRow,
)
from cyberdyne_backend.domain.bookmarks import (
    BookmarkType,
    Favorite,
    RecentView,
)


def _as_utc(value: datetime) -> datetime:
    """SQLite drops tzinfo on read; re-attach UTC. Postgres is already
    aware, so this is a no-op there."""
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value


def _row_to_favorite(row: FavoriteRow) -> Favorite:
    return Favorite(
        id=row.id,
        user_id=row.user_id,
        type=BookmarkType(row.type),
        ref=row.ref,
        added_at=_as_utc(row.added_at),
    )


def _row_to_recent(row: RecentViewRow) -> RecentView:
    return RecentView(
        id=row.id,
        user_id=row.user_id,
        type=BookmarkType(row.type),
        ref=row.ref,
        viewed_at=_as_utc(row.viewed_at),
    )


class SqlAlchemyBookmarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # ── Favorites ─────────────────────────────────────────────────────
    async def add_favorite(self, favorite: Favorite) -> Favorite:
        existing = (
            await self._session.execute(
                select(FavoriteRow).where(
                    FavoriteRow.user_id == favorite.user_id,
                    FavoriteRow.type == favorite.type.value,
                    FavoriteRow.ref == favorite.ref,
                )
            )
        ).scalar_one_or_none()
        if existing is not None:
            return _row_to_favorite(existing)

        self._session.add(
            FavoriteRow(
                id=favorite.id,
                user_id=favorite.user_id,
                type=favorite.type.value,
                ref=favorite.ref,
                added_at=favorite.added_at,
            )
        )
        await self._session.flush()
        return favorite

    async def list_favorites_for_user(self, user_id: UUID) -> list[Favorite]:
        rows = (
            (
                await self._session.execute(
                    select(FavoriteRow)
                    .where(FavoriteRow.user_id == user_id)
                    .order_by(FavoriteRow.added_at.desc())
                )
            )
            .scalars()
            .all()
        )
        return [_row_to_favorite(r) for r in rows]

    async def remove_favorite(self, *, user_id: UUID, favorite_id: UUID) -> bool:
        result = await self._session.execute(
            delete(FavoriteRow).where(
                FavoriteRow.id == favorite_id,
                FavoriteRow.user_id == user_id,
            )
        )
        await self._session.flush()
        return (result.rowcount or 0) > 0

    # ── Recently viewed ───────────────────────────────────────────────
    async def record_recent_view(self, view: RecentView) -> RecentView:
        existing = (
            await self._session.execute(
                select(RecentViewRow).where(
                    RecentViewRow.user_id == view.user_id,
                    RecentViewRow.type == view.type.value,
                    RecentViewRow.ref == view.ref,
                )
            )
        ).scalar_one_or_none()
        if existing is not None:
            existing.viewed_at = view.viewed_at
            await self._session.flush()
            return _row_to_recent(existing)

        self._session.add(
            RecentViewRow(
                id=view.id,
                user_id=view.user_id,
                type=view.type.value,
                ref=view.ref,
                viewed_at=view.viewed_at,
            )
        )
        await self._session.flush()
        return view

    async def list_recent_for_user(
        self, user_id: UUID, *, limit: int
    ) -> list[RecentView]:
        rows = (
            (
                await self._session.execute(
                    select(RecentViewRow)
                    .where(RecentViewRow.user_id == user_id)
                    .order_by(RecentViewRow.viewed_at.desc())
                    .limit(limit)
                )
            )
            .scalars()
            .all()
        )
        return [_row_to_recent(r) for r in rows]
