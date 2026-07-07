"""Repository-level regression tests for the courses list read (issue #258).

Runs against the in-memory aiosqlite engine bound in ``conftest`` — no
Postgres required — and asserts the count-only path (``include_lessons=False``)
sizes ``lesson_count`` with a COUNT aggregate WITHOUT hydrating a single lesson
``text_body`` (the over-fetch the issue reports), while the default path still
loads full lessons for the callers that need them.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator

import pytest
import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.courses.repository import (
    SqlAlchemyCourseRepository,
)
from cyberdyne_backend.domain.courses import CourseStatus, new_course, new_lesson
from cyberdyne_backend.infrastructure.database.engine import get_engine

pytestmark = pytest.mark.usefixtures("_prepared_schema")


@pytest_asyncio.fixture
async def seeded_repo(db_session: AsyncSession) -> AsyncIterator[SqlAlchemyCourseRepository]:
    """A published course with three text lessons, each with a real body."""
    course = new_course(title="Algebra", description="Learn algebra", level="Beginner", slug="alg")
    course.status = CourseStatus.PUBLISHED
    for i in range(3):
        course.lessons.append(
            new_lesson(
                course_id=course.id,
                title=f"Lesson {i}",
                lesson_type="text",
                text_body=f"# Heading {i}\n\nSome long markdown body number {i}.",
                sort_order=i,
            )
        )
    repo = SqlAlchemyCourseRepository(db_session)
    await repo.save(course)
    yield repo


@pytest.fixture
def captured_sql() -> Iterator[list[str]]:
    """Capture every SQL statement the shared engine emits during the test."""
    statements: list[str] = []
    engine = get_engine().sync_engine

    def _record(conn, cursor, statement, parameters, context, executemany) -> None:  # type: ignore[no-untyped-def]
        statements.append(statement)

    event.listen(engine, "before_cursor_execute", _record)
    try:
        yield statements
    finally:
        event.remove(engine, "before_cursor_execute", _record)


async def test_count_only_read_does_not_hydrate_lesson_bodies(
    seeded_repo: SqlAlchemyCourseRepository, captured_sql: list[str]
) -> None:
    courses = await seeded_repo.list_courses(include_lessons=False)

    assert len(courses) == 1
    course = courses[0]
    # Count is correct...
    assert course.lesson_count == 3
    # ...without any lesson row (and thus body) being hydrated.
    assert course.lessons == []
    # And no emitted statement selected the heavy lesson body column.
    assert not any("text_body" in stmt for stmt in captured_sql), captured_sql


async def test_default_read_still_hydrates_lessons(
    seeded_repo: SqlAlchemyCourseRepository,
) -> None:
    # The default (used by progress / AI / category callers) is unchanged:
    # lessons come back fully, and lesson_count stays None so the summary
    # builder falls back to len(lessons).
    courses = await seeded_repo.list_courses()

    assert len(courses) == 1
    course = courses[0]
    assert course.lesson_count is None
    assert [le.title for le in course.lessons] == ["Lesson 0", "Lesson 1", "Lesson 2"]
    assert course.lessons[0].text_body is not None
