"""Provision the built-in Academy courses (MATLAB & Python) with their
curated lesson content.

Idempotent and non-destructive — see ``application.courses.seed``. Historically
this ran on every container boot (see the Dockerfile CMD), which reconciles the
whole catalogue and blocks ``uvicorn`` from starting (issue #259). It seeds the
English source only; translating the catalogue is a separate, heavy, on-demand
job — ``cli.translate_academy`` — already kept out of the boot path.

    python -m cyberdyne_backend.cli.seed_academy            # always seeds
    python -m cyberdyne_backend.cli.seed_academy --on-boot  # honours SEED_ACADEMY_ON_BOOT

Pass ``--on-boot`` from the container CMD: it seeds only when
``SEED_ACADEMY_ON_BOOT`` is true (the default). Ops can set that flag false and
run the plain (no-flag) invocation as a release step to move the seed off the
blocking boot path. It prints a per-course summary and exits non-zero on failure.
"""

from __future__ import annotations

import argparse
import asyncio
import logging

from cyberdyne_backend.adapters.outbound.persistence.courses.repository import (
    SqlAlchemyCategoryRepository,
    SqlAlchemyCourseRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.quizzes.repository import (
    SqlAlchemyQuizRepository,
)
from cyberdyne_backend.application.courses.categories import (
    assign_course_categories,
    seed_categories,
)
from cyberdyne_backend.application.courses.seed import seed_courses
from cyberdyne_backend.application.quizzes.use_cases import UpsertQuiz
from cyberdyne_backend.infrastructure.database.engine import dispose_engine, session_scope
from cyberdyne_backend.infrastructure.logging import configure_logging
from cyberdyne_backend.infrastructure.settings import Settings, get_settings

logger = logging.getLogger("cyberdyne_backend.cli.seed_academy")


def _should_run_seed(on_boot: bool, settings: Settings) -> bool:
    """Whether the full-catalog seed should run.

    Skipped only on the boot path (``--on-boot``) when ops has moved the
    seed to a release step by setting ``SEED_ACADEMY_ON_BOOT=false``. A
    manual (no-flag) invocation always seeds so that deploy step works.
    """
    return settings.seed_academy_on_boot if on_boot else True


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Provision the built-in Academy catalogue (idempotent)."
    )
    parser.add_argument(
        "--on-boot",
        action="store_true",
        help=(
            "Run as the container-boot seed: honour SEED_ACADEMY_ON_BOOT so ops "
            "can move seeding to a release step. Omit to always seed."
        ),
    )
    return parser.parse_args(argv)


async def main(argv: list[str] | None = None) -> None:
    settings = get_settings()
    configure_logging(settings.log_level)
    if not _should_run_seed(_parse_args(argv).on_boot, settings):
        logger.info(
            "academy seed skipped on boot (SEED_ACADEMY_ON_BOOT=false); "
            "run it as a release step instead"
        )
        return
    try:
        async with session_scope() as session:
            summary = await seed_courses(
                SqlAlchemyCourseRepository(session),
                quiz_author=UpsertQuiz(repo=SqlAlchemyQuizRepository(session)),
            )
        # Built-in categories + a slug-derived default for any uncategorized
        # course (fills gaps only — never overrides a manual reassignment).
        async with session_scope() as session:
            categories = await seed_categories(SqlAlchemyCategoryRepository(session))
            assigned = await assign_course_categories(
                SqlAlchemyCourseRepository(session), categories
            )
        for line in summary:
            logger.info("academy seed — %s", line)
        print("Academy seed applied:")
        for line in summary:
            print(f"  • {line}")
        print(f"  • categories: {len(categories)} ensured, {assigned} courses categorized")
    finally:
        await dispose_engine()


if __name__ == "__main__":
    asyncio.run(main())
