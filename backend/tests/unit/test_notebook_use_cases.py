"""Unit tests for notebook notes domain + use cases (issue #161)."""

from __future__ import annotations

import asyncio
import uuid

import pytest

from cyberdyne_backend.application.notebook import (
    CreateNote,
    DeleteNote,
    GetNote,
    ListNotes,
    UpdateNote,
)
from cyberdyne_backend.domain.notebook import (
    InvalidNoteError,
    Note,
    NoteFields,
    NoteNotFoundError,
    NotePage,
    NoteType,
    new_note,
)


def _fields(title: str = "My Note", type_: NoteType = NoteType.CODE) -> NoteFields:
    return NoteFields(title=title, type=type_, body="b")


def test_new_note_validates_title() -> None:
    with pytest.raises(InvalidNoteError):
        new_note(user_id=uuid.uuid4(), fields=_fields(title="   "))


def test_new_note_trims_title_and_stamps() -> None:
    n = new_note(user_id=uuid.uuid4(), fields=_fields(title="  Trig  "))
    assert n.title == "Trig"
    assert n.updated_at is not None


class _FakeRepo:
    def __init__(self) -> None:
        self.notes: dict[uuid.UUID, Note] = {}

    async def add(self, note: Note) -> Note:
        self.notes[note.id] = note
        return note

    async def get(self, *, user_id, note_id) -> Note:
        n = self.notes.get(note_id)
        if n is None or n.user_id != user_id:
            raise NoteNotFoundError(str(note_id))
        return n

    async def update(self, note: Note) -> Note:
        self.notes[note.id] = note
        return note

    async def delete(self, *, user_id, note_id) -> bool:
        n = self.notes.get(note_id)
        if n is None or n.user_id != user_id:
            return False
        del self.notes[note_id]
        return True

    async def list_for_user(
        self, *, user_id, type=None, query=None, cursor=None, limit=20
    ) -> NotePage:
        rows = [n for n in self.notes.values() if n.user_id == user_id]
        return NotePage(items=rows[:limit], next_cursor=None)


def test_create_then_get_is_user_scoped() -> None:
    repo = _FakeRepo()
    me, other = uuid.uuid4(), uuid.uuid4()
    note = asyncio.run(CreateNote(repo=repo).execute(user_id=me, fields=_fields()))
    # Another user cannot read it.
    with pytest.raises(NoteNotFoundError):
        asyncio.run(GetNote(repo=repo).execute(user_id=other, note_id=note.id))


def test_update_preserves_id_and_created_at() -> None:
    repo = _FakeRepo()
    me = uuid.uuid4()
    note = asyncio.run(CreateNote(repo=repo).execute(user_id=me, fields=_fields()))
    updated = asyncio.run(
        UpdateNote(repo=repo).execute(user_id=me, note_id=note.id, fields=_fields(title="Renamed"))
    )
    assert updated.id == note.id
    assert updated.created_at == note.created_at
    assert updated.title == "Renamed"


def test_delete_missing_raises() -> None:
    repo = _FakeRepo()
    with pytest.raises(NoteNotFoundError):
        asyncio.run(DeleteNote(repo=repo).execute(user_id=uuid.uuid4(), note_id=uuid.uuid4()))


def test_list_clamps_limit() -> None:
    repo = _FakeRepo()
    me = uuid.uuid4()
    for _ in range(3):
        asyncio.run(CreateNote(repo=repo).execute(user_id=me, fields=_fields()))
    page = asyncio.run(ListNotes(repo=repo).execute(user_id=me, limit=9999))
    assert len(page.items) == 3
