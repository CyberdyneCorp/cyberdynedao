"""SQLAlchemy adapter for ``AchievementMetricsReader`` (issue #163).

Read-only counts across the courses/quizzes/learning contexts that the
deterministic award rules consume. Cross-context table access is
intentional and read-only, like the analytics reporting adapter — this
view owns no tables and never writes.
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.courses.models import (
    CourseCertificateRow,
)
from cyberdyne_backend.adapters.outbound.persistence.learning.models import (
    CertificateRow,
    ModuleProgressRow,
)
from cyberdyne_backend.adapters.outbound.persistence.quizzes.models import (
    QuizAttemptRow,
)
from cyberdyne_backend.domain.achievements import LearnerMetrics


class SqlAlchemyAchievementMetricsReader:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def compute(self, user_id: UUID) -> LearnerMetrics:
        return LearnerMetrics(
            courses_completed=await self._scalar(
                select(func.count())
                .select_from(CourseCertificateRow)
                .where(CourseCertificateRow.user_id == user_id)
            ),
            quizzes_passed=await self._scalar(
                select(func.count(func.distinct(QuizAttemptRow.quiz_id))).where(
                    QuizAttemptRow.user_id == user_id,
                    QuizAttemptRow.passed.is_(True),
                )
            ),
            perfect_quizzes=await self._scalar(
                select(func.count(func.distinct(QuizAttemptRow.quiz_id))).where(
                    QuizAttemptRow.user_id == user_id,
                    QuizAttemptRow.score == 100,
                )
            ),
            certificates_earned=(
                await self._scalar(
                    select(func.count())
                    .select_from(CourseCertificateRow)
                    .where(CourseCertificateRow.user_id == user_id)
                )
                + await self._scalar(
                    select(func.count())
                    .select_from(CertificateRow)
                    .where(CertificateRow.user_id == user_id)
                )
            ),
            modules_completed=await self._scalar(
                select(func.count())
                .select_from(ModuleProgressRow)
                .where(
                    ModuleProgressRow.user_id == user_id,
                    ModuleProgressRow.percent == 100,
                )
            ),
        )

    async def _scalar(self, stmt: Select[tuple[int]]) -> int:
        return int((await self._session.execute(stmt)).scalar_one() or 0)
