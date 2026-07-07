"""Use-case tests for the courses context, with a hand-written fake repo."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

import pytest

from cyberdyne_backend.application.courses import (
    AddLesson,
    AddLessonCommand,
    CreateCourse,
    CreateCourseCommand,
    DeleteCourse,
    DeleteLesson,
    GetCourse,
    ListCourses,
    ReorderCourses,
    ReorderLessons,
    SetCourseDeadline,
    SetCoursePublished,
    UpdateCourse,
    UpdateCourseCommand,
    UpdateLesson,
    UpdateLessonCommand,
)
from cyberdyne_backend.domain.courses import (
    Course,
    CourseLevel,
    CourseNotFoundError,
    CourseRepository,
    CourseStatus,
    InvalidLessonContentError,
    LessonNotFoundError,
    new_course,
)


class FakeCourseRepo:
    def __init__(self, seed: list[Course] | None = None) -> None:
        self._by_slug: dict[str, Course] = {c.slug: c for c in (seed or [])}

    async def save(self, course: Course) -> None:
        # Drop any stale slug entry for this id (slug is immutable in the
        # use cases, so this is just defensive).
        self._by_slug[course.slug] = course

    async def get_by_slug(
        self, slug: str, *, include_drafts: bool = False, locale: str = "en"
    ) -> Course:
        course = self._by_slug.get(slug)
        if course is None:
            raise CourseNotFoundError(slug)
        if not include_drafts and not course.is_visible_to_anonymous():
            raise CourseNotFoundError(slug)
        return course

    async def list_courses(
        self,
        *,
        level: CourseLevel | None = None,
        include_drafts: bool = False,
        locale: str = "en",
        limit: int | None = None,
        offset: int = 0,
        include_lessons: bool = True,
    ) -> list[Course]:
        items = list(self._by_slug.values())
        if not include_drafts:
            items = [c for c in items if c.is_visible_to_anonymous()]
        if level is not None:
            items = [c for c in items if c.level is level]
        items.sort(key=lambda c: (c.level.value, c.sort_order, c.title))
        if offset:
            items = items[offset:]
        if limit is not None:
            items = items[:limit]
        return items

    async def get_by_id(self, course_id: UUID) -> Course | None:
        return next((c for c in self._by_slug.values() if c.id == course_id), None)

    async def delete(self, course_id: UUID) -> None:
        self._by_slug = {s: c for s, c in self._by_slug.items() if c.id != course_id}

    async def set_category(self, course_id: UUID, category_id: UUID | None) -> None:
        for course in self._by_slug.values():
            if course.id == course_id:
                course.category = None if category_id is None else course.category


def test_fake_repo_matches_port() -> None:
    assert isinstance(FakeCourseRepo(), CourseRepository)


# ── CreateCourse ─────────────────────────────────────────────────────


class TestCreateCourse:
    async def test_creates_draft(self) -> None:
        uc = CreateCourse(repo=FakeCourseRepo())
        course = await uc.execute(
            CreateCourseCommand(title="Solidity 101", description="d", level="Beginner")
        )
        assert course.status is CourseStatus.DRAFT
        assert course.slug == "solidity-101"


# ── publish / unpublish ──────────────────────────────────────────────


class TestSetCoursePublished:
    async def test_publish_then_unpublish(self) -> None:
        course = new_course(title="x", description="d", level="Beginner")
        repo = FakeCourseRepo(seed=[course])
        uc = SetCoursePublished(repo=repo)
        published = await uc.execute(course.slug, published=True)
        assert published.status is CourseStatus.PUBLISHED
        unpublished = await uc.execute(course.slug, published=False)
        assert unpublished.status is CourseStatus.DRAFT

    async def test_missing_course_raises(self) -> None:
        uc = SetCoursePublished(repo=FakeCourseRepo())
        with pytest.raises(CourseNotFoundError):
            await uc.execute("missing", published=True)


class TestSetCourseDeadline:
    async def test_set_then_clear(self) -> None:
        course = new_course(title="x", description="d", level="Beginner")
        repo = FakeCourseRepo(seed=[course])
        uc = SetCourseDeadline(repo=repo)
        due = datetime(2030, 1, 1, tzinfo=UTC)
        updated = await uc.execute(course.slug, due_at=due)
        assert updated.due_at == due
        cleared = await uc.execute(course.slug, due_at=None)
        assert cleared.due_at is None

    async def test_works_on_draft(self) -> None:
        # Deadlines can be set before a course is published.
        course = new_course(title="draft", description="d", level="Beginner")
        repo = FakeCourseRepo(seed=[course])
        due = datetime(2030, 6, 1, tzinfo=UTC)
        updated = await SetCourseDeadline(repo=repo).execute(course.slug, due_at=due)
        assert updated.due_at == due

    async def test_missing_course_raises(self) -> None:
        with pytest.raises(CourseNotFoundError):
            await SetCourseDeadline(repo=FakeCourseRepo()).execute("missing", due_at=None)


# ── GetCourse / ListCourses visibility ───────────────────────────────


class TestVisibility:
    def _seed(self) -> FakeCourseRepo:
        draft = new_course(title="Draft", description="d", level="Beginner")
        published = new_course(title="Live", description="d", level="Beginner")
        published.publish()
        return FakeCourseRepo(seed=[draft, published])

    async def test_anon_sees_only_published(self) -> None:
        uc = ListCourses(repo=self._seed())
        courses = await uc.execute()
        assert [c.slug for c in courses] == ["live"]

    async def test_editor_sees_drafts(self) -> None:
        uc = ListCourses(repo=self._seed())
        courses = await uc.execute(include_drafts=True)
        assert {c.slug for c in courses} == {"draft", "live"}

    async def test_level_filter(self) -> None:
        beginner = new_course(title="B", description="d", level="Beginner")
        beginner.publish()
        advanced = new_course(title="A", description="d", level="Advanced")
        advanced.publish()
        uc = ListCourses(repo=FakeCourseRepo(seed=[beginner, advanced]))
        only_adv = await uc.execute(level=CourseLevel.ADVANCED)
        assert [c.slug for c in only_adv] == ["a"]

    def _seed_published(self, n: int) -> FakeCourseRepo:
        courses = []
        for i in range(n):
            c = new_course(title=f"C{i:02d}", description="d", level="Beginner", sort_order=i)
            c.publish()
            courses.append(c)
        return FakeCourseRepo(seed=courses)

    async def test_no_limit_returns_full_catalogue(self) -> None:
        uc = ListCourses(repo=self._seed_published(5))
        courses = await uc.execute()
        assert len(courses) == 5  # default: unpaged, backward-compatible

    async def test_limit_bounds_the_page(self) -> None:
        uc = ListCourses(repo=self._seed_published(5))
        courses = await uc.execute(limit=2)
        assert [c.title for c in courses] == ["C00", "C01"]

    async def test_offset_with_limit_pages(self) -> None:
        uc = ListCourses(repo=self._seed_published(5))
        courses = await uc.execute(limit=2, offset=2)
        assert [c.title for c in courses] == ["C02", "C03"]

    async def test_limit_clamped_to_ceiling(self) -> None:
        repo = self._seed_published(3)
        uc = ListCourses(repo=repo)
        # An over-cap limit must not error and still returns what exists.
        courses = await uc.execute(limit=10_000)
        assert len(courses) == 3

    async def test_get_draft_404_for_anon(self) -> None:
        uc = GetCourse(repo=self._seed())
        with pytest.raises(CourseNotFoundError):
            await uc.execute("draft")

    async def test_get_draft_visible_to_editor(self) -> None:
        uc = GetCourse(repo=self._seed())
        course = await uc.execute("draft", include_drafts=True)
        assert course.slug == "draft"


# ── UpdateCourse ─────────────────────────────────────────────────────


class TestUpdateCourse:
    async def test_updates_fields(self) -> None:
        course = new_course(title="x", description="old", level="Beginner")
        uc = UpdateCourse(repo=FakeCourseRepo(seed=[course]))
        updated = await uc.execute(
            course.slug,
            UpdateCourseCommand(description="new", mandatory=True, sort_order=3),
        )
        assert updated.description == "new"
        assert updated.mandatory is True
        assert updated.sort_order == 3

    async def test_empty_title_raises(self) -> None:
        course = new_course(title="x", description="d", level="Beginner")
        uc = UpdateCourse(repo=FakeCourseRepo(seed=[course]))
        with pytest.raises(ValueError, match="title cannot be empty"):
            await uc.execute(course.slug, UpdateCourseCommand(title="  "))


# ── DeleteCourse + ReorderCourses ────────────────────────────────────


class TestDeleteAndReorder:
    async def test_delete(self) -> None:
        course = new_course(title="x", description="d", level="Beginner")
        repo = FakeCourseRepo(seed=[course])
        await DeleteCourse(repo=repo).execute(course.slug)
        with pytest.raises(CourseNotFoundError):
            await repo.get_by_slug(course.slug, include_drafts=True)

    async def test_reorder(self) -> None:
        a = new_course(title="A", description="d", level="Beginner", sort_order=1)
        b = new_course(title="B", description="d", level="Beginner", sort_order=2)
        repo = FakeCourseRepo(seed=[a, b])
        uc = ReorderCourses(repo=repo)
        result = await uc.execute({a.slug: 20, b.slug: 10})
        by_slug = {c.slug: c.sort_order for c in result}
        assert by_slug == {a.slug: 20, b.slug: 10}


# ── Lessons ──────────────────────────────────────────────────────────


class TestLessons:
    def _course(self) -> Course:
        c = new_course(title="x", description="d", level="Beginner")
        return c

    async def test_add_lesson(self) -> None:
        course = self._course()
        repo = FakeCourseRepo(seed=[course])
        uc = AddLesson(repo=repo)
        lesson = await uc.execute(
            course.slug,
            AddLessonCommand(title="Intro", lesson_type="text", text_body="hi"),
        )
        assert lesson.title == "Intro"
        reloaded = await repo.get_by_slug(course.slug, include_drafts=True)
        assert len(reloaded.lessons) == 1

    async def test_add_lesson_invalid_content(self) -> None:
        course = self._course()
        uc = AddLesson(repo=FakeCourseRepo(seed=[course]))
        with pytest.raises(InvalidLessonContentError):
            await uc.execute(course.slug, AddLessonCommand(title="v", lesson_type="video"))

    async def test_update_lesson(self) -> None:
        course = self._course()
        repo = FakeCourseRepo(seed=[course])
        lesson = await AddLesson(repo=repo).execute(
            course.slug, AddLessonCommand(title="t", lesson_type="text", text_body="a")
        )
        updated = await UpdateLesson(repo=repo).execute(
            course.slug, lesson.id, UpdateLessonCommand(text_body="b")
        )
        assert updated.text_body == "b"

    async def test_update_missing_lesson_raises(self) -> None:
        course = self._course()
        uc = UpdateLesson(repo=FakeCourseRepo(seed=[course]))
        import uuid

        with pytest.raises(LessonNotFoundError):
            await uc.execute(course.slug, uuid.uuid4(), UpdateLessonCommand(title="x"))

    async def test_delete_lesson(self) -> None:
        course = self._course()
        repo = FakeCourseRepo(seed=[course])
        lesson = await AddLesson(repo=repo).execute(
            course.slug, AddLessonCommand(title="t", lesson_type="quiz")
        )
        await DeleteLesson(repo=repo).execute(course.slug, lesson.id)
        reloaded = await repo.get_by_slug(course.slug, include_drafts=True)
        assert reloaded.lessons == []

    async def test_reorder_lessons(self) -> None:
        course = self._course()
        repo = FakeCourseRepo(seed=[course])
        l1 = await AddLesson(repo=repo).execute(
            course.slug, AddLessonCommand(title="one", lesson_type="quiz", sort_order=1)
        )
        l2 = await AddLesson(repo=repo).execute(
            course.slug, AddLessonCommand(title="two", lesson_type="quiz", sort_order=2)
        )
        result = await ReorderLessons(repo=repo).execute(course.slug, {l1.id: 10, l2.id: 1})
        # Sorted ascending by new sort_order → l2 first.
        assert [les.id for les in result.lessons] == [l2.id, l1.id]
