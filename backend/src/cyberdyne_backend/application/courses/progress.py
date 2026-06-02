"""Per-lesson progress + per-course completion use cases.

A learner records progress against a course's lessons; the course's own
completion is derived (complete iff every lesson is). Reads and writes
resolve the course by slug (published only — drafts aren't consumable),
and validate that the lesson actually belongs to that course before
touching progress.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from cyberdyne_backend.domain.courses import (
    Course,
    CourseProgress,
    CourseProgressRepository,
    CourseRepository,
    LessonNotFoundError,
    build_course_progress,
    new_lesson_progress,
)
from cyberdyne_backend.domain.courses.progress import LessonProgress


def _course_progress(course: Course, rows: list[LessonProgress]) -> CourseProgress:
    return build_course_progress(
        course_id=course.id,
        slug=course.slug,
        lessons=[(lesson.id, lesson.title) for lesson in course.lessons],
        progress_by_lesson={row.lesson_id: row for row in rows},
    )


@dataclass(slots=True)
class SetLessonProgress:
    courses: CourseRepository
    progress: CourseProgressRepository

    async def execute(
        self, *, user_id: UUID, slug: str, lesson_id: UUID, percent: int
    ) -> CourseProgress:
        course = await self.courses.get_by_slug(slug)  # CourseNotFoundError if absent
        if not any(lesson.id == lesson_id for lesson in course.lessons):
            raise LessonNotFoundError(f"lesson {lesson_id} is not part of course {slug}")
        existing = await self.progress.get_lesson_progress(user_id=user_id, lesson_id=lesson_id)
        if existing is None:
            existing = new_lesson_progress(
                user_id=user_id,
                course_id=course.id,
                lesson_id=lesson_id,
                percent=percent,
            )
        else:
            existing.update(percent)
        await self.progress.upsert_lesson_progress(existing)
        rows = await self.progress.list_course_progress(user_id=user_id, course_id=course.id)
        return _course_progress(course, rows)


@dataclass(slots=True)
class GetMyCourseProgress:
    courses: CourseRepository
    progress: CourseProgressRepository

    async def execute(self, *, user_id: UUID, slug: str) -> CourseProgress:
        course = await self.courses.get_by_slug(slug)  # CourseNotFoundError if absent
        rows = await self.progress.list_course_progress(user_id=user_id, course_id=course.id)
        return _course_progress(course, rows)


__all__ = [
    "GetMyCourseProgress",
    "SetLessonProgress",
]
