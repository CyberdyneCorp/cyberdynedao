"""Entities for the bookmarks context — favorites + recently-viewed."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID

from cyberdyne_backend.domain.bookmarks.errors import InvalidBookmarkTypeError


class BookmarkType(StrEnum):
    """What a favorite/recent entry points at."""

    COURSE = "course"
    LESSON = "lesson"
    NOTE = "note"


def parse_bookmark_type(raw: str) -> BookmarkType:
    try:
        return BookmarkType(raw)
    except ValueError as exc:
        allowed = ", ".join(t.value for t in BookmarkType)
        raise InvalidBookmarkTypeError(
            f"unknown bookmark type {raw!r}; expected one of: {allowed}"
        ) from exc


@dataclass(slots=True)
class Favorite:
    """A learner-scoped favorite/bookmark.

    Uniquely identified per user by ``(type, ref)`` — favoriting the same
    item twice is idempotent (the persistence adapter upserts).
    """

    id: UUID
    user_id: UUID
    type: BookmarkType
    ref: str
    added_at: datetime


@dataclass(slots=True)
class RecentView:
    """A learner's most-recent access of an item.

    Keyed per user by ``(type, ref)``; re-viewing an item bumps
    ``viewed_at`` rather than creating a duplicate row.
    """

    id: UUID
    user_id: UUID
    type: BookmarkType
    ref: str
    viewed_at: datetime


def new_favorite(
    *,
    user_id: UUID,
    type: BookmarkType,
    ref: str,
    now: datetime | None = None,
) -> Favorite:
    return Favorite(
        id=uuid.uuid4(),
        user_id=user_id,
        type=type,
        ref=ref,
        added_at=now or datetime.now(tz=UTC),
    )


def new_recent_view(
    *,
    user_id: UUID,
    type: BookmarkType,
    ref: str,
    now: datetime | None = None,
) -> RecentView:
    return RecentView(
        id=uuid.uuid4(),
        user_id=user_id,
        type=type,
        ref=ref,
        viewed_at=now or datetime.now(tz=UTC),
    )
