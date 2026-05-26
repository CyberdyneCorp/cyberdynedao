"""Application use cases for the content context.

Use cases are stateless; they take a repository in the constructor and
expose an async ``execute`` method. The constructor injection makes
wiring explicit (the Container in infrastructure builds them per
request scope).
"""

from __future__ import annotations

from dataclasses import dataclass

from cyberdyne_backend.domain.content import (
    ContentRepository,
    CyberdynePage,
    TeamMember,
)

# The slug we use for the about-us page. Hardcoded today; admin
# authoring (Phase 3) could parameterise it but the frontend only
# consumes the cyberdyne page in Phase 1.
CYBERDYNE_PAGE_SLUG = "cyberdyne"


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
