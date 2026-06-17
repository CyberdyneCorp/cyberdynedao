"""Notebook use cases."""

from cyberdyne_backend.application.notebook.ai_use_cases import (
    MAX_GENERATED_FLASHCARDS,
    GenerateFlashcards,
    SummarizeNote,
)
from cyberdyne_backend.application.notebook.use_cases import (
    DEFAULT_NOTE_LIMIT,
    MAX_NOTE_LIMIT,
    AddFlashcard,
    CreateNote,
    DeleteFlashcard,
    DeleteNote,
    GetNote,
    ListFlashcards,
    ListNotes,
    ReviewNote,
    UpdateNote,
)

__all__ = [
    "DEFAULT_NOTE_LIMIT",
    "MAX_GENERATED_FLASHCARDS",
    "MAX_NOTE_LIMIT",
    "AddFlashcard",
    "CreateNote",
    "DeleteFlashcard",
    "DeleteNote",
    "GenerateFlashcards",
    "GetNote",
    "ListFlashcards",
    "ListNotes",
    "ReviewNote",
    "SummarizeNote",
    "UpdateNote",
]
