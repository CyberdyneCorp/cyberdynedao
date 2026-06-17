"""Achievements endpoint (issue #163).

Earned + in-progress achievements for the authenticated learner, with
progress toward unearned ones. Award rules are deterministic and live in
the domain; this surface just renders the computed statuses.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from cyberdyne_backend.adapters.inbound.api.achievements.schemas import (
    AchievementResponse,
    ProgressResponse,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.application.achievements import GetMyAchievements
from cyberdyne_backend.domain.achievements import AchievementStatus
from cyberdyne_backend.domain.auth_identity import UserPrincipal

public_router = APIRouter(prefix="/api/v1/achievements", tags=["achievements"])


# Dependency stub — overridden in main.py.
async def get_my_achievements_uc() -> GetMyAchievements:  # pragma: no cover - override target
    raise NotImplementedError


def _achievement_response(status: AchievementStatus) -> AchievementResponse:
    d = status.definition
    return AchievementResponse(
        id=d.key,
        key=d.key,
        title=d.title,
        description=d.description,
        icon=d.icon,
        earned_at=status.earned_at,
        progress=ProgressResponse(current=status.current, target=d.target),
    )


@public_router.get(
    "/me",
    response_model=list[AchievementResponse],
    response_model_by_alias=True,
)
async def get_my_achievements(
    use_case: Annotated[GetMyAchievements, Depends(get_my_achievements_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> list[AchievementResponse]:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    statuses = await use_case.execute(principal.user_id)
    return [_achievement_response(s) for s in statuses]
