"""Ports for the content context.

Concrete impl lives in
``adapters/outbound/persistence/content/repository.py``. A FakeRepo for
unit tests lives next to the application use cases.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from cyberdyne_backend.domain.content.entities import CyberdynePage, TeamMember


class ContentNotFoundError(LookupError):
    """No content page with the requested slug exists."""


@runtime_checkable
class ContentRepository(Protocol):
    async def list_team(self) -> list[TeamMember]:
        """Return all team members, deterministically ordered."""
        ...

    async def get_page(self, slug: str) -> CyberdynePage:
        """Return the page with this slug. Raises ``ContentNotFoundError``."""
        ...
