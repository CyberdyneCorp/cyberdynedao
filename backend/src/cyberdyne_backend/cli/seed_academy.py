"""Provision the built-in Academy courses (MATLAB & Python) with their
curated lesson content.

Idempotent and non-destructive — see ``application.courses.seed``. Run against
whichever database ``DATABASE_URL`` points at:

    python -m cyberdyne_backend.cli.seed_academy

After the English seed, it translates course/lesson/quiz content into the
supported languages (pt-BR/es/fr) when an OpenAI key is configured — content
whose English source is unchanged is skipped (``source_hash``). Without a key
the translation phase is skipped so local/CI seeds stay fast and free. Prints
a per-course summary and exits non-zero on failure.
"""

from __future__ import annotations

import asyncio
import logging

from cyberdyne_backend.adapters.outbound.persistence.academy.translation_repository import (
    SqlAlchemyTranslationRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.courses.repository import (
    SqlAlchemyCourseRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.quizzes.repository import (
    SqlAlchemyQuizRepository,
)
from cyberdyne_backend.application.academy import (
    MarkdownAwareTranslator,
    TranslateAcademy,
    TranslationStats,
)
from cyberdyne_backend.application.courses.seed import seed_courses
from cyberdyne_backend.application.quizzes.use_cases import UpsertQuiz
from cyberdyne_backend.domain.quizzes import QuizNotFoundError
from cyberdyne_backend.infrastructure.container import Container
from cyberdyne_backend.infrastructure.database.engine import dispose_engine, session_scope
from cyberdyne_backend.infrastructure.logging import configure_logging
from cyberdyne_backend.infrastructure.settings import get_settings

logger = logging.getLogger("cyberdyne_backend.cli.seed_academy")

# Languages the seed content is translated into (English is the source).
TARGET_LANGUAGES = ["pt-BR", "es", "fr"]


async def _translate_content() -> TranslationStats:
    """Translate every seeded course/lesson/quiz into the target languages.

    Committed per course so a long run leaves partial progress and keeps
    transactions small. The orchestrator skips content whose English source
    hasn't changed since the last run.
    """
    settings = get_settings()
    container = Container(settings)
    translator = MarkdownAwareTranslator(llm=container.chat_llm)
    total = TranslationStats()
    try:
        # Read the freshly-seeded catalogue + its quizzes in one session.
        async with session_scope() as session:
            courses = await SqlAlchemyCourseRepository(session).list_courses(include_drafts=True)
            quiz_repo = SqlAlchemyQuizRepository(session)
            quizzes_by_lesson = {}
            for course in courses:
                for lesson in course.lessons:
                    try:
                        quizzes_by_lesson[lesson.id] = await quiz_repo.get_by_lesson(lesson.id)
                    except QuizNotFoundError:
                        continue
        # Translate + persist one course at a time.
        for course in courses:
            lesson_ids = {le.id for le in course.lessons}
            course_quizzes = [q for lid, q in quizzes_by_lesson.items() if lid in lesson_ids]
            async with session_scope() as session:
                orchestrator = TranslateAcademy(
                    translator=translator,
                    repo=SqlAlchemyTranslationRepository(session),
                )
                stats = await orchestrator.run(
                    courses=[course], quizzes=course_quizzes, languages=TARGET_LANGUAGES
                )
            total.merge(stats)
            logger.info(
                "academy translate — %s: +%d translated, %d skipped, %d failed",
                course.slug,
                stats.translated,
                stats.skipped,
                stats.failed,
            )
    finally:
        await container.aclose()
    return total


async def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)
    try:
        async with session_scope() as session:
            summary = await seed_courses(
                SqlAlchemyCourseRepository(session),
                quiz_author=UpsertQuiz(repo=SqlAlchemyQuizRepository(session)),
            )
        for line in summary:
            logger.info("academy seed — %s", line)
        print("Academy seed applied:")
        for line in summary:
            print(f"  • {line}")

        if settings.openai_api_key is None:
            print("  • translation skipped (no OPENAI_API_KEY configured)")
            logger.info("academy translate — skipped (no OpenAI key)")
        else:
            print(f"  • translating into {', '.join(TARGET_LANGUAGES)} …")
            stats = await _translate_content()
            print(
                f"  • translation done: {stats.translated} translated, "
                f"{stats.skipped} skipped, {stats.failed} failed"
            )
    finally:
        await dispose_engine()


if __name__ == "__main__":
    asyncio.run(main())
