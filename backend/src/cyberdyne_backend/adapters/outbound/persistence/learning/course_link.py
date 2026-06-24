"""Adapter implementing the learning context's ``CourseLinkReader`` port over
the *courses* context's repositories.

It lets a course-backed module (stage) validate its linked courses and derive
its completion from real course progress, without the courses context knowing
about learning. Percent-per-course is computed exactly like
``application.courses.ListMyCourseProgress`` (a course is complete iff every
lesson is), in two queries rather than N+1.
"""

from __future__ import annotations

from uuid import UUID

from cyberdyne_backend.domain.courses import (
    CourseProgressRepository,
    CourseRepository,
    build_course_progress,
)
from cyberdyne_backend.domain.courses.progress import LessonProgress


class SqlAlchemyCourseLinkReader:
    def __init__(self, courses: CourseRepository, progress: CourseProgressRepository) -> None:
        self._courses = courses
        self._progress = progress

    async def existing_course_slugs(self) -> set[str]:
        courses = await self._courses.list_courses(include_drafts=False)
        return {course.slug for course in courses}

    async def percent_by_course(self, user_id: UUID) -> dict[str, int]:
        courses = await self._courses.list_courses(include_drafts=False)
        rows = await self._progress.list_all_progress_for_user(user_id=user_id)
        by_course: dict[UUID, dict[UUID, LessonProgress]] = {}
        for row in rows:
            by_course.setdefault(row.course_id, {})[row.lesson_id] = row
        return {
            course.slug: build_course_progress(
                course_id=course.id,
                slug=course.slug,
                lessons=[(lesson.id, lesson.title) for lesson in course.lessons],
                progress_by_lesson=by_course.get(course.id, {}),
            ).percent
            for course in courses
        }
