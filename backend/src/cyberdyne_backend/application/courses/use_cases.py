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
    MAX_COURSE_LIST_LIMIT,
    Category,
    CategoryNotFoundError,
    CategoryRepository,
    Course,
    CourseLevel,
    CourseRepository,
    Lesson,
    LessonNotFoundError,
    new_category,
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
        locale: str = "en",
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Course]:
        # limit=None preserves the original full-catalogue behaviour; a
        # supplied limit is clamped to a safe ceiling and offset floored.
        clamped = None if limit is None else max(1, min(limit, MAX_COURSE_LIST_LIMIT))
        return await self.repo.list_courses(
            level=level,
            include_drafts=include_drafts,
            locale=locale,
            limit=clamped,
            offset=max(0, offset),
        )


@dataclass(slots=True)
class GetCourse:
    repo: CourseRepository

    async def execute(
        self, slug: str, *, include_drafts: bool = False, locale: str = "en"
    ) -> Course:
        return await self.repo.get_by_slug(slug, include_drafts=include_drafts, locale=locale)


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


# ── Categories ────────────────────────────────────────────────────────


@dataclass(slots=True)
class ListCategories:
    repo: CategoryRepository

    async def execute(self) -> list[Category]:
        return await self.repo.list_categories()


async def _validated_parent(
    repo: CategoryRepository, parent_id: UUID | None, *, child_id: UUID | None = None
) -> None:
    """Validate a parent assignment: the parent must exist, be top-level (so the
    hierarchy stays one level deep), and not be the category itself."""
    if parent_id is None:
        return
    if child_id is not None and parent_id == child_id:
        raise ValueError("a category cannot be its own parent")
    parent = await repo.get_by_id(parent_id)
    if parent is None:
        raise CategoryNotFoundError(str(parent_id))
    if parent.parent_id is not None:
        raise ValueError("parent must be a top-level category (max one level of nesting)")


@dataclass(slots=True)
class CreateCategoryCommand:
    name: str
    slug: str | None = None
    icon: str = ""
    sort_order: int = 0
    parent_id: UUID | None = None


@dataclass(slots=True)
class CreateCategory:
    repo: CategoryRepository

    async def execute(self, cmd: CreateCategoryCommand) -> Category:
        await _validated_parent(self.repo, cmd.parent_id)
        category = new_category(
            name=cmd.name,
            slug=cmd.slug,
            icon=cmd.icon,
            sort_order=cmd.sort_order,
            parent_id=cmd.parent_id,
        )
        await self.repo.save(category)
        return category


@dataclass(slots=True)
class UpdateCategory:
    """Edit a category's name/icon/sort_order and optionally reparent it.
    ``set_parent`` distinguishes 'leave parent as-is' from 'set parent to
    ``parent_id`` (possibly None → top-level)'."""

    repo: CategoryRepository

    async def execute(
        self,
        category_id: UUID,
        *,
        name: str | None = None,
        icon: str | None = None,
        sort_order: int | None = None,
        set_parent: bool = False,
        parent_id: UUID | None = None,
    ) -> Category:
        category = await self.repo.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError(str(category_id))
        if name is not None:
            if not name.strip():
                raise ValueError("name cannot be empty")
            category.name = name.strip()
        if icon is not None:
            category.icon = icon.strip()
        if sort_order is not None:
            category.sort_order = sort_order
        if set_parent:
            await _validated_parent(self.repo, parent_id, child_id=category_id)
            category.parent_id = parent_id
        await self.repo.save(category)
        return category


@dataclass(slots=True)
class DeleteCategory:
    repo: CategoryRepository

    async def execute(self, category_id: UUID) -> None:
        # Courses referencing it become uncategorized (FK ON DELETE SET NULL),
        # and any child categories are promoted to top level (self-FK SET NULL).
        await self.repo.delete(category_id)


@dataclass(slots=True)
class SetCourseCategory:
    """Assign (or clear, with ``category_id=None``) a course's category."""

    course_repo: CourseRepository
    category_repo: CategoryRepository

    async def execute(self, slug: str, category_id: UUID | None) -> Course:
        course = await self.course_repo.get_by_slug(slug, include_drafts=True)
        if category_id is not None and await self.category_repo.get_by_id(category_id) is None:
            raise CategoryNotFoundError(str(category_id))
        await self.course_repo.set_category(course.id, category_id)
        return await self.course_repo.get_by_slug(slug, include_drafts=True)


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
