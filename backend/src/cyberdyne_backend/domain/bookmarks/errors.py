"""Domain errors for the bookmarks context."""

from __future__ import annotations


class FavoriteNotFoundError(LookupError):
    """Raised when a favorite cannot be found for the requesting user."""


class InvalidBookmarkTypeError(ValueError):
    """Raised when an unknown favorite/recent type is supplied."""
