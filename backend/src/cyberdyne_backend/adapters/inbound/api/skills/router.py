"""Skill Map endpoint (issue #165).

Per-domain skill mastery + weak areas for the authenticated learner,
derived server-side from quiz performance + lesson/course completion.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from cyberdyne_backend.adapters.inbound.api.skills.schemas import (
    SkillMapResponse,
    SkillMasteryResponse,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.application.skills import GetSkillMap
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.skills import SkillMap

public_router = APIRouter(prefix="/api/v1/skills", tags=["skills"])


# Dependency stub — overridden in main.py.
async def get_skill_map_uc() -> GetSkillMap:  # pragma: no cover - override target
    raise NotImplementedError


def _skill_map_response(skill_map: SkillMap) -> SkillMapResponse:
    return SkillMapResponse(
        skills=[
            SkillMasteryResponse(
                id=s.id,
                name=s.name,
                domain=s.domain,
                mastery=s.mastery,
                course_count=s.course_count,
                weak=s.weak,
            )
            for s in skill_map.skills
        ],
        weak_areas=skill_map.weak_areas,
        suggestions=skill_map.suggestions,
    )


@public_router.get(
    "/me",
    response_model=SkillMapResponse,
    response_model_by_alias=True,
)
async def get_my_skill_map(
    use_case: Annotated[GetSkillMap, Depends(get_skill_map_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> SkillMapResponse:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    skill_map = await use_case.execute(principal.user_id)
    return _skill_map_response(skill_map)
