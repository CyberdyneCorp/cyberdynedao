"""Domain errors for the learner-feedback context."""

from __future__ import annotations


class InvalidFeedbackKindError(ValueError):
    """Raised when an unknown feedback kind is supplied."""


class InvalidFeedbackStatusError(ValueError):
    """Raised when an unknown feedback status is supplied."""
