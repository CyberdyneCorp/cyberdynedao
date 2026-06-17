"""SQLAlchemy adapter for ``LessonNoteRepository``."""

from __future__ import annotations

import base64
import binascii
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.lesson_notes.models import (
    LessonNoteRow,
)
from cyberdyne_backend.domain.lesson_notes import (
    LessonNote,
    LessonNoteNotFoundError,
    LessonNotePage,
)

_CURSOR_SEP = "\x00"


def _as_utc(value: datetime | None) -> datetime | None:
    if value is not None and value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value


def _encode_cursor(created_at: datetime, note_id: UUID) -> str:
    raw = f"{created_at.isoformat()}{_CURSOR_SEP}{note_id}"
    return base64.urlsafe_b64encode(raw.encode()).decode("ascii")


def _decode_cursor(cursor: str) -> tuple[datetime, UUID] | None:
    try:
        raw = base64.urlsafe_b64decode(cursor.encode("ascii")).decode()
        ts_raw, _, id_raw = raw.partition(_CURSOR_SEP)
        return datetime.fromisoformat(ts_raw), UUID(id_raw)
    except (ValueError, binascii.Error, UnicodeDecodeError):
        return None


def _row_to_note(row: LessonNoteRow) -> LessonNote:
    return LessonNote(
        id=row.id,
        user_id=row.user_id,
        course_slug=row.course_slug,
        lesson_id=row.lesson_id,
        body=row.body,
        quote=row.quote,
        created_at=_as_utc(row.created_at) or row.created_at,
        updated_at=_as_utc(row.updated_at),
    )


class SqlAlchemyLessonNoteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _row(self, *, user_id: UUID, note_id: UUID) -> LessonNoteRow | None:
        return (
            await self._session.execute(
                select(LessonNoteRow).where(
                    LessonNoteRow.id == note_id, LessonNoteRow.user_id == user_id
                )
            )
        ).scalar_one_or_none()

    async def upsert(self, note: LessonNote) -> bool:
        existing = await self._row(user_id=note.user_id, note_id=note.id)
        if existing is not None:
            existing.course_slug = note.course_slug
            existing.lesson_id = note.lesson_id
            existing.quote = note.quote
            existing.body = note.body
            existing.updated_at = note.updated_at
            await self._session.flush()
            return False
        self._session.add(
            LessonNoteRow(
                id=note.id,
                user_id=note.user_id,
                course_slug=note.course_slug,
                lesson_id=note.lesson_id,
                quote=note.quote,
                body=note.body,
                created_at=note.created_at,
                updated_at=note.updated_at,
            )
        )
        await self._session.flush()
        return True

    async def get(self, *, user_id: UUID, note_id: UUID) -> LessonNote:
        row = await self._row(user_id=user_id, note_id=note_id)
        if row is None:
            raise LessonNoteNotFoundError(f"note {note_id} not found")
        return _row_to_note(row)

    async def list_for_lesson(self, *, user_id: UUID, lesson_id: str) -> list[LessonNote]:
        rows = (
            (
                await self._session.execute(
                    select(LessonNoteRow)
                    .where(
                        LessonNoteRow.user_id == user_id,
                        LessonNoteRow.lesson_id == lesson_id,
                    )
                    .order_by(LessonNoteRow.created_at.desc(), LessonNoteRow.id.desc())
                )
            )
            .scalars()
            .all()
        )
        return [_row_to_note(r) for r in rows]

    async def list_for_user(
        self,
        *,
        user_id: UUID,
        course_slug: str | None = None,
        cursor: str | None = None,
        limit: int = 50,
    ) -> LessonNotePage:
        stmt = (
            select(LessonNoteRow)
            .where(LessonNoteRow.user_id == user_id)
            .order_by(LessonNoteRow.created_at.desc(), LessonNoteRow.id.desc())
            .limit(limit + 1)
        )
        if course_slug is not None:
            stmt = stmt.where(LessonNoteRow.course_slug == course_slug)
        if cursor is not None:
            decoded = _decode_cursor(cursor)
            if decoded is not None:
                c_ts, c_id = decoded
                stmt = stmt.where(
                    or_(
                        LessonNoteRow.created_at < c_ts,
                        and_(LessonNoteRow.created_at == c_ts, LessonNoteRow.id < c_id),
                    )
                )
        rows = (await self._session.execute(stmt)).scalars().all()
        has_more = len(rows) > limit
        page = rows[:limit]
        items = [_row_to_note(r) for r in page]
        next_cursor = (
            _encode_cursor(items[-1].created_at, items[-1].id) if has_more and items else None
        )
        return LessonNotePage(items=items, next_cursor=next_cursor)

    async def update(self, note: LessonNote) -> LessonNote:
        row = await self._row(user_id=note.user_id, note_id=note.id)
        if row is None:
            raise LessonNoteNotFoundError(f"note {note.id} not found")
        row.course_slug = note.course_slug
        row.lesson_id = note.lesson_id
        row.quote = note.quote
        row.body = note.body
        row.updated_at = note.updated_at
        await self._session.flush()
        return note

    async def delete(self, *, user_id: UUID, note_id: UUID) -> bool:
        row = await self._row(user_id=user_id, note_id=note_id)
        if row is None:
            return False
        await self._session.delete(row)
        await self._session.flush()
        return True
