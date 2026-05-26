"""Use-case tests for the content context.

The repo port is replaced with a hand-written fake; this verifies the
orchestration without touching SQLAlchemy.
"""

from __future__ import annotations

import pytest

from cyberdyne_backend.application.content.use_cases import (
    CONTACT_META_SLUG,
    CYBERDYNE_PAGE_SLUG,
    SERVICES_META_SLUG,
    GetContactPage,
    GetCyberdynePage,
    GetServicesPage,
    ListProjects,
    ListResourceGroups,
    ListTeam,
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


class FakeContentRepo:
    def __init__(
        self,
        team: list[TeamMember] | None = None,
        pages: dict[str, CyberdynePage] | None = None,
        projects: list[Project] | None = None,
        services: list[ServiceSection] | None = None,
        contacts: list[ContactMethod] | None = None,
        resources: list[ResourceGroup] | None = None,
    ) -> None:
        self._team = team or []
        self._pages = pages or {}
        self._projects = projects or []
        self._services = services or []
        self._contacts = contacts or []
        self._resources = resources or []

    async def list_team(self) -> list[TeamMember]:
        return list(self._team)

    async def get_page(self, slug: str) -> CyberdynePage:
        try:
            return self._pages[slug]
        except KeyError as exc:
            raise ContentNotFoundError(f"missing slug {slug!r}") from exc

    async def list_projects(self) -> list[Project]:
        return list(self._projects)

    async def list_service_sections(self) -> list[ServiceSection]:
        return list(self._services)

    async def list_contact_methods(self) -> list[ContactMethod]:
        return list(self._contacts)

    async def list_resource_groups(self) -> list[ResourceGroup]:
        return list(self._resources)


# ── ListTeam ─────────────────────────────────────────────────────────


async def test_list_team_returns_repo_values() -> None:
    members = [
        TeamMember(
            id="alice",
            name="Alice",
            title="Engineer",
            image_url="/alice.webp",
            bio="builds stuff",
            tags=("python", "rust"),
            palette="blue",
        )
    ]
    uc = ListTeam(repo=FakeContentRepo(team=members))
    assert await uc.execute() == members


async def test_list_team_empty() -> None:
    assert await ListTeam(repo=FakeContentRepo()).execute() == []


# ── GetCyberdynePage ─────────────────────────────────────────────────


async def test_get_cyberdyne_page_returns_seeded_page() -> None:
    page = CyberdynePage(slug=CYBERDYNE_PAGE_SLUG, payload={"hero_tagline": "hi"})
    uc = GetCyberdynePage(repo=FakeContentRepo(pages={CYBERDYNE_PAGE_SLUG: page}))
    assert await uc.execute() is page


async def test_get_cyberdyne_page_raises_when_missing() -> None:
    uc = GetCyberdynePage(repo=FakeContentRepo())
    with pytest.raises(ContentNotFoundError):
        await uc.execute()


# ── ListProjects ─────────────────────────────────────────────────────


async def test_list_projects_returns_repo_values() -> None:
    projects = [
        Project(
            id="p1",
            name="P1",
            icon="🌍",
            description="d",
            features=("a",),
            extra_features=None,
            palette="green",
            status="shipping",
            full_width=False,
        )
    ]
    assert await ListProjects(repo=FakeContentRepo(projects=projects)).execute() == projects


async def test_list_projects_empty() -> None:
    assert await ListProjects(repo=FakeContentRepo()).execute() == []


# ── GetServicesPage ──────────────────────────────────────────────────


async def test_get_services_page_returns_sections_and_meta() -> None:
    sections = [
        ServiceSection(
            id="strategy",
            icon="🎯",
            title="Strategy",
            intro="plan",
            bullets=(ServiceBullet(title="t", description="d"),),
            palette="purple",
            full_width=False,
        )
    ]
    meta = CyberdynePage(
        slug=SERVICES_META_SLUG,
        payload={"hero_subtitle": "hi"},
    )
    uc = GetServicesPage(repo=FakeContentRepo(services=sections, pages={SERVICES_META_SLUG: meta}))
    result_sections, result_meta = await uc.execute()
    assert result_sections == sections
    assert result_meta is meta


async def test_get_services_page_raises_when_meta_missing() -> None:
    uc = GetServicesPage(repo=FakeContentRepo(services=[]))
    with pytest.raises(ContentNotFoundError):
        await uc.execute()


# ── GetContactPage ───────────────────────────────────────────────────


async def test_get_contact_page_returns_methods_and_intro() -> None:
    methods = [
        ContactMethod(
            id="whatsapp",
            name="WhatsApp",
            icon="💬",
            description="d",
            action="Chat",
            link="https://example.com",
            brand_solid="#000",
            brand_hover="#111",
            brand_rgb="0,0,0",
            tagline="t",
        )
    ]
    intro = CyberdynePage(slug=CONTACT_META_SLUG, payload={"headline": "h", "body": "b"})
    uc = GetContactPage(repo=FakeContentRepo(contacts=methods, pages={CONTACT_META_SLUG: intro}))
    result_methods, result_intro = await uc.execute()
    assert result_methods == methods
    assert result_intro is intro


async def test_get_contact_page_raises_when_intro_missing() -> None:
    uc = GetContactPage(repo=FakeContentRepo(contacts=[]))
    with pytest.raises(ContentNotFoundError):
        await uc.execute()


# ── ListResourceGroups ───────────────────────────────────────────────


async def test_list_resource_groups_returns_groups_with_links() -> None:
    groups = [
        ResourceGroup(
            id="docs",
            icon="📚",
            title="Docs",
            links=(ResourceLink(label="L", href="https://example.com"),),
        )
    ]
    assert await ListResourceGroups(repo=FakeContentRepo(resources=groups)).execute() == groups


async def test_list_resource_groups_empty() -> None:
    assert await ListResourceGroups(repo=FakeContentRepo()).execute() == []
