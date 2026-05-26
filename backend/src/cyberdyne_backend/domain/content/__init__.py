"""Content bounded context.

Owns the editorial copy that the frontend currently inlines in
``src/lib/data/*.ts``. Phase 1 covers two surfaces:

- ``TeamMember`` — list aggregate, one row per teammate.
- ``CyberdynePage`` — the "about us" / domains / tokenomics / roadmap
  payload. Stored as a single document for Phase 1; normalized when
  admin authoring lands.

Blog and learning content live in sibling contexts so the bounded
contexts don't bleed into each other.
"""

from cyberdyne_backend.domain.content.entities import (
    CyberdynePage,
    TeamMember,
)
from cyberdyne_backend.domain.content.ports import ContentRepository

__all__ = [
    "ContentRepository",
    "CyberdynePage",
    "TeamMember",
]
