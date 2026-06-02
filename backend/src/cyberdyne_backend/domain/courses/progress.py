"""Per-lesson learner progress + per-course completion (courses context).

This is course-scoped progress, keyed by ``(user_id, lesson_id)`` — it is
deliberately separate from the ``learning`` context's path/module
progress, which tracks a different (slug-keyed) catalogue. A learner's
standing in a *course* is derived purely from how many of that course's
lessons they've completed; the course is complete iff every lesson is.

Invariant on ``LessonProgress`` (mirrors ``learning.ModuleProgress``):
``completed_at`` is non-null iff ``percent == 100``. Enforced by the
factory + ``update``; the persistence adapter never writes ``percent``
and ``completed_at`` independently.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from cyberdyne_backend.domain.courses.errors import ProgressOutOfRangeError


@dataclass(slots=True)
class LessonProgress:
    id: UUID
    user_id: UUID
    course_id: UUID
    lesson_id: UUID
    percent: int
    started_at: datetime
    completed_at: datetime | None = None
    updated_at: datetime | None = None

    def update(self, new_percent: int, now: datetime | None = None) -> None:
        if not 0 <= new_percent <= 100:
            raise ProgressOutOfRangeError(f"percent must be 0..100, got {new_percent}")
        moment = now or datetime.now(tz=UTC)
        self.percent = new_percent
        self.updated_at = moment
        if new_percent == 100 and self.completed_at is None:
            self.completed_at = moment
        elif new_percent < 100:
            # Re-opening a completed lesson clears the completion marker.
            self.completed_at = None

    @property
    def is_completed(self) -> bool:
        return self.percent == 100 and self.completed_at is not None


def new_lesson_progress(
    *,
    user_id: UUID,
    course_id: UUID,
    lesson_id: UUID,
    percent: int = 0,
    now: datetime | None = None,
) -> LessonProgress:
    if not 0 <= percent <= 100:
        raise ProgressOutOfRangeError(f"percent must be 0..100, got {percent}")
    moment = now or datetime.now(tz=UTC)
    progress = LessonProgress(
        id=uuid.uuid4(),
        user_id=user_id,
        course_id=course_id,
        lesson_id=lesson_id,
        percent=0,
        started_at=moment,
        updated_at=moment,
    )
    # Route through ``update`` so the completed_at invariant holds even
    # when a lesson is created already at 100%.
    progress.update(percent, now=moment)
    return progress


@dataclass(frozen=True, slots=True)
class LessonProgressView:
    """One lesson's standing within a course, for the progress read."""

    lesson_id: UUID
    title: str
    percent: int
    completed: bool


@dataclass(frozen=True, slots=True)
class CourseProgress:
    """A learner's computed standing in a single course."""

    course_id: UUID
    slug: str
    total_lessons: int
    completed_lessons: int
    percent: int
    completed: bool
    lessons: list[LessonProgressView] = field(default_factory=list)


def build_course_progress(
    *,
    course_id: UUID,
    slug: str,
    lessons: list[tuple[UUID, str]],
    progress_by_lesson: dict[UUID, LessonProgress],
) -> CourseProgress:
    """Aggregate per-lesson progress into a course summary.

    ``lessons`` is the course's ordered ``(lesson_id, title)`` pairs;
    ``progress_by_lesson`` maps lesson id -> the learner's row (absent =
    not started). A course with no lessons is 0% and not complete.
    """
    views: list[LessonProgressView] = []
    completed_count = 0
    for lesson_id, title in lessons:
        row = progress_by_lesson.get(lesson_id)
        percent = row.percent if row is not None else 0
        completed = row.is_completed if row is not None else False
        if completed:
            completed_count += 1
        views.append(
            LessonProgressView(
                lesson_id=lesson_id, title=title, percent=percent, completed=completed
            )
        )
    total = len(views)
    course_percent = round(completed_count / total * 100) if total else 0
    return CourseProgress(
        course_id=course_id,
        slug=slug,
        total_lessons=total,
        completed_lessons=completed_count,
        percent=course_percent,
        completed=total > 0 and completed_count == total,
        lessons=views,
    )


__all__ = [
    "CourseProgress",
    "LessonProgress",
    "LessonProgressView",
    "build_course_progress",
    "new_lesson_progress",
]
