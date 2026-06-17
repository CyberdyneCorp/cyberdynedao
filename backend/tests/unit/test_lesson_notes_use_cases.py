"""Unit tests for lesson-notes use cases (issue #188)."""

from __future__ import annotations

import asyncio
import uuid

import pytest

from cyberdyne_backend.application.lesson_notes import (
    DeleteLessonNote,
    SyncLessonNote,
    UpdateLessonNote,
)
from cyberdyne_backend.domain.lesson_notes import (
    InvalidLessonNoteError,
    LessonNote,
    LessonNoteNotFoundError,
    LessonNotePage,
    new_lesson_note,
)


def test_new_lesson_note_validates_body() -> None:
    with pytest.raises(InvalidLessonNoteError):
        new_lesson_note(user_id=uuid.uuid4(), course_slug="c", lesson_id="l1", body="   ")


def test_new_lesson_note_uses_client_id_when_given() -> None:
    cid = uuid.uuid4()
    n = new_lesson_note(
        user_id=uuid.uuid4(), course_slug="c", lesson_id="l1", body="b", note_id=cid
    )
    assert n.id == cid


class _FakeRepo:
    def __init__(self) -> None:
        self.notes: dict[uuid.UUID, LessonNote] = {}

    async def upsert(self, note: LessonNote) -> bool:
        created = note.id not in self.notes
        self.notes[note.id] = note
        return created

    async def get(self, *, user_id, note_id) -> LessonNote:
        n = self.notes.get(note_id)
        if n is None or n.user_id != user_id:
            raise LessonNoteNotFoundError(str(note_id))
        return n

    async def update(self, note: LessonNote) -> LessonNote:
        self.notes[note.id] = note
        return note

    async def delete(self, *, user_id, note_id) -> bool:
        n = self.notes.get(note_id)
        if n is None or n.user_id != user_id:
            return False
        del self.notes[note_id]
        return True

    async def list_for_lesson(self, *, user_id, lesson_id):
        return [n for n in self.notes.values() if n.user_id == user_id and n.lesson_id == lesson_id]

    async def list_for_user(self, *, user_id, course_slug=None, cursor=None, limit=50):
        rows = [n for n in self.notes.values() if n.user_id == user_id]
        return LessonNotePage(items=rows[:limit], next_cursor=None)


def test_sync_is_idempotent_on_client_id() -> None:
    repo = _FakeRepo()
    uc = SyncLessonNote(repo=repo)
    user, cid = uuid.uuid4(), uuid.uuid4()

    first = asyncio.run(
        uc.execute(user_id=user, lesson_id="l1", course_slug="c", body="v1", note_id=cid)
    )
    assert first.created is True

    # Re-sync the same client id → updates in place, no duplicate.
    second = asyncio.run(
        uc.execute(user_id=user, lesson_id="l1", course_slug="c", body="v2", note_id=cid)
    )
    assert second.created is False
    assert second.note.id == cid
    assert len(repo.notes) == 1
    assert repo.notes[cid].body == "v2"


def test_update_clears_quote_only_when_set() -> None:
    repo = _FakeRepo()
    user = uuid.uuid4()
    note = new_lesson_note(user_id=user, course_slug="c", lesson_id="l1", body="b", quote="hi")
    asyncio.run(repo.upsert(note))

    # quote_set=False leaves the existing quote untouched.
    out = asyncio.run(
        UpdateLessonNote(repo=repo).execute(
            user_id=user, note_id=note.id, body="b2", quote=None, quote_set=False
        )
    )
    assert out.quote == "hi"
    assert out.body == "b2"

    # quote_set=True with None clears it.
    out2 = asyncio.run(
        UpdateLessonNote(repo=repo).execute(
            user_id=user, note_id=note.id, quote=None, quote_set=True
        )
    )
    assert out2.quote is None


def test_update_missing_note_raises() -> None:
    repo = _FakeRepo()
    with pytest.raises(LessonNoteNotFoundError):
        asyncio.run(
            UpdateLessonNote(repo=repo).execute(
                user_id=uuid.uuid4(), note_id=uuid.uuid4(), body="x"
            )
        )


def test_delete_missing_note_raises() -> None:
    repo = _FakeRepo()
    with pytest.raises(LessonNoteNotFoundError):
        asyncio.run(DeleteLessonNote(repo=repo).execute(user_id=uuid.uuid4(), note_id=uuid.uuid4()))
