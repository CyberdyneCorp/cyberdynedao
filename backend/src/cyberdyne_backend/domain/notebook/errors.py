"""Domain errors for the notebook context."""

from __future__ import annotations


class NoteNotFoundError(LookupError):
    """Raised when a note can't be found for the requesting user."""


class InvalidNoteError(ValueError):
    """Raised when a note fails its invariants (bad title/type)."""


class FlashcardNotFoundError(LookupError):
    """Raised when a flashcard can't be found on the user's note."""


class InvalidFlashcardError(ValueError):
    """Raised when a flashcard fails its invariants (empty question/answer)."""
