"""Notebook bounded context.

The learner's per-user "living memory": saved notes (concepts, executed
code + run results/plots, AI summaries, theory, problems), plus
auto/authored flashcards and a spaced-review schedule per note. See
issue #161.
"""

from cyberdyne_backend.domain.notebook.entities import (
    Flashcard,
    Note,
    NoteFields,
    NotePage,
    NoteType,
    ReviewRating,
    apply_fields,
    new_flashcard,
    new_note,
    next_interval_days,
    parse_note_type,
    parse_review_rating,
    record_review,
)
from cyberdyne_backend.domain.notebook.errors import (
    FlashcardNotFoundError,
    InvalidFlashcardError,
    InvalidNoteError,
    InvalidReviewError,
    NoteNotFoundError,
)
from cyberdyne_backend.domain.notebook.ports import NotebookRepository

__all__ = [
    "Flashcard",
    "FlashcardNotFoundError",
    "InvalidFlashcardError",
    "InvalidNoteError",
    "InvalidReviewError",
    "Note",
    "NoteFields",
    "NoteNotFoundError",
    "NotePage",
    "NoteType",
    "NotebookRepository",
    "ReviewRating",
    "apply_fields",
    "new_flashcard",
    "new_note",
    "next_interval_days",
    "parse_note_type",
    "parse_review_rating",
    "record_review",
]
