"""Analytics endpoints — learner dashboard + admin overview."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from cyberdyne_backend.adapters.inbound.api.analytics.schemas import (
    AdminOverviewResponse,
    LearnerDashboardResponse,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import (
    require_editor,
    require_principal,
)
from cyberdyne_backend.application.analytics import (
    GetAdminOverview,
    GetLearnerDashboard,
)
from cyberdyne_backend.domain.analytics import AdminOverview, LearnerDashboard
from cyberdyne_backend.domain.auth_identity import UserPrincipal

public_router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])
admin_router = APIRouter(prefix="/api/v1/admin/analytics", tags=["analytics-admin"])


# Dependency stubs — overridden in main.py.
async def get_learner_dashboard_uc() -> GetLearnerDashboard:  # pragma: no cover - override target
    raise NotImplementedError


async def get_admin_overview_uc() -> GetAdminOverview:  # pragma: no cover - override target
    raise NotImplementedError


def _learner_response(d: LearnerDashboard) -> LearnerDashboardResponse:
    return LearnerDashboardResponse(
        enrolled_paths=d.enrolled_paths,
        completed_paths=d.completed_paths,
        active_paths=d.active_paths,
        completed_modules=d.completed_modules,
        in_progress_modules=d.in_progress_modules,
        avg_module_percent=d.avg_module_percent,
        quizzes_attempted=d.quizzes_attempted,
        quizzes_passed=d.quizzes_passed,
        quiz_pass_rate=d.quiz_pass_rate,
        avg_quiz_score=d.avg_quiz_score,
        total_quiz_attempts=d.total_quiz_attempts,
        certificates=d.certificates,
        completed_courses=d.completed_courses,
        in_progress_courses=d.in_progress_courses,
    )


def _admin_response(o: AdminOverview) -> AdminOverviewResponse:
    return AdminOverviewResponse(
        total_learners=o.total_learners,
        total_enrollments=o.total_enrollments,
        completed_enrollments=o.completed_enrollments,
        enrollment_completion_rate=o.enrollment_completion_rate,
        published_courses=o.published_courses,
        draft_courses=o.draft_courses,
        total_modules=o.total_modules,
        total_paths=o.total_paths,
        total_certificates=o.total_certificates,
        total_quiz_attempts=o.total_quiz_attempts,
        quiz_pass_rate=o.quiz_pass_rate,
        avg_quiz_score=o.avg_quiz_score,
    )


@public_router.get(
    "/me",
    response_model=LearnerDashboardResponse,
    response_model_by_alias=True,
)
async def get_my_dashboard(
    use_case: Annotated[GetLearnerDashboard, Depends(get_learner_dashboard_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> LearnerDashboardResponse:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    dashboard = await use_case.execute(principal.user_id)
    return _learner_response(dashboard)


@admin_router.get(
    "/overview",
    response_model=AdminOverviewResponse,
    response_model_by_alias=True,
)
async def get_admin_overview(
    use_case: Annotated[GetAdminOverview, Depends(get_admin_overview_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> AdminOverviewResponse:
    overview = await use_case.execute()
    return _admin_response(overview)


__all__ = ["admin_router", "public_router"]
