"""SQLAlchemy adapter for :class:`TranslationRepository`.

Writes the four ``*_translations`` tables (course/lesson/quiz-question/
quiz-option) and reports current per-language source hashes so the
translation orchestrator can skip unchanged content.
"""

from __future__ import annotations

import uuid
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.courses.models import (
    CourseTranslationRow,
    LessonRow,
    LessonTranslationRow,
)
from cyberdyne_backend.adapters.outbound.persistence.quizzes.models import (
    QuizOptionTranslationRow,
    QuizQuestionTranslationRow,
)


class SqlAlchemyTranslationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def course_languages(self, course_id: UUID) -> list[str]:
        rows = (
            (
                await self._session.execute(
                    select(CourseTranslationRow.language)
                    .where(CourseTranslationRow.course_id == course_id)
                    .distinct()
                )
            )
            .scalars()
            .all()
        )
        return list(rows)

    async def translated_lesson_counts(self, course_id: UUID) -> dict[str, int]:
        rows = (
            await self._session.execute(
                select(
                    LessonTranslationRow.language,
                    func.count(LessonTranslationRow.id),
                )
                .join(LessonRow, LessonRow.id == LessonTranslationRow.lesson_id)
                .where(LessonRow.course_id == course_id)
                .group_by(LessonTranslationRow.language)
            )
        ).all()
        return {language: count for language, count in rows}

    # ── hashes (skip-unchanged lookups) ──────────────────────────────

    async def course_hashes(self, language: str) -> dict[UUID, str]:
        rows = (
            await self._session.execute(
                select(CourseTranslationRow.course_id, CourseTranslationRow.source_hash).where(
                    CourseTranslationRow.language == language
                )
            )
        ).all()
        return {cid: h for cid, h in rows}

    async def lesson_hashes(self, language: str) -> dict[UUID, str]:
        rows = (
            await self._session.execute(
                select(LessonTranslationRow.lesson_id, LessonTranslationRow.source_hash).where(
                    LessonTranslationRow.language == language
                )
            )
        ).all()
        return {lid: h for lid, h in rows}

    async def question_hashes(self, language: str) -> dict[UUID, str]:
        rows = (
            await self._session.execute(
                select(
                    QuizQuestionTranslationRow.question_id,
                    QuizQuestionTranslationRow.source_hash,
                ).where(QuizQuestionTranslationRow.language == language)
            )
        ).all()
        return {qid: h for qid, h in rows}

    async def option_hashes(self, language: str) -> dict[UUID, str]:
        rows = (
            await self._session.execute(
                select(
                    QuizOptionTranslationRow.option_id,
                    QuizOptionTranslationRow.source_hash,
                ).where(QuizOptionTranslationRow.language == language)
            )
        ).all()
        return {oid: h for oid, h in rows}

    # ── upserts ───────────────────────────────────────────────────────

    async def upsert_course_translation(
        self, *, course_id: UUID, language: str, title: str, description: str, source_hash: str
    ) -> None:
        existing = (
            await self._session.execute(
                select(CourseTranslationRow).where(
                    CourseTranslationRow.course_id == course_id,
                    CourseTranslationRow.language == language,
                )
            )
        ).scalar_one_or_none()
        if existing is None:
            self._session.add(
                CourseTranslationRow(
                    id=uuid.uuid4(),
                    course_id=course_id,
                    language=language,
                    title=title,
                    description=description,
                    source_hash=source_hash,
                )
            )
        else:
            existing.title = title
            existing.description = description
            existing.source_hash = source_hash
        await self._session.flush()

    async def upsert_lesson_translation(
        self,
        *,
        lesson_id: UUID,
        language: str,
        title: str,
        text_body: str | None,
        source_hash: str,
    ) -> None:
        existing = (
            await self._session.execute(
                select(LessonTranslationRow).where(
                    LessonTranslationRow.lesson_id == lesson_id,
                    LessonTranslationRow.language == language,
                )
            )
        ).scalar_one_or_none()
        if existing is None:
            self._session.add(
                LessonTranslationRow(
                    id=uuid.uuid4(),
                    lesson_id=lesson_id,
                    language=language,
                    title=title,
                    text_body=text_body,
                    source_hash=source_hash,
                )
            )
        else:
            existing.title = title
            existing.text_body = text_body
            existing.source_hash = source_hash
        await self._session.flush()

    async def upsert_question_translation(
        self,
        *,
        question_id: UUID,
        language: str,
        prompt: str,
        explanation: str,
        source_hash: str,
    ) -> None:
        existing = (
            await self._session.execute(
                select(QuizQuestionTranslationRow).where(
                    QuizQuestionTranslationRow.question_id == question_id,
                    QuizQuestionTranslationRow.language == language,
                )
            )
        ).scalar_one_or_none()
        if existing is None:
            self._session.add(
                QuizQuestionTranslationRow(
                    id=uuid.uuid4(),
                    question_id=question_id,
                    language=language,
                    prompt=prompt,
                    explanation=explanation,
                    source_hash=source_hash,
                )
            )
        else:
            existing.prompt = prompt
            existing.explanation = explanation
            existing.source_hash = source_hash
        await self._session.flush()

    async def upsert_option_translation(
        self, *, option_id: UUID, language: str, text: str, source_hash: str
    ) -> None:
        existing = (
            await self._session.execute(
                select(QuizOptionTranslationRow).where(
                    QuizOptionTranslationRow.option_id == option_id,
                    QuizOptionTranslationRow.language == language,
                )
            )
        ).scalar_one_or_none()
        if existing is None:
            self._session.add(
                QuizOptionTranslationRow(
                    id=uuid.uuid4(),
                    option_id=option_id,
                    language=language,
                    text=text,
                    source_hash=source_hash,
                )
            )
        else:
            existing.text = text
            existing.source_hash = source_hash
        await self._session.flush()
