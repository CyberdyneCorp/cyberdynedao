"""Notebook bounded context.

The learner's per-user "living memory": saved notes (concepts, executed
code + run results/plots, AI summaries, theory, problems). This slice
covers the core note model + CRUD; flashcards and spaced-review
scheduling land in follow-ups. See issue #161.
"""

from cyberdyne_backend.domain.notebook.entities import (
    Flashcard,
    Note,
    NoteFields,
    NotePage,
    NoteType,
    apply_fields,
    new_flashcard,
    new_note,
    parse_note_type,
)
from cyberdyne_backend.domain.notebook.errors import (
    FlashcardNotFoundError,
    InvalidFlashcardError,
    InvalidNoteError,
    NoteNotFoundError,
)
from cyberdyne_backend.domain.notebook.ports import NotebookRepository

__all__ = [
    "Flashcard",
    "FlashcardNotFoundError",
    "InvalidFlashcardError",
    "InvalidNoteError",
    "Note",
    "NoteFields",
    "NoteNotFoundError",
    "NotePage",
    "NoteType",
    "NotebookRepository",
    "apply_fields",
    "new_flashcard",
    "new_note",
    "parse_note_type",
]
