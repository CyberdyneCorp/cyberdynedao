"""Domain + use-case tests for per-lesson progress / per-course completion."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from uuid import UUID

import pytest

from cyberdyne_backend.application.courses import GetMyCourseProgress, SetLessonProgress
from cyberdyne_backend.domain.courses import (
    Course,
    CourseNotFoundError,
    CourseProgressRepository,
    LessonNotFoundError,
    LessonProgress,
    ProgressOutOfRangeError,
    build_course_progress,
    new_course,
    new_lesson,
    new_lesson_progress,
)

# ── Domain ────────────────────────────────────────────────────────────


class TestLessonProgressEntity:
    def _progress(self) -> LessonProgress:
        return new_lesson_progress(
            user_id=uuid.uuid4(), course_id=uuid.uuid4(), lesson_id=uuid.uuid4()
        )

    def test_starts_not_completed(self) -> None:
        p = self._progress()
        assert p.percent == 0
        assert p.completed_at is None
        assert p.is_completed is False

    def test_completion_sets_marker(self) -> None:
        p = self._progress()
        p.update(100, now=datetime(2030, 1, 1, tzinfo=UTC))
        assert p.is_completed is True
        assert p.completed_at == datetime(2030, 1, 1, tzinfo=UTC)

    def test_reopening_clears_marker(self) -> None:
        p = self._progress()
        p.update(100)
        p.update(40)
        assert p.completed_at is None
        assert p.is_completed is False

    def test_created_at_full_is_completed(self) -> None:
        p = new_lesson_progress(
            user_id=uuid.uuid4(), course_id=uuid.uuid4(), lesson_id=uuid.uuid4(), percent=100
        )
        assert p.is_completed is True

    @pytest.mark.parametrize("bad", [-1, 101, 200])
    def test_out_of_range_raises(self, bad: int) -> None:
        with pytest.raises(ProgressOutOfRangeError):
            self._progress().update(bad)

    def test_factory_rejects_out_of_range(self) -> None:
        with pytest.raises(ProgressOutOfRangeError):
            new_lesson_progress(
                user_id=uuid.uuid4(), course_id=uuid.uuid4(), lesson_id=uuid.uuid4(), percent=150
            )


class TestBuildCourseProgress:
    def test_empty_course_is_zero_and_incomplete(self) -> None:
        cp = build_course_progress(
            course_id=uuid.uuid4(), slug="x", lessons=[], progress_by_lesson={}
        )
        assert cp.percent == 0
        assert cp.completed is False
        assert cp.total_lessons == 0

    def test_partial_completion(self) -> None:
        l1, l2 = uuid.uuid4(), uuid.uuid4()
        done = new_lesson_progress(
            user_id=uuid.uuid4(), course_id=uuid.uuid4(), lesson_id=l1, percent=100
        )
        cp = build_course_progress(
            course_id=uuid.uuid4(),
            slug="x",
            lessons=[(l1, "One"), (l2, "Two")],
            progress_by_lesson={l1: done},
        )
        assert cp.completed_lessons == 1
        assert cp.percent == 50
        assert cp.completed is False
        assert [v.completed for v in cp.lessons] == [True, False]

    def test_full_completion(self) -> None:
        l1 = uuid.uuid4()
        done = new_lesson_progress(
            user_id=uuid.uuid4(), course_id=uuid.uuid4(), lesson_id=l1, percent=100
        )
        cp = build_course_progress(
            course_id=uuid.uuid4(),
            slug="x",
            lessons=[(l1, "One")],
            progress_by_lesson={l1: done},
        )
        assert cp.percent == 100
        assert cp.completed is True


# ── Use cases (fakes) ─────────────────────────────────────────────────


class FakeCourseRepo:
    def __init__(self, course: Course | None = None) -> None:
        self._course = course

    async def save(self, course: Course) -> None:  # pragma: no cover - unused
        raise NotImplementedError

    async def get_by_slug(self, slug: str, *, include_drafts: bool = False) -> Course:
        if self._course is None or self._course.slug != slug:
            raise CourseNotFoundError(slug)
        return self._course

    async def list_courses(self, *, level: object = None, include_drafts: bool = False):  # type: ignore[no-untyped-def]
        raise NotImplementedError  # pragma: no cover - unused

    async def delete(self, course_id: UUID) -> None:  # pragma: no cover - unused
        raise NotImplementedError


class FakeProgressRepo:
    def __init__(self) -> None:
        self.rows: dict[tuple[UUID, UUID], LessonProgress] = {}

    async def get_lesson_progress(self, *, user_id: UUID, lesson_id: UUID) -> LessonProgress | None:
        return self.rows.get((user_id, lesson_id))

    async def upsert_lesson_progress(self, progress: LessonProgress) -> None:
        self.rows[(progress.user_id, progress.lesson_id)] = progress

    async def list_course_progress(self, *, user_id: UUID, course_id: UUID) -> list[LessonProgress]:
        return [p for (u, _), p in self.rows.items() if u == user_id and p.course_id == course_id]


def test_fake_progress_matches_port() -> None:
    assert isinstance(FakeProgressRepo(), CourseProgressRepository)


def _course_with_lessons(n: int) -> Course:
    course = new_course(title="Solidity", description="d", level="Beginner")
    course.lessons = [
        new_lesson(
            course_id=course.id, title=f"L{i}", lesson_type="text", text_body="b", sort_order=i
        )
        for i in range(n)
    ]
    return course


class TestSetLessonProgress:
    async def test_marks_lesson_and_aggregates(self) -> None:
        course = _course_with_lessons(2)
        repo, prog = FakeCourseRepo(course), FakeProgressRepo()
        uc = SetLessonProgress(courses=repo, progress=prog)
        user = uuid.uuid4()

        cp = await uc.execute(
            user_id=user, slug=course.slug, lesson_id=course.lessons[0].id, percent=100
        )
        assert cp.completed_lessons == 1
        assert cp.percent == 50
        assert cp.completed is False

        cp = await uc.execute(
            user_id=user, slug=course.slug, lesson_id=course.lessons[1].id, percent=100
        )
        assert cp.percent == 100
        assert cp.completed is True

    async def test_idempotent_update_does_not_double_count(self) -> None:
        course = _course_with_lessons(2)
        uc = SetLessonProgress(courses=FakeCourseRepo(course), progress=FakeProgressRepo())
        user = uuid.uuid4()
        await uc.execute(
            user_id=user, slug=course.slug, lesson_id=course.lessons[0].id, percent=100
        )
        cp = await uc.execute(
            user_id=user, slug=course.slug, lesson_id=course.lessons[0].id, percent=100
        )
        assert cp.completed_lessons == 1

    async def test_lesson_not_in_course_raises(self) -> None:
        course = _course_with_lessons(1)
        uc = SetLessonProgress(courses=FakeCourseRepo(course), progress=FakeProgressRepo())
        with pytest.raises(LessonNotFoundError):
            await uc.execute(
                user_id=uuid.uuid4(), slug=course.slug, lesson_id=uuid.uuid4(), percent=50
            )

    async def test_unknown_course_raises(self) -> None:
        uc = SetLessonProgress(courses=FakeCourseRepo(None), progress=FakeProgressRepo())
        with pytest.raises(CourseNotFoundError):
            await uc.execute(user_id=uuid.uuid4(), slug="nope", lesson_id=uuid.uuid4(), percent=10)


class TestGetMyCourseProgress:
    async def test_reads_aggregate(self) -> None:
        course = _course_with_lessons(2)
        repo, prog = FakeCourseRepo(course), FakeProgressRepo()
        user = uuid.uuid4()
        await SetLessonProgress(courses=repo, progress=prog).execute(
            user_id=user, slug=course.slug, lesson_id=course.lessons[0].id, percent=100
        )
        cp = await GetMyCourseProgress(courses=repo, progress=prog).execute(
            user_id=user, slug=course.slug
        )
        assert cp.total_lessons == 2
        assert cp.completed_lessons == 1

    async def test_no_progress_is_zero(self) -> None:
        course = _course_with_lessons(3)
        cp = await GetMyCourseProgress(
            courses=FakeCourseRepo(course), progress=FakeProgressRepo()
        ).execute(user_id=uuid.uuid4(), slug=course.slug)
        assert cp.percent == 0
        assert all(v.completed is False for v in cp.lessons)
