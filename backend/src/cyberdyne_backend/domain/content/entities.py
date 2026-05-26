"""Domain entities for the content context."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class TeamMember:
    id: str
    name: str
    title: str
    image_url: str
    bio: str
    tags: tuple[str, ...]
    palette: str


@dataclass(frozen=True, slots=True)
class CyberdynePage:
    """The Cyberdyne about-us page payload.

    Held as an opaque ``dict[str, Any]`` for Phase 1 because:

    1. The shape is rich (domains, beliefs, tokenomics, roadmap,
       economics) and changes per-section over time.
    2. There is no admin-editing UI yet; content is seeded via an
       Alembic data migration. Normalising the schema before we have
       an editor would invest in the wrong abstraction.
    3. The router layer pins a strict pydantic response schema so the
       OpenAPI surface stays typed even when the domain object is dict-
       shaped.

    Phase 3 (admin authoring) can split this into per-section
    aggregates when there's a real reason to.
    """

    slug: str
    payload: dict[str, Any]
