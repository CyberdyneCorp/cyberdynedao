"""Repository port for the notebook context."""

from __future__ import annotations

from datetime import datetime
from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.notebook.entities import (
    Flashcard,
    Note,
    NotePage,
    NoteType,
)


@runtime_checkable
class NotebookRepository(Protocol):
    async def add(self, note: Note) -> Note:
        """Persist a new note."""
        ...

    async def get(self, *, user_id: UUID, note_id: UUID) -> Note:
        """Load a note owned by the user. Raises ``NoteNotFoundError``."""
        ...

    async def list_for_user(
        self,
        *,
        user_id: UUID,
        type: NoteType | None = None,
        query: str | None = None,
        due: bool = False,
        now: datetime | None = None,
        cursor: str | None = None,
        limit: int = 20,
    ) -> NotePage:
        """List the user's notes newest-first, optionally filtered by type,
        a title/body substring, and (when ``due``) only notes whose
        ``next_review_at`` is at or before ``now``. Paged with an opaque
        keyset cursor."""
        ...

    async def update(self, note: Note) -> Note:
        """Persist changes to an existing note. Raises ``NoteNotFoundError``
        if it doesn't exist for the user."""
        ...

    async def delete(self, *, user_id: UUID, note_id: UUID) -> bool:
        """Delete a note owned by the user. Returns ``True`` if removed."""
        ...

    # ── Flashcards (the caller verifies note ownership first) ──────────
    async def add_flashcard(self, flashcard: Flashcard) -> Flashcard:
        """Persist a flashcard against its note."""
        ...

    async def list_flashcards(self, note_id: UUID) -> list[Flashcard]:
        """Flashcards for a note, oldest first."""
        ...

    async def delete_flashcard(self, *, note_id: UUID, flashcard_id: UUID) -> bool:
        """Delete a flashcard from a note. Returns ``True`` if removed."""
        ...
