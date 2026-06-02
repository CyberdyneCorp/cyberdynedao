"""Ports the courses context depends on."""

from __future__ import annotations

from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.courses.entities import Course, CourseLevel
from cyberdyne_backend.domain.courses.progress import LessonProgress


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


@runtime_checkable
class CourseProgressRepository(Protocol):
    """Persists per-lesson learner progress for the courses context."""

    async def get_lesson_progress(self, *, user_id: UUID, lesson_id: UUID) -> LessonProgress | None:
        """The learner's row for a single lesson, or ``None`` if they
        have not started it."""
        ...

    async def upsert_lesson_progress(self, progress: LessonProgress) -> None:
        """Insert or update a learner's progress for one lesson."""
        ...

    async def list_course_progress(self, *, user_id: UUID, course_id: UUID) -> list[LessonProgress]:
        """Every lesson-progress row the learner has within a course."""
        ...
