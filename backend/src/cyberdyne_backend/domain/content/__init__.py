"""Content bounded context.

Owns the editorial copy that the frontend currently inlines in
``src/lib/data/*.ts``. Phase 1 + 2 surfaces:

- ``TeamMember`` — list aggregate, one row per teammate.
- ``Project`` — list aggregate, one row per Cyberdyne project.
- ``ServiceSection`` — list aggregate, one row per service-offering card.
- ``ContactMethod`` — list aggregate, one row per contact channel.
- ``ResourceGroup`` (+ ``ResourceLink``) — list of resource-link clusters.
- ``CyberdynePage`` — page-level payloads (about, services-meta,
  contact-meta) stored as JSON documents keyed by slug. Normalised
  when admin authoring lands (Phase 3+).

Blog and learning content live in sibling contexts so the bounded
contexts don't bleed into each other.
"""

from cyberdyne_backend.domain.content.entities import (
    ContactMethod,
    CyberdynePage,
    Project,
    ResourceGroup,
    ResourceLink,
    ServiceBullet,
    ServiceSection,
    TeamMember,
)
from cyberdyne_backend.domain.content.ports import ContentRepository

__all__ = [
    "ContactMethod",
    "ContentRepository",
    "CyberdynePage",
    "Project",
    "ResourceGroup",
    "ResourceLink",
    "ServiceBullet",
    "ServiceSection",
    "TeamMember",
]
