"""Ports the courses context depends on."""

from __future__ import annotations

from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.courses.entities import Course, CourseLevel


@runtime_checkable
class CourseRepository(Protocol):
    async def save(self, course: Course) -> None:
        """Insert or update a course **and its lessons**.

        Raises ``DuplicateCourseSlugError`` if another course already
        owns the slug.
        """
        ...

    async def get_by_slug(self, slug: str, *, include_drafts: bool = False) -> Course:
        """Load a course (with its ordered lessons) by slug. Raises
        ``CourseNotFoundError``. Drafts resolve only when
        ``include_drafts`` is true (editor scope)."""
        ...

    async def list_courses(
        self,
        *,
        level: CourseLevel | None = None,
        include_drafts: bool = False,
    ) -> list[Course]:
        """All courses ordered by (level, sort_order). Drafts are
        filtered out unless ``include_drafts`` is true. Lessons are
        included so a catalogue render needs a single round-trip."""
        ...

    async def delete(self, course_id: UUID) -> None:
        """Delete a course and its lessons. No-op if absent."""
        ...
