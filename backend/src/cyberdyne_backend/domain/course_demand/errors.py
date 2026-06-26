"""Domain errors for the course-demand context."""

from __future__ import annotations


class InvalidRequestSourceError(ValueError):
    """Raised when an unknown course-request source is supplied."""
