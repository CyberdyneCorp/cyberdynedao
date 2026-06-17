"""SQLAlchemy adapter for ``QuizCatalogReader`` (issue #169).

Read-only browse view that joins quizzes to their lesson + course (+
category) so the Quizzes nav can list assessments outside a single
lesson. Cross-context table access is intentional and read-only, like
the analytics reporting adapter — this view owns no tables and never
writes. Only quizzes belonging to *published* courses are returned.

Paging is keyset (cursor) on ``(course_slug, quiz_id)`` — a stable,
total order that works identically on SQLite (tests) and Postgres.
"""

from __future__ import annotations

import base64
import binascii
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.courses.models import (
    CategoryRow,
    CourseRow,
    LessonRow,
)
from cyberdyne_backend.adapters.outbound.persistence.quizzes.models import (
    QuizAttemptRow,
    QuizQuestionRow,
    QuizRow,
)
from cyberdyne_backend.domain.quizzes import (
    LastAttempt,
    QuizCatalogPage,
    QuizSummary,
)

# Cursor payload separator — a NUL byte never appears in a slug or UUID.
_CURSOR_SEP = "\x00"

# Mirrors the courses public-read filter (CourseStatus.PUBLISHED). Kept
# as a literal so the quizzes adapter doesn't import the courses domain.
_PUBLISHED_STATUS = "published"


def _encode_cursor(course_slug: str, quiz_id: UUID) -> str:
    raw = f"{course_slug}{_CURSOR_SEP}{quiz_id}".encode()
    return base64.urlsafe_b64encode(raw).decode("ascii")


def _decode_cursor(cursor: str) -> tuple[str, UUID] | None:
    """Decode a cursor into ``(course_slug, quiz_id)``. Returns ``None``
    for a malformed token so the caller can treat it as 'from the start'
    rather than 500."""
    try:
        raw = base64.urlsafe_b64decode(cursor.encode("ascii")).decode()
        course_slug, _, quiz_raw = raw.partition(_CURSOR_SEP)
        return course_slug, UUID(quiz_raw)
    except (ValueError, binascii.Error, UnicodeDecodeError):
        return None


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value


class SqlAlchemyQuizCatalogReader:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_quizzes(
        self,
        *,
        user_id: UUID,
        course_slug: str | None = None,
        category_slug: str | None = None,
        cursor: str | None = None,
        limit: int = 20,
    ) -> QuizCatalogPage:
        question_count = (
            select(func.count(QuizQuestionRow.id))
            .where(QuizQuestionRow.quiz_id == QuizRow.id)
            .scalar_subquery()
        )

        stmt = (
            select(
                QuizRow.id,
                QuizRow.lesson_id,
                QuizRow.passing_score,
                LessonRow.title,
                CourseRow.slug,
                CourseRow.title,
                CategoryRow.slug,
                question_count,
            )
            .join(LessonRow, LessonRow.id == QuizRow.lesson_id)
            .join(CourseRow, CourseRow.id == LessonRow.course_id)
            .join(CategoryRow, CategoryRow.id == CourseRow.category_id, isouter=True)
            # Learner-facing browse: only published courses are discoverable.
            .where(CourseRow.status == _PUBLISHED_STATUS)
            .order_by(CourseRow.slug, QuizRow.id)
            .limit(limit + 1)  # +1 row probes whether another page exists.
        )

        if course_slug is not None:
            stmt = stmt.where(CourseRow.slug == course_slug)
        if category_slug is not None:
            stmt = stmt.where(CategoryRow.slug == category_slug)
        if cursor is not None:
            decoded = _decode_cursor(cursor)
            if decoded is not None:
                last_slug, last_id = decoded
                stmt = stmt.where(
                    or_(
                        CourseRow.slug > last_slug,
                        and_(CourseRow.slug == last_slug, QuizRow.id > last_id),
                    )
                )

        rows = (await self._session.execute(stmt)).all()

        has_more = len(rows) > limit
        page_rows = rows[:limit]

        last_attempts = await self._last_attempts_for(
            user_id=user_id, quiz_ids=[r[0] for r in page_rows]
        )

        items = [
            QuizSummary(
                quiz_id=r[0],
                lesson_id=r[1],
                passing_score=r[2],
                lesson_title=r[3],
                course_slug=r[4],
                course_title=r[5],
                category_slug=r[6],
                question_count=r[7] or 0,
                last_attempt=last_attempts.get(r[0]),
            )
            for r in page_rows
        ]

        next_cursor = (
            _encode_cursor(items[-1].course_slug, items[-1].quiz_id)
            if has_more and items
            else None
        )
        return QuizCatalogPage(items=items, next_cursor=next_cursor)

    async def _last_attempts_for(
        self, *, user_id: UUID, quiz_ids: list[UUID]
    ) -> dict[UUID, LastAttempt]:
        """Most-recent attempt per quiz for the learner, keyed by quiz id."""
        if not quiz_ids:
            return {}
        rows = (
            (
                await self._session.execute(
                    select(QuizAttemptRow)
                    .where(
                        QuizAttemptRow.user_id == user_id,
                        QuizAttemptRow.quiz_id.in_(quiz_ids),
                    )
                    .order_by(QuizAttemptRow.attempt_number)
                )
            )
            .scalars()
            .all()
        )
        # Ascending attempt_number means the last row wins per quiz.
        latest: dict[UUID, LastAttempt] = {}
        for row in rows:
            latest[row.quiz_id] = LastAttempt(
                score=row.score,
                passed=row.passed,
                attempt_number=row.attempt_number,
                submitted_at=_as_utc(row.submitted_at),
            )
        return latest
