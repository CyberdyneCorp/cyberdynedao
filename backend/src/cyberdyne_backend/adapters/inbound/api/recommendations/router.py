"""Course-recommendations endpoint — LLM-personalized next steps for a
signed-in learner. Read-only and self-scoped (always the caller)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from cyberdyne_backend.adapters.inbound.api.recommendations.schemas import (
    CourseRecommendationResponse,
    RecommendationsResponse,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.application.recommendations import (
    LearningRecommendations,
    RecommendCourses,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal

public_router = APIRouter(prefix="/api/v1/recommendations", tags=["recommendations"])


# Dependency stub — overridden in main.py.
async def get_recommend_courses_uc() -> RecommendCourses:  # pragma: no cover - override target
    raise NotImplementedError


def _response(recs: LearningRecommendations) -> RecommendationsResponse:
    return RecommendationsResponse(
        summary=recs.summary,
        courses=[
            CourseRecommendationResponse(slug=c.slug, title=c.title, level=c.level, reason=c.reason)
            for c in recs.courses
        ],
    )


@public_router.get(
    "/me",
    response_model=RecommendationsResponse,
    response_model_by_alias=True,
)
async def get_my_recommendations(
    use_case: Annotated[RecommendCourses, Depends(get_recommend_courses_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> RecommendationsResponse:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    recs = await use_case.execute(user_id=principal.user_id)
    return _response(recs)


__all__ = ["public_router"]
