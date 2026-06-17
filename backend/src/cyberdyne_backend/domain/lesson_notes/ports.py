"""Repository port for the lesson-notes context."""

from __future__ import annotations

from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.lesson_notes.entities import LessonNote, LessonNotePage


@runtime_checkable
class LessonNoteRepository(Protocol):
    async def upsert(self, note: LessonNote) -> bool:
        """Insert the note, or update it in place if one with the same
        ``(user_id, id)`` already exists (idempotent client-supplied id).
        Returns ``True`` if a new row was created, ``False`` if updated."""
        ...

    async def get(self, *, user_id: UUID, note_id: UUID) -> LessonNote:
        """Load a note owned by the user. Raises ``LessonNoteNotFoundError``."""
        ...

    async def list_for_lesson(self, *, user_id: UUID, lesson_id: str) -> list[LessonNote]:
        """The user's notes for one lesson, newest first."""
        ...

    async def list_for_user(
        self,
        *,
        user_id: UUID,
        course_slug: str | None = None,
        cursor: str | None = None,
        limit: int = 50,
    ) -> LessonNotePage:
        """The user's notes (optionally a single course), newest first,
        keyset-paged for export/search."""
        ...

    async def update(self, note: LessonNote) -> LessonNote:
        """Persist edits to an existing note. Raises
        ``LessonNoteNotFoundError`` if absent for the user."""
        ...

    async def delete(self, *, user_id: UUID, note_id: UUID) -> bool:
        """Delete a note owned by the user. Returns ``True`` if removed."""
        ...
