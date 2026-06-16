"""Regression: quiz upsert must insert parents before children.

The quiz tree is quizzes -> quiz_questions -> quiz_options (FK chain), and
the models declare only column-level ForeignKeys (no relationship()), so a
single flush let the unit of work emit quiz_options INSERTs before their
quiz_questions existed. SQLite ignores FKs by default (so the old code
passed in CI), but Postgres rejects it with a ForeignKeyViolation — quiz
authoring 500'd in production.

This test enables SQLite FK enforcement (PRAGMA foreign_keys=ON) so the
ordering bug surfaces here too, then drives the real repository.
"""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator
from datetime import UTC, datetime

import pytest
import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from cyberdyne_backend.adapters.outbound.persistence.content import models as _content  # noqa: F401
from cyberdyne_backend.adapters.outbound.persistence.courses import models as courses_models
from cyberdyne_backend.adapters.outbound.persistence.quizzes import models as _quizzes  # noqa: F401
from cyberdyne_backend.adapters.outbound.persistence.quizzes.models import (
    QuizOptionTranslationRow,
    QuizQuestionTranslationRow,
)
from cyberdyne_backend.adapters.outbound.persistence.quizzes.repository import (
    SqlAlchemyQuizRepository,
)
from cyberdyne_backend.application.quizzes.use_cases import (
    OptionInput,
    QuestionInput,
    UpsertQuiz,
    UpsertQuizCommand,
)
from cyberdyne_backend.infrastructure.database.base import Base

pytestmark = pytest.mark.integration


@pytest_asyncio.fixture
async def fk_session() -> AsyncIterator[AsyncSession]:
    """In-memory SQLite session with foreign-key enforcement turned ON."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    @event.listens_for(engine.sync_engine, "connect")
    def _fk_on(dbapi_conn, _record):
        cur = dbapi_conn.cursor()
        cur.execute("PRAGMA foreign_keys=ON")
        cur.close()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        yield session
    await engine.dispose()


def _cmd() -> UpsertQuizCommand:
    return UpsertQuizCommand(
        passing_score=70,
        questions=[
            QuestionInput(
                prompt="What does the apostrophe do?",
                explanation="Transpose.",
                options=[
                    OptionInput(text="Transposes it", is_correct=True),
                    OptionInput(text="Inverts it", is_correct=False),
                ],
            ),
            QuestionInput(
                prompt="Element-wise multiply?",
                explanation=".*",
                options=[
                    OptionInput(text=".*", is_correct=True),
                    OptionInput(text="*", is_correct=False),
                ],
            ),
        ],
    )


async def _seed_quiz_lesson(session: AsyncSession) -> uuid.UUID:
    course_id = uuid.uuid4()
    lesson_id = uuid.uuid4()
    session.add(
        courses_models.CourseRow(
            id=course_id,
            slug="fk-course",
            title="FK Course",
            description="",
            level="Beginner",
            status="draft",
            mandatory=False,
            sort_order=0,
            created_at=datetime.now(UTC),
        )
    )
    session.add(
        courses_models.LessonRow(
            id=lesson_id,
            course_id=course_id,
            title="Quiz lesson",
            lesson_type="quiz",
            sort_order=0,
            created_at=datetime.now(UTC),
        )
    )
    await session.flush()
    return lesson_id


async def test_upsert_inserts_parents_before_children(fk_session: AsyncSession) -> None:
    lesson_id = await _seed_quiz_lesson(fk_session)
    repo = SqlAlchemyQuizRepository(fk_session)

    # Would raise IntegrityError (options before questions) before the fix.
    await UpsertQuiz(repo=repo).execute(lesson_id, _cmd())

    stored = await repo.get_by_lesson(lesson_id)
    assert stored is not None
    assert len(stored.questions) == 2
    assert [len(q.options) for q in stored.questions] == [2, 2]


async def test_re_upsert_replaces_the_tree(fk_session: AsyncSession) -> None:
    lesson_id = await _seed_quiz_lesson(fk_session)
    repo = SqlAlchemyQuizRepository(fk_session)
    await UpsertQuiz(repo=repo).execute(lesson_id, _cmd())

    # Second upsert shrinks the tree (2 questions -> 1): the overlap is
    # reconciled in place and the surplus question is dropped, no FK errors.
    await UpsertQuiz(repo=repo).execute(
        lesson_id,
        UpsertQuizCommand(
            passing_score=80,
            questions=[
                QuestionInput(
                    prompt="Only one now",
                    explanation="",
                    options=[
                        OptionInput(text="yes", is_correct=True),
                        OptionInput(text="no", is_correct=False),
                    ],
                )
            ],
        ),
    )
    stored = await repo.get_by_lesson(lesson_id)
    assert stored is not None
    assert stored.passing_score == 80
    assert len(stored.questions) == 1


async def test_re_upsert_preserves_quiz_translations(fk_session: AsyncSession) -> None:
    """Regression: re-authoring an unchanged quiz must NOT wipe its
    translations.

    quiz_question_translations / quiz_option_translations CASCADE on the
    question/option ids. The seeder re-authors quizzes on every boot, so a
    delete + re-insert upsert cascade-erased every localized quiz on each
    deploy — quizzes fell back to English. The fix reconciles the tree in
    place (stable ids), so the translation rows below survive the re-upsert.
    """
    lesson_id = await _seed_quiz_lesson(fk_session)
    repo = SqlAlchemyQuizRepository(fk_session)
    await UpsertQuiz(repo=repo).execute(lesson_id, _cmd())

    # Simulate the translate job: attach a pt-BR translation to the first
    # question and its first option.
    stored = await repo.get_by_lesson(lesson_id)
    question = stored.questions[0]
    option = question.options[0]
    fk_session.add(
        QuizQuestionTranslationRow(
            id=uuid.uuid4(),
            question_id=question.id,
            language="pt-BR",
            prompt="O que faz o apóstrofo?",
            explanation="Transpõe.",
            source_hash="hash-q",
        )
    )
    fk_session.add(
        QuizOptionTranslationRow(
            id=uuid.uuid4(),
            option_id=option.id,
            language="pt-BR",
            text="Transpõe a matriz",
            source_hash="hash-o",
        )
    )
    await fk_session.flush()

    # Re-author the identical quiz, as seed_academy does on every boot.
    await UpsertQuiz(repo=repo).execute(lesson_id, _cmd())

    # The translation must still resolve through the localized read path.
    localized = await repo.get_by_lesson(lesson_id, locale="pt-BR")
    assert localized.questions[0].prompt == "O que faz o apóstrofo?"
    assert localized.questions[0].explanation == "Transpõe."
    assert localized.questions[0].options[0].text == "Transpõe a matriz"
