"""Repository port for the notebook context."""

from __future__ import annotations

from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.notebook.entities import Note, NotePage, NoteType


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
        cursor: str | None = None,
        limit: int = 20,
    ) -> NotePage:
        """List the user's notes newest-first, optionally filtered by type
        and a title/body substring, paged with an opaque keyset cursor."""
        ...

    async def update(self, note: Note) -> Note:
        """Persist changes to an existing note. Raises ``NoteNotFoundError``
        if it doesn't exist for the user."""
        ...

    async def delete(self, *, user_id: UUID, note_id: UUID) -> bool:
        """Delete a note owned by the user. Returns ``True`` if removed."""
        ...
