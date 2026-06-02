"""SQLAlchemy adapter for ``AnalyticsRepository``.

Read-only aggregation across the learning, courses, and quiz tables.
Cross-context table access is intentional — analytics is a reporting
view that spans bounded contexts; it owns no tables and never writes.
Booleans are aggregated via ``CAST(... AS INTEGER)`` so the same queries
run on both SQLite (tests) and Postgres (prod), where ``MAX(boolean)``
is not valid.
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import Integer, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.courses.models import (
    CourseRow,
    LessonProgressRow,
    LessonRow,
)
from cyberdyne_backend.adapters.outbound.persistence.learning.models import (
    CertificateRow,
    EnrollmentRow,
    LearningModuleRow,
    LearningPathRow,
    ModuleProgressRow,
)
from cyberdyne_backend.adapters.outbound.persistence.quizzes.models import QuizAttemptRow
from cyberdyne_backend.domain.analytics import LearnerCounts, PlatformCounts


class SqlAlchemyAnalyticsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def learner_counts(self, user_id: UUID) -> LearnerCounts:
        session = self._session

        # Enrollments by status.
        enr_rows = (
            await session.execute(
                select(EnrollmentRow.status, func.count())
                .where(EnrollmentRow.user_id == user_id)
                .group_by(EnrollmentRow.status)
            )
        ).all()
        by_status = {status: count for status, count in enr_rows}
        enrolled = sum(by_status.values())
        completed_paths = by_status.get("completed", 0)
        active_paths = by_status.get("active", 0)

        # Module progress.
        prog = (
            await session.execute(
                select(
                    func.count(),
                    func.coalesce(func.sum(ModuleProgressRow.percent), 0),
                    func.coalesce(
                        func.sum(cast(ModuleProgressRow.completed_at.is_not(None), Integer)),
                        0,
                    ),
                    func.coalesce(
                        func.sum(
                            cast(
                                (ModuleProgressRow.percent > 0) & (ModuleProgressRow.percent < 100),
                                Integer,
                            )
                        ),
                        0,
                    ),
                ).where(ModuleProgressRow.user_id == user_id)
            )
        ).one()
        module_rows, percent_sum, completed_modules, in_progress = prog

        # Best score per attempted quiz + pass flag.
        quiz_rows = (
            await session.execute(
                select(
                    QuizAttemptRow.quiz_id,
                    func.max(QuizAttemptRow.score),
                    func.max(cast(QuizAttemptRow.passed, Integer)),
                )
                .where(QuizAttemptRow.user_id == user_id)
                .group_by(QuizAttemptRow.quiz_id)
            )
        ).all()
        best_quiz_scores = [int(score) for _, score, _ in quiz_rows]
        quizzes_passed = sum(1 for _, _, passed in quiz_rows if passed)

        total_attempts = (
            await session.execute(select(func.count()).where(QuizAttemptRow.user_id == user_id))
        ).scalar_one()

        certificates = (
            await session.execute(select(func.count()).where(CertificateRow.user_id == user_id))
        ).scalar_one()

        # Course standing from per-lesson progress: a course is complete
        # iff the learner has completed every one of its lessons. Compare
        # total lessons per course against the learner's completed count.
        total_lessons_by_course: dict[UUID, int] = {
            course_id: int(count)
            for course_id, count in (
                await session.execute(
                    select(LessonRow.course_id, func.count()).group_by(LessonRow.course_id)
                )
            ).all()
        }
        user_course_rows = (
            await session.execute(
                select(
                    LessonProgressRow.course_id,
                    func.count(),
                    func.coalesce(
                        func.sum(cast(LessonProgressRow.completed_at.is_not(None), Integer)),
                        0,
                    ),
                )
                .where(LessonProgressRow.user_id == user_id)
                .group_by(LessonProgressRow.course_id)
            )
        ).all()
        completed_courses = 0
        in_progress_courses = 0
        for course_id, _touched, done in user_course_rows:
            total = int(total_lessons_by_course.get(course_id, 0))
            if total > 0 and int(done) >= total:
                completed_courses += 1
            else:
                in_progress_courses += 1

        return LearnerCounts(
            enrolled_paths=enrolled,
            completed_paths=completed_paths,
            active_paths=active_paths,
            completed_modules=int(completed_modules),
            in_progress_modules=int(in_progress),
            module_percent_sum=int(percent_sum),
            module_rows=int(module_rows),
            certificates=int(certificates),
            best_quiz_scores=best_quiz_scores,
            quizzes_passed=quizzes_passed,
            total_quiz_attempts=int(total_attempts),
            completed_courses=completed_courses,
            in_progress_courses=in_progress_courses,
        )

    async def platform_counts(self) -> PlatformCounts:
        session = self._session

        total_learners = (
            await session.execute(select(func.count(func.distinct(EnrollmentRow.user_id))))
        ).scalar_one()
        total_enrollments = (
            await session.execute(select(func.count()).select_from(EnrollmentRow))
        ).scalar_one()
        completed_enrollments = (
            await session.execute(select(func.count()).where(EnrollmentRow.status == "completed"))
        ).scalar_one()

        course_rows = (
            await session.execute(select(CourseRow.status, func.count()).group_by(CourseRow.status))
        ).all()
        by_status = {status: count for status, count in course_rows}

        total_modules = (
            await session.execute(select(func.count()).select_from(LearningModuleRow))
        ).scalar_one()
        total_paths = (
            await session.execute(select(func.count()).select_from(LearningPathRow))
        ).scalar_one()
        total_certificates = (
            await session.execute(select(func.count()).select_from(CertificateRow))
        ).scalar_one()

        quiz_agg = (
            await session.execute(
                select(
                    func.count(),
                    func.coalesce(func.sum(cast(QuizAttemptRow.passed, Integer)), 0),
                    func.coalesce(func.sum(QuizAttemptRow.score), 0),
                )
            )
        ).one()
        total_attempts, passed_attempts, score_sum = quiz_agg

        return PlatformCounts(
            total_learners=int(total_learners),
            total_enrollments=int(total_enrollments),
            completed_enrollments=int(completed_enrollments),
            published_courses=int(by_status.get("published", 0)),
            draft_courses=int(by_status.get("draft", 0)),
            total_modules=int(total_modules),
            total_paths=int(total_paths),
            total_certificates=int(total_certificates),
            total_quiz_attempts=int(total_attempts),
            passed_quiz_attempts=int(passed_attempts),
            quiz_score_sum=int(score_sum),
        )
