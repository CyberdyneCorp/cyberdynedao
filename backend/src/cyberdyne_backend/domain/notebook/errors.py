"""Domain errors for the notebook context."""

from __future__ import annotations


class NoteNotFoundError(LookupError):
    """Raised when a note can't be found for the requesting user."""


class InvalidNoteError(ValueError):
    """Raised when a note fails its invariants (bad title/type)."""
