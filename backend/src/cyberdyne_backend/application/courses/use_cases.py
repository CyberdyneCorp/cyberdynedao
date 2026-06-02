"""Use cases for the courses context.

Public reads (list / get) plus admin authoring: course CRUD, publish /
unpublish, drag-to-reorder, and lesson CRUD + reorder. Every mutating
use case loads the aggregate, mutates it in the domain, then hands the
whole ``Course`` (lessons included) back to the repository to persist.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from cyberdyne_backend.domain.courses import (
    Course,
    CourseLevel,
    CourseRepository,
    Lesson,
    LessonNotFoundError,
    new_course,
    new_lesson,
)

# ── Reads ─────────────────────────────────────────────────────────────


@dataclass(slots=True)
class ListCourses:
    repo: CourseRepository

    async def execute(
        self,
        *,
        level: CourseLevel | None = None,
        include_drafts: bool = False,
    ) -> list[Course]:
        return await self.repo.list_courses(level=level, include_drafts=include_drafts)


@dataclass(slots=True)
class GetCourse:
    repo: CourseRepository

    async def execute(self, slug: str, *, include_drafts: bool = False) -> Course:
        return await self.repo.get_by_slug(slug, include_drafts=include_drafts)


# ── Course authoring ──────────────────────────────────────────────────


@dataclass(slots=True)
class CreateCourseCommand:
    title: str
    description: str
    level: str
    slug: str | None = None
    mandatory: bool = False
    sort_order: int = 0


@dataclass(slots=True)
class CreateCourse:
    repo: CourseRepository

    async def execute(self, cmd: CreateCourseCommand) -> Course:
        course = new_course(
            title=cmd.title,
            description=cmd.description,
            level=cmd.level,
            slug=cmd.slug,
            mandatory=cmd.mandatory,
            sort_order=cmd.sort_order,
        )
        await self.repo.save(course)
        return course


@dataclass(slots=True)
class UpdateCourseCommand:
    title: str | None = None
    description: str | None = None
    mandatory: bool | None = None
    sort_order: int | None = None


@dataclass(slots=True)
class UpdateCourse:
    """Edit a course's editable fields. Level and slug are immutable
    here — a level change is a reorder concern and a slug change would
    break inbound links, so both are intentionally out of scope."""

    repo: CourseRepository

    async def execute(self, slug: str, cmd: UpdateCourseCommand) -> Course:
        course = await self.repo.get_by_slug(slug, include_drafts=True)
        if cmd.title is not None:
            if not cmd.title.strip():
                raise ValueError("title cannot be empty")
            course.title = cmd.title.strip()
        if cmd.description is not None:
            course.description = cmd.description.strip()
        if cmd.mandatory is not None:
            course.mandatory = cmd.mandatory
        if cmd.sort_order is not None:
            course.sort_order = cmd.sort_order
        await self.repo.save(course)
        return course


@dataclass(slots=True)
class SetCoursePublished:
    """Publish or unpublish a course."""

    repo: CourseRepository

    async def execute(self, slug: str, *, published: bool) -> Course:
        course = await self.repo.get_by_slug(slug, include_drafts=True)
        if published:
            course.publish()
        else:
            course.unpublish()
        await self.repo.save(course)
        return course


@dataclass(slots=True)
class SetCourseDeadline:
    """Admin-only. Set (or clear, with ``due_at=None``) a course's
    completion deadline. The overdue/urgent/upcoming status is derived at
    the read boundary, not stored."""

    repo: CourseRepository

    async def execute(self, slug: str, *, due_at: datetime | None) -> Course:
        course = await self.repo.get_by_slug(slug, include_drafts=True)
        course.set_deadline(due_at)
        await self.repo.save(course)
        return course


@dataclass(slots=True)
class DeleteCourse:
    repo: CourseRepository

    async def execute(self, slug: str) -> None:
        course = await self.repo.get_by_slug(slug, include_drafts=True)
        await self.repo.delete(course.id)


@dataclass(slots=True)
class ReorderCourses:
    """Apply a new ``sort_order`` to a batch of courses (drag-to-reorder
    within a level). Accepts ``{slug: sort_order}`` and persists each."""

    repo: CourseRepository

    async def execute(self, order_by_slug: dict[str, int]) -> list[Course]:
        updated: list[Course] = []
        for slug, order in order_by_slug.items():
            course = await self.repo.get_by_slug(slug, include_drafts=True)
            course.sort_order = order
            await self.repo.save(course)
            updated.append(course)
        return updated


# ── Lesson authoring ──────────────────────────────────────────────────


@dataclass(slots=True)
class AddLessonCommand:
    title: str
    lesson_type: str
    content_url: str | None = None
    text_body: str | None = None
    duration: str | None = None
    sort_order: int = 0


@dataclass(slots=True)
class AddLesson:
    repo: CourseRepository

    async def execute(self, course_slug: str, cmd: AddLessonCommand) -> Lesson:
        course = await self.repo.get_by_slug(course_slug, include_drafts=True)
        lesson = new_lesson(
            course_id=course.id,
            title=cmd.title,
            lesson_type=cmd.lesson_type,
            content_url=cmd.content_url,
            text_body=cmd.text_body,
            duration=cmd.duration,
            sort_order=cmd.sort_order,
        )
        course.lessons.append(lesson)
        await self.repo.save(course)
        return lesson


@dataclass(slots=True)
class UpdateLessonCommand:
    title: str | None = None
    content_url: str | None = None
    text_body: str | None = None
    duration: str | None = None
    sort_order: int | None = None


@dataclass(slots=True)
class UpdateLesson:
    repo: CourseRepository

    async def execute(self, course_slug: str, lesson_id: UUID, cmd: UpdateLessonCommand) -> Lesson:
        course = await self.repo.get_by_slug(course_slug, include_drafts=True)
        lesson = _find_lesson(course, lesson_id)
        lesson.set_content(
            title=cmd.title,
            content_url=cmd.content_url,
            text_body=cmd.text_body,
            duration=cmd.duration,
            sort_order=cmd.sort_order,
        )
        await self.repo.save(course)
        return lesson


@dataclass(slots=True)
class DeleteLesson:
    repo: CourseRepository

    async def execute(self, course_slug: str, lesson_id: UUID) -> None:
        course = await self.repo.get_by_slug(course_slug, include_drafts=True)
        lesson = _find_lesson(course, lesson_id)
        course.lessons.remove(lesson)
        await self.repo.save(course)


@dataclass(slots=True)
class ReorderLessons:
    """Apply a new ``sort_order`` to a course's lessons in one shot."""

    repo: CourseRepository

    async def execute(self, course_slug: str, order_by_id: dict[UUID, int]) -> Course:
        course = await self.repo.get_by_slug(course_slug, include_drafts=True)
        for lesson in course.lessons:
            if lesson.id in order_by_id:
                lesson.sort_order = order_by_id[lesson.id]
        course.lessons.sort(key=lambda les: les.sort_order)
        await self.repo.save(course)
        return course


def _find_lesson(course: Course, lesson_id: UUID) -> Lesson:
    for lesson in course.lessons:
        if lesson.id == lesson_id:
            return lesson
    raise LessonNotFoundError(str(lesson_id))


__all__ = [
    "AddLesson",
    "AddLessonCommand",
    "CreateCourse",
    "CreateCourseCommand",
    "DeleteCourse",
    "DeleteLesson",
    "GetCourse",
    "ListCourses",
    "ReorderCourses",
    "ReorderLessons",
    "SetCourseDeadline",
    "SetCoursePublished",
    "UpdateCourse",
    "UpdateCourseCommand",
    "UpdateLesson",
    "UpdateLessonCommand",
]
