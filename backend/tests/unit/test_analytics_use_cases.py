"""Use-case tests for the analytics context, with a fake repo."""

from __future__ import annotations

import uuid
from uuid import UUID

from cyberdyne_backend.application.analytics import GetAdminOverview, GetLearnerDashboard
from cyberdyne_backend.domain.analytics import (
    AnalyticsRepository,
    LearnerCounts,
    PlatformCounts,
)


class FakeAnalyticsRepo:
    def __init__(
        self, learner: LearnerCounts | None = None, platform: PlatformCounts | None = None
    ) -> None:
        self._learner = learner or LearnerCounts()
        self._platform = platform or PlatformCounts()

    async def learner_counts(self, user_id: UUID) -> LearnerCounts:
        return self._learner

    async def platform_counts(self) -> PlatformCounts:
        return self._platform


def test_fake_matches_port() -> None:
    assert isinstance(FakeAnalyticsRepo(), AnalyticsRepository)


class TestGetLearnerDashboard:
    async def test_builds_dashboard(self) -> None:
        repo = FakeAnalyticsRepo(
            learner=LearnerCounts(enrolled_paths=2, best_quiz_scores=[80, 100], quizzes_passed=2)
        )
        d = await GetLearnerDashboard(repo=repo).execute(uuid.uuid4())
        assert d.enrolled_paths == 2
        assert d.avg_quiz_score == 90.0
        assert d.quiz_pass_rate == 100.0


class TestGetAdminOverview:
    async def test_builds_overview(self) -> None:
        repo = FakeAnalyticsRepo(
            platform=PlatformCounts(total_learners=5, published_courses=3, total_enrollments=10)
        )
        o = await GetAdminOverview(repo=repo).execute()
        assert o.total_learners == 5
        assert o.published_courses == 3
