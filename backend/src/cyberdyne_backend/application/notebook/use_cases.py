"""Use cases for the notebook notes CRUD (issue #161, part 1)."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from cyberdyne_backend.domain.notebook import (
    Note,
    NotebookRepository,
    NoteFields,
    NoteNotFoundError,
    NotePage,
    NoteType,
    apply_fields,
    new_note,
)

DEFAULT_NOTE_LIMIT = 20
MAX_NOTE_LIMIT = 100


@dataclass(slots=True)
class CreateNote:
    repo: NotebookRepository

    async def execute(self, *, user_id: UUID, fields: NoteFields) -> Note:
        return await self.repo.add(new_note(user_id=user_id, fields=fields))


@dataclass(slots=True)
class GetNote:
    repo: NotebookRepository

    async def execute(self, *, user_id: UUID, note_id: UUID) -> Note:
        return await self.repo.get(user_id=user_id, note_id=note_id)


@dataclass(slots=True)
class ListNotes:
    repo: NotebookRepository

    async def execute(
        self,
        *,
        user_id: UUID,
        type: NoteType | None = None,
        query: str | None = None,
        cursor: str | None = None,
        limit: int = DEFAULT_NOTE_LIMIT,
    ) -> NotePage:
        clamped = max(1, min(limit, MAX_NOTE_LIMIT))
        return await self.repo.list_for_user(
            user_id=user_id, type=type, query=query, cursor=cursor, limit=clamped
        )


@dataclass(slots=True)
class UpdateNote:
    repo: NotebookRepository

    async def execute(self, *, user_id: UUID, note_id: UUID, fields: NoteFields) -> Note:
        existing = await self.repo.get(user_id=user_id, note_id=note_id)
        return await self.repo.update(apply_fields(existing, fields))


@dataclass(slots=True)
class DeleteNote:
    repo: NotebookRepository

    async def execute(self, *, user_id: UUID, note_id: UUID) -> None:
        removed = await self.repo.delete(user_id=user_id, note_id=note_id)
        if not removed:
            raise NoteNotFoundError(f"note {note_id} not found")
