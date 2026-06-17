"""Bookmarks use cases."""

from cyberdyne_backend.application.bookmarks.use_cases import (
    DEFAULT_RECENT_LIMIT,
    MAX_RECENT_LIMIT,
    AddFavorite,
    ListFavorites,
    ListRecent,
    RecordRecentView,
    RemoveFavorite,
)

__all__ = [
    "DEFAULT_RECENT_LIMIT",
    "MAX_RECENT_LIMIT",
    "AddFavorite",
    "ListFavorites",
    "ListRecent",
    "RecordRecentView",
    "RemoveFavorite",
]
