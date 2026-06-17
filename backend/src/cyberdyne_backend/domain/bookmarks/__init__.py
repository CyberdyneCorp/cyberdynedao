"""Bookmarks bounded context.

Learner-scoped favorites/bookmarks plus a recently-viewed history.
Surfaced by the redesigned client sidebar (Saved / Recent / Add to
Favorites). See issue #162.
"""

from cyberdyne_backend.domain.bookmarks.entities import (
    BookmarkType,
    Favorite,
    RecentView,
    new_favorite,
    new_recent_view,
    parse_bookmark_type,
)
from cyberdyne_backend.domain.bookmarks.errors import (
    FavoriteNotFoundError,
    InvalidBookmarkTypeError,
)
from cyberdyne_backend.domain.bookmarks.ports import BookmarkRepository

__all__ = [
    "BookmarkRepository",
    "BookmarkType",
    "Favorite",
    "FavoriteNotFoundError",
    "InvalidBookmarkTypeError",
    "RecentView",
    "new_favorite",
    "new_recent_view",
    "parse_bookmark_type",
]
