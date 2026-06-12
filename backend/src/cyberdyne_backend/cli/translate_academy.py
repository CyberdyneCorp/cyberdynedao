"""Translate the seeded Academy content into the supported languages.

A standalone, on-demand job — deliberately NOT part of the boot-time
``seed_academy`` (which must stay fast so the container starts promptly).
Translating the whole catalogue is thousands of LLM calls and can run for
a long time, so it's run explicitly:

    python -m cyberdyne_backend.cli.translate_academy            # whole catalogue
    python -m cyberdyne_backend.cli.translate_academy --slug matlab-basics  # one course
    python -m cyberdyne_backend.cli.translate_academy --limit 1            # first course only

``--slug`` / ``--limit`` exist to smoke-test cost + quality on a small slice
before committing to the full run. Requires ``OPENAI_API_KEY`` (otherwise
there's nothing to translate with — it prints a notice and exits).
Incremental: content whose English source is unchanged since the last run is
skipped (``source_hash``), so the job is safely resumable — re-run if it's
interrupted.
"""

from __future__ import annotations

import argparse
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
from cyberdyne_backend.domain.courses import Course
from cyberdyne_backend.domain.quizzes import QuizNotFoundError
from cyberdyne_backend.infrastructure.container import Container
from cyberdyne_backend.infrastructure.database.engine import dispose_engine, session_scope
from cyberdyne_backend.infrastructure.logging import configure_logging
from cyberdyne_backend.infrastructure.settings import get_settings

logger = logging.getLogger("cyberdyne_backend.cli.translate_academy")

# Languages the seed content is translated into (English is the source).
TARGET_LANGUAGES = ["pt-BR", "es", "fr"]


def select_courses(
    courses: list[Course], *, slug: str | None = None, limit: int | None = None
) -> list[Course]:
    """Apply the ``--slug`` / ``--limit`` scope to the loaded catalogue.

    ``slug`` wins over ``limit``; with neither, the whole catalogue is
    returned. Ordering is preserved so ``--limit`` is deterministic.
    """
    if slug is not None:
        return [c for c in courses if c.slug == slug]
    if limit is not None:
        return courses[: max(0, limit)]
    return courses


async def translate_content(
    *, slug: str | None = None, limit: int | None = None
) -> TranslationStats:
    """Translate seeded course/lesson/quiz content into the target languages.

    Committed per course so a long run leaves partial progress and keeps
    transactions small. Skips content whose English source is unchanged.
    """
    settings = get_settings()
    container = Container(settings)
    translator = MarkdownAwareTranslator(llm=container.chat_llm)
    total = TranslationStats()
    try:
        # Read the catalogue + its quizzes once.
        async with session_scope() as session:
            all_courses = await SqlAlchemyCourseRepository(session).list_courses(
                include_drafts=True
            )
            courses = select_courses(all_courses, slug=slug, limit=limit)
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


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="translate_academy",
        description="AI-translate the Academy catalogue into pt-BR/es/fr.",
    )
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--slug", help="Translate only this course slug (smoke test).")
    scope.add_argument("--limit", type=int, help="Translate only the first N courses (smoke test).")
    return parser.parse_args(argv)


async def main(argv: list[str] | None = None) -> None:
    args = _parse_args(argv)
    settings = get_settings()
    configure_logging(settings.log_level)
    try:
        if settings.openai_api_key is None:
            print("No OPENAI_API_KEY configured — nothing to translate.")
            logger.warning("academy translate — skipped (no OpenAI key)")
            return
        scope = (
            f"course '{args.slug}'"
            if args.slug
            else f"first {args.limit} course(s)"
            if args.limit
            else "the whole catalogue"
        )
        print(f"Translating {scope} into {', '.join(TARGET_LANGUAGES)} …")
        stats = await translate_content(slug=args.slug, limit=args.limit)
        print(
            f"Translation done: {stats.translated} translated, "
            f"{stats.skipped} skipped, {stats.failed} failed."
        )
    finally:
        await dispose_engine()


if __name__ == "__main__":
    asyncio.run(main())
