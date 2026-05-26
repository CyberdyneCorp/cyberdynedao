"""Domain errors for the leads context."""

from __future__ import annotations


class AskNotFoundError(LookupError):
    """No ask with the requested id exists."""


class AskTransitionError(ValueError):
    """Invalid state machine transition (or empty note text)."""
