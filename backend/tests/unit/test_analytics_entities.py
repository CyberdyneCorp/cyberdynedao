"""Domain tests for analytics aggregation logic."""

from __future__ import annotations

from cyberdyne_backend.domain.analytics import (
    LearnerCounts,
    PlatformCounts,
    build_admin_overview,
    build_learner_dashboard,
)


class TestLearnerDashboard:
    def test_computes_averages_and_rates(self) -> None:
        counts = LearnerCounts(
            enrolled_paths=3,
            completed_paths=1,
            active_paths=2,
            completed_modules=4,
            in_progress_modules=2,
            module_percent_sum=300,
            module_rows=6,
            certificates=1,
            best_quiz_scores=[100, 50, 60, 90],
            quizzes_passed=3,
            total_quiz_attempts=7,
            completed_courses=2,
            in_progress_courses=1,
        )
        d = build_learner_dashboard(counts)
        assert d.avg_module_percent == 50.0  # 300/6
        assert d.quizzes_attempted == 4
        assert d.quiz_pass_rate == 75.0  # 3/4
        assert d.avg_quiz_score == 75.0  # mean(100,50,60,90)
        assert d.total_quiz_attempts == 7
        assert d.completed_courses == 2
        assert d.in_progress_courses == 1

    def test_empty_learner_is_all_zero(self) -> None:
        d = build_learner_dashboard(LearnerCounts())
        assert d.avg_module_percent == 0.0
        assert d.quiz_pass_rate == 0.0
        assert d.avg_quiz_score == 0.0
        assert d.quizzes_attempted == 0
        assert d.completed_courses == 0
        assert d.in_progress_courses == 0

    def test_no_quizzes_no_divide_by_zero(self) -> None:
        d = build_learner_dashboard(LearnerCounts(module_rows=2, module_percent_sum=150))
        assert d.avg_module_percent == 75.0
        assert d.avg_quiz_score == 0.0
        assert d.quiz_pass_rate == 0.0


class TestAdminOverview:
    def test_computes_rates(self) -> None:
        counts = PlatformCounts(
            total_learners=10,
            total_enrollments=20,
            completed_enrollments=5,
            published_courses=6,
            draft_courses=2,
            total_modules=12,
            total_paths=5,
            total_certificates=3,
            total_quiz_attempts=40,
            passed_quiz_attempts=30,
            quiz_score_sum=2800,
        )
        o = build_admin_overview(counts)
        assert o.enrollment_completion_rate == 25.0  # 5/20
        assert o.quiz_pass_rate == 75.0  # 30/40
        assert o.avg_quiz_score == 70.0  # 2800/40
        assert o.published_courses == 6

    def test_empty_platform_no_divide_by_zero(self) -> None:
        o = build_admin_overview(PlatformCounts())
        assert o.enrollment_completion_rate == 0.0
        assert o.quiz_pass_rate == 0.0
        assert o.avg_quiz_score == 0.0

    def test_rate_rounds_to_one_decimal(self) -> None:
        o = build_admin_overview(PlatformCounts(total_enrollments=3, completed_enrollments=1))
        assert o.enrollment_completion_rate == 33.3  # 1/3
