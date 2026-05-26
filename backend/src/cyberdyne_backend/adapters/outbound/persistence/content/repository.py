"""SQLAlchemy adapter for ``ContentRepository``."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.content.models import (
    ContactMethodRow,
    ContentPageRow,
    ProjectRow,
    ResourceGroupRow,
    ServiceSectionRow,
    TeamMemberRow,
)
from cyberdyne_backend.domain.content import (
    ContactMethod,
    CyberdynePage,
    Project,
    ResourceGroup,
    ResourceLink,
    ServiceBullet,
    ServiceSection,
    TeamMember,
)
from cyberdyne_backend.domain.content.ports import ContentNotFoundError


class SqlAlchemyContentRepository:
    """Reads content from Postgres via an async SQLAlchemy session."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_team(self) -> list[TeamMember]:
        result = await self._session.execute(
            select(TeamMemberRow).order_by(TeamMemberRow.sort_order, TeamMemberRow.id)
        )
        rows = result.scalars().all()
        return [
            TeamMember(
                id=row.id,
                name=row.name,
                title=row.title,
                image_url=row.image_url,
                bio=row.bio,
                tags=tuple(row.tags),
                palette=row.palette,
            )
            for row in rows
        ]

    async def get_page(self, slug: str) -> CyberdynePage:
        result = await self._session.execute(
            select(ContentPageRow).where(ContentPageRow.slug == slug)
        )
        row = result.scalar_one_or_none()
        if row is None:
            raise ContentNotFoundError(f"no content page with slug={slug!r}")
        return CyberdynePage(slug=row.slug, payload=row.payload)

    async def list_projects(self) -> list[Project]:
        result = await self._session.execute(
            select(ProjectRow).order_by(ProjectRow.sort_order, ProjectRow.id)
        )
        rows = result.scalars().all()
        return [
            Project(
                id=row.id,
                name=row.name,
                icon=row.icon,
                description=row.description,
                features=tuple(row.features),
                extra_features=tuple(row.extra_features) if row.extra_features else None,
                palette=row.palette,
                status=row.status,
                full_width=row.full_width,
            )
            for row in rows
        ]

    async def list_service_sections(self) -> list[ServiceSection]:
        result = await self._session.execute(
            select(ServiceSectionRow).order_by(ServiceSectionRow.sort_order, ServiceSectionRow.id)
        )
        rows = result.scalars().all()
        return [
            ServiceSection(
                id=row.id,
                icon=row.icon,
                title=row.title,
                intro=row.intro,
                bullets=tuple(
                    ServiceBullet(title=b["title"], description=b["description"])
                    for b in row.bullets
                ),
                palette=row.palette,
                full_width=row.full_width,
            )
            for row in rows
        ]

    async def list_contact_methods(self) -> list[ContactMethod]:
        result = await self._session.execute(
            select(ContactMethodRow).order_by(ContactMethodRow.sort_order, ContactMethodRow.id)
        )
        rows = result.scalars().all()
        return [
            ContactMethod(
                id=row.id,
                name=row.name,
                icon=row.icon,
                description=row.description,
                action=row.action,
                link=row.link,
                brand_solid=row.brand_solid,
                brand_hover=row.brand_hover,
                brand_rgb=row.brand_rgb,
                tagline=row.tagline,
            )
            for row in rows
        ]

    async def list_resource_groups(self) -> list[ResourceGroup]:
        result = await self._session.execute(
            select(ResourceGroupRow).order_by(ResourceGroupRow.sort_order, ResourceGroupRow.id)
        )
        rows = result.scalars().all()
        return [
            ResourceGroup(
                id=row.id,
                icon=row.icon,
                title=row.title,
                links=tuple(
                    ResourceLink(
                        label=lk["label"],
                        href=lk["href"],
                        disabled=bool(lk.get("disabled", False)),
                    )
                    for lk in row.links
                ),
            )
            for row in rows
        ]
