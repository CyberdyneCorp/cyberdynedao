"""Domain errors for the activity context."""

from __future__ import annotations


class InvalidActivityKindError(ValueError):
    """Raised when an unknown activity kind is supplied."""
