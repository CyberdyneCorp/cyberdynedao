"""Use-case tests for the content context.

The repo port is replaced with a hand-written fake; this verifies the
orchestration without touching SQLAlchemy.
"""

from __future__ import annotations

import pytest

from cyberdyne_backend.application.content.use_cases import (
    CYBERDYNE_PAGE_SLUG,
    GetCyberdynePage,
    ListTeam,
)
from cyberdyne_backend.domain.content import CyberdynePage, TeamMember
from cyberdyne_backend.domain.content.ports import ContentNotFoundError


class FakeContentRepo:
    def __init__(
        self,
        team: list[TeamMember] | None = None,
        pages: dict[str, CyberdynePage] | None = None,
    ) -> None:
        self._team = team or []
        self._pages = pages or {}

    async def list_team(self) -> list[TeamMember]:
        return list(self._team)

    async def get_page(self, slug: str) -> CyberdynePage:
        try:
            return self._pages[slug]
        except KeyError as exc:
            raise ContentNotFoundError(f"missing slug {slug!r}") from exc


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
    result = await uc.execute()
    assert result == members


async def test_list_team_empty() -> None:
    uc = ListTeam(repo=FakeContentRepo())
    assert await uc.execute() == []


# ── GetCyberdynePage ─────────────────────────────────────────────────


async def test_get_cyberdyne_page_returns_seeded_page() -> None:
    page = CyberdynePage(slug=CYBERDYNE_PAGE_SLUG, payload={"hero_tagline": "hi"})
    uc = GetCyberdynePage(repo=FakeContentRepo(pages={CYBERDYNE_PAGE_SLUG: page}))
    assert await uc.execute() is page


async def test_get_cyberdyne_page_raises_when_missing() -> None:
    uc = GetCyberdynePage(repo=FakeContentRepo())
    with pytest.raises(ContentNotFoundError):
        await uc.execute()
