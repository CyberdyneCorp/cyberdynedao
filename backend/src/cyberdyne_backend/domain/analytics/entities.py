"""Analytics domain — value objects + pure aggregation logic.

The repository returns *raw counts* (cheap SQL aggregates); the derived
figures — averages, completion/pass rates — are computed here so the
arithmetic is pure-domain and unit-tested, and the adapter stays a thin
query layer. Rates are returned as percentages rounded to one decimal,
with zero-denominator guards.
"""

from __future__ import annotations

from dataclasses import dataclass, field


def _rate(numerator: int, denominator: int) -> float:
    """Percentage (0-100, 1 dp). Zero denominator -> 0.0."""
    if denominator <= 0:
        return 0.0
    return round(numerator / denominator * 100, 1)


def _mean(values: list[int]) -> float:
    if not values:
        return 0.0
    return round(sum(values) / len(values), 1)


# ── Learner dashboard ────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class LearnerCounts:
    """Raw per-user aggregates straight from the repository."""

    enrolled_paths: int = 0
    completed_paths: int = 0
    active_paths: int = 0
    completed_modules: int = 0
    in_progress_modules: int = 0
    module_percent_sum: int = 0
    module_rows: int = 0
    certificates: int = 0
    # Best (max) score per quiz the user has attempted.
    best_quiz_scores: list[int] = field(default_factory=list)
    quizzes_passed: int = 0
    total_quiz_attempts: int = 0
    # Course standing, derived from per-lesson progress: a course is
    # complete iff every one of its lessons is.
    completed_courses: int = 0
    in_progress_courses: int = 0


@dataclass(frozen=True, slots=True)
class LearnerDashboard:
    enrolled_paths: int
    completed_paths: int
    active_paths: int
    completed_modules: int
    in_progress_modules: int
    avg_module_percent: float
    quizzes_attempted: int
    quizzes_passed: int
    quiz_pass_rate: float
    avg_quiz_score: float
    total_quiz_attempts: int
    certificates: int
    completed_courses: int
    in_progress_courses: int


def build_learner_dashboard(counts: LearnerCounts) -> LearnerDashboard:
    quizzes_attempted = len(counts.best_quiz_scores)
    return LearnerDashboard(
        enrolled_paths=counts.enrolled_paths,
        completed_paths=counts.completed_paths,
        active_paths=counts.active_paths,
        completed_modules=counts.completed_modules,
        in_progress_modules=counts.in_progress_modules,
        avg_module_percent=(
            round(counts.module_percent_sum / counts.module_rows, 1) if counts.module_rows else 0.0
        ),
        quizzes_attempted=quizzes_attempted,
        quizzes_passed=counts.quizzes_passed,
        quiz_pass_rate=_rate(counts.quizzes_passed, quizzes_attempted),
        avg_quiz_score=_mean(counts.best_quiz_scores),
        total_quiz_attempts=counts.total_quiz_attempts,
        certificates=counts.certificates,
        completed_courses=counts.completed_courses,
        in_progress_courses=counts.in_progress_courses,
    )


# ── Admin overview ───────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class PlatformCounts:
    total_learners: int = 0
    total_enrollments: int = 0
    completed_enrollments: int = 0
    published_courses: int = 0
    draft_courses: int = 0
    total_modules: int = 0
    total_paths: int = 0
    total_certificates: int = 0
    total_quiz_attempts: int = 0
    passed_quiz_attempts: int = 0
    quiz_score_sum: int = 0


@dataclass(frozen=True, slots=True)
class AdminOverview:
    total_learners: int
    total_enrollments: int
    completed_enrollments: int
    enrollment_completion_rate: float
    published_courses: int
    draft_courses: int
    total_modules: int
    total_paths: int
    total_certificates: int
    total_quiz_attempts: int
    quiz_pass_rate: float
    avg_quiz_score: float


def build_admin_overview(counts: PlatformCounts) -> AdminOverview:
    return AdminOverview(
        total_learners=counts.total_learners,
        total_enrollments=counts.total_enrollments,
        completed_enrollments=counts.completed_enrollments,
        enrollment_completion_rate=_rate(counts.completed_enrollments, counts.total_enrollments),
        published_courses=counts.published_courses,
        draft_courses=counts.draft_courses,
        total_modules=counts.total_modules,
        total_paths=counts.total_paths,
        total_certificates=counts.total_certificates,
        total_quiz_attempts=counts.total_quiz_attempts,
        quiz_pass_rate=_rate(counts.passed_quiz_attempts, counts.total_quiz_attempts),
        avg_quiz_score=(
            round(counts.quiz_score_sum / counts.total_quiz_attempts, 1)
            if counts.total_quiz_attempts
            else 0.0
        ),
    )
