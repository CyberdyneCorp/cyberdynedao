"""Application use cases for the content context.

Use cases are stateless; they take a repository in the constructor and
expose an async ``execute`` method. The constructor injection makes
wiring explicit (the Container in infrastructure builds them per
request scope).
"""

from __future__ import annotations

from dataclasses import dataclass

from cyberdyne_backend.domain.content import (
    ContactMethod,
    ContentRepository,
    CyberdynePage,
    Project,
    ResourceGroup,
    ServiceSection,
    TeamMember,
)

# Slugs for page-level content stored in the content_pages table.
# Hardcoded today; admin authoring (later phase) can parameterise.
CYBERDYNE_PAGE_SLUG = "cyberdyne"
SERVICES_META_SLUG = "services-meta"
CONTACT_META_SLUG = "contact-meta"


# ── Phase 1 ──────────────────────────────────────────────────────────


@dataclass(slots=True)
class ListTeam:
    repo: ContentRepository

    async def execute(self) -> list[TeamMember]:
        return await self.repo.list_team()


@dataclass(slots=True)
class GetCyberdynePage:
    repo: ContentRepository

    async def execute(self) -> CyberdynePage:
        return await self.repo.get_page(CYBERDYNE_PAGE_SLUG)


# ── Phase 2 ──────────────────────────────────────────────────────────


@dataclass(slots=True)
class ListProjects:
    repo: ContentRepository

    async def execute(self) -> list[Project]:
        return await self.repo.list_projects()


@dataclass(slots=True)
class GetServicesPage:
    """Returns the list of service sections plus the page-level meta
    (workflow steps, why-Cyberdyne points, CTA copy). The two get
    bundled in one response so the view renders in one round-trip."""

    repo: ContentRepository

    async def execute(self) -> tuple[list[ServiceSection], CyberdynePage]:
        sections = await self.repo.list_service_sections()
        meta = await self.repo.get_page(SERVICES_META_SLUG)
        return sections, meta


@dataclass(slots=True)
class GetContactPage:
    """List of contact channels + the page-level intro copy."""

    repo: ContentRepository

    async def execute(self) -> tuple[list[ContactMethod], CyberdynePage]:
        methods = await self.repo.list_contact_methods()
        intro = await self.repo.get_page(CONTACT_META_SLUG)
        return methods, intro


@dataclass(slots=True)
class ListResourceGroups:
    repo: ContentRepository

    async def execute(self) -> list[ResourceGroup]:
        return await self.repo.list_resource_groups()
