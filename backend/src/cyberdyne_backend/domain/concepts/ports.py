"""Repository port for the concepts context."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from cyberdyne_backend.domain.concepts.entities import Concept, ConceptPage


@runtime_checkable
class ConceptRepository(Protocol):
    async def get_by_slug(self, slug: str) -> Concept:
        """Load a concept by slug. Raises ``ConceptNotFoundError``."""
        ...

    async def list_concepts(
        self,
        *,
        query: str | None = None,
        domain: str | None = None,
        cursor: str | None = None,
        limit: int = 20,
    ) -> ConceptPage:
        """Browse/search concepts. ``query`` matches title/summary
        (case-insensitive substring); ``domain`` filters exactly. Ordered
        by slug with an opaque keyset cursor."""
        ...

    async def create(self, concept: Concept) -> Concept:
        """Persist a new concept. Raises ``DuplicateConceptError`` if the
        slug already exists."""
        ...

    async def update(self, concept: Concept) -> Concept:
        """Persist changes to an existing concept (matched by slug).
        Raises ``ConceptNotFoundError`` if absent."""
        ...

    async def delete(self, slug: str) -> None:
        """Delete a concept by slug. Raises ``ConceptNotFoundError`` if
        absent."""
        ...
