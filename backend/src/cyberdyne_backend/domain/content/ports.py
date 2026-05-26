"""Ports for the content context.

Concrete impl lives in
``adapters/outbound/persistence/content/repository.py``. A FakeRepo for
unit tests lives next to the application use cases.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from cyberdyne_backend.domain.content.entities import (
    ContactMethod,
    CyberdynePage,
    Project,
    ResourceGroup,
    ServiceSection,
    TeamMember,
)


class ContentNotFoundError(LookupError):
    """No content with the requested slug / id exists."""


@runtime_checkable
class ContentRepository(Protocol):
    async def list_team(self) -> list[TeamMember]:
        """Return all team members, deterministically ordered."""
        ...

    async def get_page(self, slug: str) -> CyberdynePage:
        """Return the page with this slug. Raises ``ContentNotFoundError``."""
        ...

    async def list_projects(self) -> list[Project]:
        """Return every Cyberdyne project, deterministically ordered."""
        ...

    async def list_service_sections(self) -> list[ServiceSection]:
        """Return every service-offering card."""
        ...

    async def list_contact_methods(self) -> list[ContactMethod]:
        """Return every contact channel."""
        ...

    async def list_resource_groups(self) -> list[ResourceGroup]:
        """Return every resource-link cluster (Learn view footer)."""
        ...
