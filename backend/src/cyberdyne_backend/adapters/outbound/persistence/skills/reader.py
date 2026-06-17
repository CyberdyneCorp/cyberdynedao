"""SQLAlchemy adapter for ``SkillMapReader`` (issue #165).

Read-only aggregation across courses, lessons, lesson-progress and quiz
attempts, grouped by category (= skill). Cross-context table access is
intentional and read-only, like the analytics reporting adapter — this
view owns no tables and never writes. Only published, categorized courses
contribute. The mastery formula itself lives in the domain
(``build_skill_map``); this adapter only supplies raw aggregates.
"""

from __future__ import annotations

from collections import defaultdict
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from cyberdyne_backend.adapters.outbound.persistence.courses.models import (
    CategoryRow,
    CourseRow,
    LessonProgressRow,
    LessonRow,
)
from cyberdyne_backend.adapters.outbound.persistence.quizzes.models import (
    QuizAttemptRow,
    QuizRow,
)
from cyberdyne_backend.domain.skills import SkillInput

_PUBLISHED_STATUS = "published"


class SqlAlchemySkillMapReader:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def skill_inputs_for_user(self, user_id: UUID) -> list[SkillInput]:
        categories = await self._categories()
        course_to_cat, cat_courses, course_slug = await self._published_courses()
        course_lessons = await self._lessons(list(course_to_cat))
        progress = await self._lesson_progress(user_id)
        quiz_scores = await self._quiz_best_scores(user_id)

        inputs: list[SkillInput] = []
        for cat_id, course_ids in cat_courses.items():
            meta = categories.get(cat_id)
            if meta is None:
                continue
            slug, name, domain = meta
            total_lessons = sum(len(course_lessons[c]) for c in course_ids)
            percent_sum = sum(progress.get(lid, 0) for c in course_ids for lid in course_lessons[c])
            inputs.append(
                SkillInput(
                    slug=slug,
                    name=name,
                    domain=domain,
                    course_count=len(course_ids),
                    total_lessons=total_lessons,
                    lesson_percent_sum=percent_sum,
                    quiz_best_scores=tuple(quiz_scores.get(cat_id, [])),
                    suggestion_slug=_pick_suggestion(
                        course_ids, course_lessons, progress, course_slug
                    ),
                )
            )
        return inputs

    async def _categories(self) -> dict[UUID, tuple[str, str, str]]:
        parent = aliased(CategoryRow)
        rows = (
            await self._session.execute(
                select(
                    CategoryRow.id,
                    CategoryRow.slug,
                    CategoryRow.name,
                    parent.name,
                ).join(parent, CategoryRow.parent_id == parent.id, isouter=True)
            )
        ).all()
        # domain = parent category name, or the skill's own name if top-level.
        return {cid: (slug, name, parent_name or name) for cid, slug, name, parent_name in rows}

    async def _published_courses(
        self,
    ) -> tuple[dict[UUID, UUID], dict[UUID, list[UUID]], dict[UUID, str]]:
        rows = (
            await self._session.execute(
                select(CourseRow.id, CourseRow.category_id, CourseRow.slug).where(
                    CourseRow.status == _PUBLISHED_STATUS,
                    CourseRow.category_id.is_not(None),
                )
            )
        ).all()
        course_to_cat: dict[UUID, UUID] = {}
        cat_courses: dict[UUID, list[UUID]] = defaultdict(list)
        course_slug: dict[UUID, str] = {}
        for course_id, category_id, slug in rows:
            course_to_cat[course_id] = category_id
            cat_courses[category_id].append(course_id)
            course_slug[course_id] = slug
        return course_to_cat, cat_courses, course_slug

    async def _lessons(self, course_ids: list[UUID]) -> dict[UUID, list[UUID]]:
        course_lessons: dict[UUID, list[UUID]] = defaultdict(list)
        if not course_ids:
            return course_lessons
        rows = (
            await self._session.execute(
                select(LessonRow.id, LessonRow.course_id).where(LessonRow.course_id.in_(course_ids))
            )
        ).all()
        for lesson_id, course_id in rows:
            course_lessons[course_id].append(lesson_id)
        return course_lessons

    async def _lesson_progress(self, user_id: UUID) -> dict[UUID, int]:
        rows = (
            await self._session.execute(
                select(LessonProgressRow.lesson_id, LessonProgressRow.percent).where(
                    LessonProgressRow.user_id == user_id
                )
            )
        ).all()
        return {lesson_id: percent for lesson_id, percent in rows}

    async def _quiz_best_scores(self, user_id: UUID) -> dict[UUID, list[int]]:
        rows = (
            await self._session.execute(
                select(
                    CourseRow.category_id,
                    QuizAttemptRow.quiz_id,
                    func.max(QuizAttemptRow.score),
                )
                .join(QuizRow, QuizRow.id == QuizAttemptRow.quiz_id)
                .join(LessonRow, LessonRow.id == QuizRow.lesson_id)
                .join(CourseRow, CourseRow.id == LessonRow.course_id)
                .where(
                    QuizAttemptRow.user_id == user_id,
                    CourseRow.status == _PUBLISHED_STATUS,
                    CourseRow.category_id.is_not(None),
                )
                .group_by(CourseRow.category_id, QuizAttemptRow.quiz_id)
            )
        ).all()
        scores: dict[UUID, list[int]] = defaultdict(list)
        for category_id, _quiz_id, best in rows:
            scores[category_id].append(int(best))
        return scores


def _pick_suggestion(
    course_ids: list[UUID],
    course_lessons: dict[UUID, list[UUID]],
    progress: dict[UUID, int],
    course_slug: dict[UUID, str],
) -> str | None:
    """The lowest-completion course that isn't finished — the natural
    next step. Courses with no lessons can't be studied, so they're
    skipped."""
    best_slug: str | None = None
    best_frac: float | None = None
    for course_id in course_ids:
        lessons = course_lessons.get(course_id, [])
        if not lessons:
            continue
        frac = sum(progress.get(lid, 0) for lid in lessons) / (100 * len(lessons))
        if frac >= 1.0:
            continue
        if best_frac is None or frac < best_frac:
            best_frac = frac
            best_slug = course_slug[course_id]
    return best_slug
