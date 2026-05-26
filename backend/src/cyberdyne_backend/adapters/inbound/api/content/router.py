"""Content endpoints — ``GET /api/v1/content/team`` and ``…/cyberdyne``.

The router itself is thin: it depends on use cases via FastAPI's DI,
serialises domain objects through pydantic response models, and lets
the upstream container wire everything together.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from cyberdyne_backend.adapters.inbound.api.content.schemas import (
    CyberdynePageResponse,
    TeamMemberResponse,
)
from cyberdyne_backend.application.content.use_cases import (
    GetCyberdynePage,
    ListTeam,
)
from cyberdyne_backend.domain.content.ports import ContentNotFoundError

router = APIRouter(prefix="/api/v1/content", tags=["content"])


# These FastAPI dependencies are overridden in main.py to wire the
# real repository per-request. Tests override them too.
async def get_list_team_uc() -> ListTeam:  # pragma: no cover - override target
    raise NotImplementedError("ListTeam dependency not wired")


async def get_cyberdyne_page_uc() -> GetCyberdynePage:  # pragma: no cover - override target
    raise NotImplementedError("GetCyberdynePage dependency not wired")


@router.get(
    "/team",
    response_model=list[TeamMemberResponse],
    response_model_by_alias=True,
)
async def list_team(
    use_case: Annotated[ListTeam, Depends(get_list_team_uc)],
) -> list[TeamMemberResponse]:
    members = await use_case.execute()
    return [
        TeamMemberResponse(
            id=m.id,
            name=m.name,
            title=m.title,
            image_url=m.image_url,
            bio=m.bio,
            tags=list(m.tags),
            palette=m.palette,
        )
        for m in members
    ]


@router.get(
    "/cyberdyne",
    response_model=CyberdynePageResponse,
    response_model_by_alias=True,
)
async def get_cyberdyne_page(
    use_case: Annotated[GetCyberdynePage, Depends(get_cyberdyne_page_uc)],
) -> CyberdynePageResponse:
    try:
        page = await use_case.execute()
    except ContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail="cyberdyne page not seeded") from exc
    # The payload is dict-shaped at the domain level; pydantic validates
    # the actual shape here at the boundary. Mis-seeded data surfaces as
    # a 500 with a precise error, which is the right behaviour.
    return CyberdynePageResponse.model_validate(page.payload)
