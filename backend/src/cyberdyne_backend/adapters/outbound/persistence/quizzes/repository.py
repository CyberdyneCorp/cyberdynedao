"""SQLAlchemy adapter for ``QuizRepository``."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.quizzes.models import (
    QuizAttemptRow,
    QuizOptionRow,
    QuizOptionTranslationRow,
    QuizQuestionRow,
    QuizQuestionTranslationRow,
    QuizRow,
)
from cyberdyne_backend.domain.quizzes import (
    Question,
    QuestionOption,
    Quiz,
    QuizAttempt,
    QuizNotFoundError,
)


class SqlAlchemyQuizRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_lesson(self, lesson_id: UUID, *, locale: str = "en") -> Quiz:
        row = (
            await self._session.execute(select(QuizRow).where(QuizRow.lesson_id == lesson_id))
        ).scalar_one_or_none()
        if row is None:
            raise QuizNotFoundError(str(lesson_id))
        question_rows = (
            (
                await self._session.execute(
                    select(QuizQuestionRow)
                    .where(QuizQuestionRow.quiz_id == row.id)
                    .order_by(QuizQuestionRow.sort_order)
                )
            )
            .scalars()
            .all()
        )
        options_by_question = await self._options_for([q.id for q in question_rows])
        # Per-field English fallback overlay for a non-English locale.
        localize = locale not in ("", "en")
        q_tr = (
            await self._question_translations([q.id for q in question_rows], locale)
            if localize
            else {}
        )
        all_option_ids = [o.id for opts in options_by_question.values() for o in opts]
        o_tr = await self._option_translations(all_option_ids, locale) if localize else {}
        questions = [
            Question(
                id=q.id,
                prompt=(q_tr[q.id].prompt if q.id in q_tr and q_tr[q.id].prompt else q.prompt),
                explanation=(
                    q_tr[q.id].explanation
                    if q.id in q_tr and q_tr[q.id].explanation
                    else q.explanation
                ),
                sort_order=q.sort_order,
                options=[
                    QuestionOption(
                        id=o.id,
                        text=(o_tr[o.id].text if o.id in o_tr and o_tr[o.id].text else o.text),
                        is_correct=o.is_correct,
                        sort_order=o.sort_order,
                    )
                    for o in sorted(options_by_question.get(q.id, []), key=lambda x: x.sort_order)
                ],
            )
            for q in question_rows
        ]
        return Quiz(
            id=row.id,
            lesson_id=row.lesson_id,
            passing_score=row.passing_score,
            questions=questions,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    async def upsert(self, quiz: Quiz) -> None:
        existing = (
            await self._session.execute(select(QuizRow).where(QuizRow.lesson_id == quiz.lesson_id))
        ).scalar_one_or_none()
        if existing is not None:
            # Clear out the old question/option tree before re-inserting.
            await self._delete_questions(existing.id)
            existing.passing_score = quiz.passing_score
            existing.updated_at = quiz.updated_at
            quiz_id = existing.id
        else:
            self._session.add(
                QuizRow(
                    id=quiz.id,
                    lesson_id=quiz.lesson_id,
                    passing_score=quiz.passing_score,
                    created_at=quiz.created_at,
                    updated_at=quiz.updated_at,
                )
            )
            quiz_id = quiz.id
        # Flush each level before inserting the next: the rows form a
        # quizzes → quiz_questions → quiz_options FK chain, and the models
        # declare only column-level ForeignKeys (no relationship()), so the
        # unit of work doesn't know to order the INSERTs. A single flush
        # lets options be written before their question exists, which a
        # real FK-enforcing DB (Postgres) rejects (SQLite silently allows
        # it). Flushing per level guarantees parents land first.
        await self._session.flush()
        for question in quiz.questions:
            self._session.add(
                QuizQuestionRow(
                    id=question.id,
                    quiz_id=quiz_id,
                    prompt=question.prompt,
                    explanation=question.explanation,
                    sort_order=question.sort_order,
                )
            )
        await self._session.flush()
        for question in quiz.questions:
            for option in question.options:
                self._session.add(
                    QuizOptionRow(
                        id=option.id,
                        question_id=question.id,
                        text=option.text,
                        is_correct=option.is_correct,
                        sort_order=option.sort_order,
                    )
                )
        await self._session.flush()

    async def delete_by_lesson(self, lesson_id: UUID) -> None:
        row = (
            await self._session.execute(select(QuizRow).where(QuizRow.lesson_id == lesson_id))
        ).scalar_one_or_none()
        if row is None:
            return
        await self._delete_questions(row.id)
        await self._session.execute(delete(QuizAttemptRow).where(QuizAttemptRow.quiz_id == row.id))
        await self._session.execute(delete(QuizRow).where(QuizRow.id == row.id))
        await self._session.flush()

    async def add_attempt(self, attempt: QuizAttempt) -> QuizAttempt:
        self._session.add(
            QuizAttemptRow(
                id=attempt.id,
                user_id=attempt.user_id,
                quiz_id=attempt.quiz_id,
                lesson_id=attempt.lesson_id,
                score=attempt.score,
                passed=attempt.passed,
                attempt_number=attempt.attempt_number,
                answers=attempt.answers,
                submitted_at=attempt.submitted_at,
            )
        )
        await self._session.flush()
        return attempt

    async def list_attempts(self, *, user_id: UUID, quiz_id: UUID) -> list[QuizAttempt]:
        rows = (
            (
                await self._session.execute(
                    select(QuizAttemptRow)
                    .where(
                        QuizAttemptRow.user_id == user_id,
                        QuizAttemptRow.quiz_id == quiz_id,
                    )
                    .order_by(QuizAttemptRow.attempt_number)
                )
            )
            .scalars()
            .all()
        )
        return [_row_to_attempt(r) for r in rows]

    async def count_attempts(self, *, user_id: UUID, quiz_id: UUID) -> int:
        total = (
            await self._session.execute(
                select(func.count(QuizAttemptRow.id)).where(
                    QuizAttemptRow.user_id == user_id,
                    QuizAttemptRow.quiz_id == quiz_id,
                )
            )
        ).scalar_one()
        return int(total)

    async def _options_for(self, question_ids: list[UUID]) -> dict[UUID, list[QuizOptionRow]]:
        if not question_ids:
            return {}
        rows = (
            (
                await self._session.execute(
                    select(QuizOptionRow).where(QuizOptionRow.question_id.in_(question_ids))
                )
            )
            .scalars()
            .all()
        )
        out: dict[UUID, list[QuizOptionRow]] = {}
        for row in rows:
            out.setdefault(row.question_id, []).append(row)
        return out

    async def _question_translations(
        self, question_ids: list[UUID], locale: str
    ) -> dict[UUID, QuizQuestionTranslationRow]:
        if not question_ids:
            return {}
        rows = (
            (
                await self._session.execute(
                    select(QuizQuestionTranslationRow).where(
                        QuizQuestionTranslationRow.question_id.in_(question_ids),
                        QuizQuestionTranslationRow.language == locale,
                    )
                )
            )
            .scalars()
            .all()
        )
        return {row.question_id: row for row in rows}

    async def _option_translations(
        self, option_ids: list[UUID], locale: str
    ) -> dict[UUID, QuizOptionTranslationRow]:
        if not option_ids:
            return {}
        rows = (
            (
                await self._session.execute(
                    select(QuizOptionTranslationRow).where(
                        QuizOptionTranslationRow.option_id.in_(option_ids),
                        QuizOptionTranslationRow.language == locale,
                    )
                )
            )
            .scalars()
            .all()
        )
        return {row.option_id: row for row in rows}

    async def _delete_questions(self, quiz_id: UUID) -> None:
        question_ids = (
            (
                await self._session.execute(
                    select(QuizQuestionRow.id).where(QuizQuestionRow.quiz_id == quiz_id)
                )
            )
            .scalars()
            .all()
        )
        if question_ids:
            await self._session.execute(
                delete(QuizOptionRow).where(QuizOptionRow.question_id.in_(question_ids))
            )
        await self._session.execute(
            delete(QuizQuestionRow).where(QuizQuestionRow.quiz_id == quiz_id)
        )


def _row_to_attempt(row: QuizAttemptRow) -> QuizAttempt:
    return QuizAttempt(
        id=row.id,
        user_id=row.user_id,
        quiz_id=row.quiz_id,
        lesson_id=row.lesson_id,
        score=row.score,
        passed=row.passed,
        attempt_number=row.attempt_number,
        answers=dict(row.answers),
        submitted_at=row.submitted_at,
    )
