"""SQLAlchemy adapter for ``NotebookRepository``."""

from __future__ import annotations

import base64
import binascii
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.notebook.models import NoteRow
from cyberdyne_backend.domain.notebook import (
    Note,
    NoteNotFoundError,
    NotePage,
    NoteType,
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


def _row_to_note(row: NoteRow) -> Note:
    return Note(
        id=row.id,
        user_id=row.user_id,
        title=row.title,
        type=NoteType(row.type),
        body=row.body,
        course_slug=row.course_slug,
        lesson_id=row.lesson_id,
        code=row.code,
        language=row.language,
        run_result=row.run_result,
        plot_refs=tuple(row.plot_refs),
        tags=tuple(row.tags),
        created_at=_as_utc(row.created_at) or row.created_at,
        updated_at=_as_utc(row.updated_at),
    )


def _note_to_row(note: Note) -> NoteRow:
    return NoteRow(
        id=note.id,
        user_id=note.user_id,
        title=note.title,
        type=note.type.value,
        body=note.body,
        course_slug=note.course_slug,
        lesson_id=note.lesson_id,
        code=note.code,
        language=note.language,
        run_result=note.run_result,
        plot_refs=list(note.plot_refs),
        tags=list(note.tags),
        created_at=note.created_at,
        updated_at=note.updated_at,
    )


class SqlAlchemyNotebookRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _row(self, *, user_id: UUID, note_id: UUID) -> NoteRow | None:
        return (
            await self._session.execute(
                select(NoteRow).where(NoteRow.id == note_id, NoteRow.user_id == user_id)
            )
        ).scalar_one_or_none()

    async def add(self, note: Note) -> Note:
        self._session.add(_note_to_row(note))
        await self._session.flush()
        return note

    async def get(self, *, user_id: UUID, note_id: UUID) -> Note:
        row = await self._row(user_id=user_id, note_id=note_id)
        if row is None:
            raise NoteNotFoundError(f"note {note_id} not found")
        return _row_to_note(row)

    async def list_for_user(
        self,
        *,
        user_id: UUID,
        type: NoteType | None = None,
        query: str | None = None,
        cursor: str | None = None,
        limit: int = 20,
    ) -> NotePage:
        # Newest first; (created_at, id) descending gives a stable total order.
        stmt = (
            select(NoteRow)
            .where(NoteRow.user_id == user_id)
            .order_by(NoteRow.created_at.desc(), NoteRow.id.desc())
            .limit(limit + 1)
        )
        if type is not None:
            stmt = stmt.where(NoteRow.type == type.value)
        if query:
            needle = f"%{query.lower()}%"
            stmt = stmt.where(
                func.lower(NoteRow.title).like(needle) | func.lower(NoteRow.body).like(needle)
            )
        if cursor is not None:
            decoded = _decode_cursor(cursor)
            if decoded is not None:
                c_ts, c_id = decoded
                stmt = stmt.where(
                    or_(
                        NoteRow.created_at < c_ts,
                        and_(NoteRow.created_at == c_ts, NoteRow.id < c_id),
                    )
                )

        rows = (await self._session.execute(stmt)).scalars().all()
        has_more = len(rows) > limit
        page = rows[:limit]
        items = [_row_to_note(r) for r in page]
        next_cursor = (
            _encode_cursor(items[-1].created_at, items[-1].id) if has_more and items else None
        )
        return NotePage(items=items, next_cursor=next_cursor)

    async def update(self, note: Note) -> Note:
        row = await self._row(user_id=note.user_id, note_id=note.id)
        if row is None:
            raise NoteNotFoundError(f"note {note.id} not found")
        row.title = note.title
        row.type = note.type.value
        row.body = note.body
        row.course_slug = note.course_slug
        row.lesson_id = note.lesson_id
        row.code = note.code
        row.language = note.language
        row.run_result = note.run_result
        row.plot_refs = list(note.plot_refs)
        row.tags = list(note.tags)
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
