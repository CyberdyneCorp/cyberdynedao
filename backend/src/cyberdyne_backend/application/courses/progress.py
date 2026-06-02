"""Per-lesson progress + per-course completion use cases.

A learner records progress against a course's lessons; the course's own
completion is derived (complete iff every lesson is). Reads and writes
resolve the course by slug (published only — drafts aren't consumable),
and validate that the lesson actually belongs to that course before
touching progress.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from cyberdyne_backend.domain.courses import (
    Course,
    CourseCertificateAwarder,
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
    # Optional: when the course tips into "complete", auto-award its
    # certificate. None keeps progress self-contained (e.g. in tests).
    awarder: CourseCertificateAwarder | None = field(default=None)

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
        result = _course_progress(course, rows)
        if result.completed and self.awarder is not None:
            await self.awarder.award_if_complete(user_id=user_id, course_id=course.id)
        return result


@dataclass(slots=True)
class GetMyCourseProgress:
    courses: CourseRepository
    progress: CourseProgressRepository

    async def execute(self, *, user_id: UUID, slug: str) -> CourseProgress:
        course = await self.courses.get_by_slug(slug)  # CourseNotFoundError if absent
        rows = await self.progress.list_course_progress(user_id=user_id, course_id=course.id)
        return _course_progress(course, rows)


@dataclass(slots=True)
class CourseLessonCompleter:
    """Marks a lesson 100% complete — the courses-side implementation of
    the quizzes ``LessonCompleter`` seam, so passing a quiz auto-completes
    its lesson. A lesson outside any course (no owning course id) is a
    safe no-op."""

    progress: CourseProgressRepository
    # Optional: auto-award the course certificate if this completion
    # finishes the course (e.g. the last lesson was a passed quiz).
    awarder: CourseCertificateAwarder | None = field(default=None)

    async def complete_lesson(self, *, user_id: UUID, lesson_id: UUID) -> None:
        course_id = await self.progress.get_lesson_course_id(lesson_id)
        if course_id is None:
            return
        existing = await self.progress.get_lesson_progress(user_id=user_id, lesson_id=lesson_id)
        if existing is None:
            existing = new_lesson_progress(
                user_id=user_id, course_id=course_id, lesson_id=lesson_id, percent=100
            )
        else:
            existing.update(100)
        await self.progress.upsert_lesson_progress(existing)
        if self.awarder is not None:
            await self.awarder.award_if_complete(user_id=user_id, course_id=course_id)


__all__ = [
    "CourseLessonCompleter",
    "GetMyCourseProgress",
    "SetLessonProgress",
]
