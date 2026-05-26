"""Content endpoints.

The router itself is thin: it depends on use cases via FastAPI's DI,
serialises domain objects through pydantic response models (camelCase
on the wire), and lets the upstream container wire everything together.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from cyberdyne_backend.adapters.inbound.api.content.schemas import (
    ContactMethodResponse,
    ContactPageResponse,
    CyberdynePageResponse,
    ProjectResponse,
    ResourceGroupResponse,
    ResourceLinkResponse,
    ServiceBulletResponse,
    ServiceSectionResponse,
    ServicesPageResponse,
    TeamMemberResponse,
)
from cyberdyne_backend.application.content.use_cases import (
    GetContactPage,
    GetCyberdynePage,
    GetServicesPage,
    ListProjects,
    ListResourceGroups,
    ListTeam,
)
from cyberdyne_backend.domain.content.ports import ContentNotFoundError

router = APIRouter(prefix="/api/v1/content", tags=["content"])


# Dependency stubs — overridden in main.py to wire real repositories.
async def get_list_team_uc() -> ListTeam:  # pragma: no cover - override target
    raise NotImplementedError("ListTeam dependency not wired")


async def get_cyberdyne_page_uc() -> GetCyberdynePage:  # pragma: no cover - override target
    raise NotImplementedError("GetCyberdynePage dependency not wired")


async def get_list_projects_uc() -> ListProjects:  # pragma: no cover - override target
    raise NotImplementedError("ListProjects dependency not wired")


async def get_services_page_uc() -> GetServicesPage:  # pragma: no cover - override target
    raise NotImplementedError("GetServicesPage dependency not wired")


async def get_contact_page_uc() -> GetContactPage:  # pragma: no cover - override target
    raise NotImplementedError("GetContactPage dependency not wired")


async def get_list_resources_uc() -> ListResourceGroups:  # pragma: no cover - override target
    raise NotImplementedError("ListResourceGroups dependency not wired")


# ── Team ─────────────────────────────────────────────────────────────


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


# ── Cyberdyne about page ─────────────────────────────────────────────


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
    # Payload is dict-shaped at the domain level; pydantic validates
    # the actual shape at the boundary. Mis-seeded data surfaces as a
    # 500 with a precise error, which is the right behaviour.
    return CyberdynePageResponse.model_validate(page.payload)


# ── Projects ─────────────────────────────────────────────────────────


@router.get(
    "/projects",
    response_model=list[ProjectResponse],
    response_model_by_alias=True,
)
async def list_projects(
    use_case: Annotated[ListProjects, Depends(get_list_projects_uc)],
) -> list[ProjectResponse]:
    projects = await use_case.execute()
    return [
        ProjectResponse(
            id=p.id,
            name=p.name,
            icon=p.icon,
            description=p.description,
            features=list(p.features),
            extra_features=list(p.extra_features) if p.extra_features is not None else None,
            palette=p.palette,
            status=p.status,
            full_width=p.full_width,
        )
        for p in projects
    ]


# ── Services ─────────────────────────────────────────────────────────


@router.get(
    "/services",
    response_model=ServicesPageResponse,
    response_model_by_alias=True,
)
async def get_services_page(
    use_case: Annotated[GetServicesPage, Depends(get_services_page_uc)],
) -> ServicesPageResponse:
    try:
        sections, meta = await use_case.execute()
    except ContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail="services-meta not seeded") from exc

    section_payload = [
        ServiceSectionResponse(
            id=s.id,
            icon=s.icon,
            title=s.title,
            intro=s.intro,
            bullets=[
                ServiceBulletResponse(title=b.title, description=b.description) for b in s.bullets
            ],
            palette=s.palette,
            full_width=s.full_width,
        )
        for s in sections
    ]
    return ServicesPageResponse.model_validate(
        {**meta.payload, "sections": [r.model_dump() for r in section_payload]}
    )


# ── Contact ──────────────────────────────────────────────────────────


@router.get(
    "/contact",
    response_model=ContactPageResponse,
    response_model_by_alias=True,
)
async def get_contact_page(
    use_case: Annotated[GetContactPage, Depends(get_contact_page_uc)],
) -> ContactPageResponse:
    try:
        methods, intro = await use_case.execute()
    except ContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail="contact-meta not seeded") from exc

    method_payload = [
        ContactMethodResponse(
            id=m.id,
            name=m.name,
            icon=m.icon,
            description=m.description,
            action=m.action,
            link=m.link,
            brand_solid=m.brand_solid,
            brand_hover=m.brand_hover,
            brand_rgb=m.brand_rgb,
            tagline=m.tagline,
        )
        for m in methods
    ]
    return ContactPageResponse.model_validate(
        {
            "methods": [r.model_dump() for r in method_payload],
            "intro": intro.payload,
        }
    )


# ── Resources (Learn view footer) ────────────────────────────────────


@router.get(
    "/resources",
    response_model=list[ResourceGroupResponse],
    response_model_by_alias=True,
)
async def list_resources(
    use_case: Annotated[ListResourceGroups, Depends(get_list_resources_uc)],
) -> list[ResourceGroupResponse]:
    groups = await use_case.execute()
    return [
        ResourceGroupResponse(
            id=g.id,
            icon=g.icon,
            title=g.title,
            links=[
                ResourceLinkResponse(label=lk.label, href=lk.href, disabled=lk.disabled)
                for lk in g.links
            ],
        )
        for g in groups
    ]
