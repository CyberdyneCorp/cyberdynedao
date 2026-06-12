"""Provision the built-in Academy courses (MATLAB & Python) with their
curated lesson content.

Idempotent and non-destructive — see ``application.courses.seed``. Runs on
container boot (see the Dockerfile CMD), so it must stay fast: it seeds the
English source only. Translating the catalogue into other languages is a
separate, heavy, on-demand job — ``cli.translate_academy`` — kept out of the
boot path so the API starts promptly.

    python -m cyberdyne_backend.cli.seed_academy

It prints a per-course summary and exits non-zero on failure.
"""

from __future__ import annotations

import asyncio
import logging

from cyberdyne_backend.adapters.outbound.persistence.courses.repository import (
    SqlAlchemyCourseRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.quizzes.repository import (
    SqlAlchemyQuizRepository,
)
from cyberdyne_backend.application.courses.seed import seed_courses
from cyberdyne_backend.application.quizzes.use_cases import UpsertQuiz
from cyberdyne_backend.infrastructure.database.engine import dispose_engine, session_scope
from cyberdyne_backend.infrastructure.logging import configure_logging
from cyberdyne_backend.infrastructure.settings import get_settings

logger = logging.getLogger("cyberdyne_backend.cli.seed_academy")


async def main() -> None:
    configure_logging(get_settings().log_level)
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
    finally:
        await dispose_engine()


if __name__ == "__main__":
    asyncio.run(main())
