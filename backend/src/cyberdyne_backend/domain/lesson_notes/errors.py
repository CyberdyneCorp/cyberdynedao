"""Domain errors for the lesson-notes context."""

from __future__ import annotations


class LessonNoteNotFoundError(LookupError):
    """Raised when a lesson note can't be found for the requesting user."""


class InvalidLessonNoteError(ValueError):
    """Raised when a lesson note fails its invariants."""
