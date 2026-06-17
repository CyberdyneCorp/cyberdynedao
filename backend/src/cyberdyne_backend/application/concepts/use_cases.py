"""Use cases for the concepts library (issue #168)."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from cyberdyne_backend.domain.concepts import (
    Concept,
    ConceptPage,
    ConceptRepository,
    new_concept,
)

DEFAULT_CONCEPT_LIMIT = 20
MAX_CONCEPT_LIMIT = 100


@dataclass(slots=True)
class ListConcepts:
    repo: ConceptRepository

    async def execute(
        self,
        *,
        query: str | None = None,
        domain: str | None = None,
        cursor: str | None = None,
        limit: int = DEFAULT_CONCEPT_LIMIT,
    ) -> ConceptPage:
        clamped = max(1, min(limit, MAX_CONCEPT_LIMIT))
        return await self.repo.list_concepts(
            query=query, domain=domain, cursor=cursor, limit=clamped
        )


@dataclass(slots=True)
class GetConcept:
    repo: ConceptRepository

    async def execute(self, slug: str) -> Concept:
        return await self.repo.get_by_slug(slug)


@dataclass(slots=True)
class ConceptInput:
    slug: str
    title: str
    domain: str
    summary: str
    formula: str | None = None
    related_lesson_ids: tuple[UUID, ...] = ()
    related_course_slugs: tuple[str, ...] = ()


@dataclass(slots=True)
class CreateConcept:
    repo: ConceptRepository

    async def execute(self, data: ConceptInput) -> Concept:
        concept = new_concept(
            slug=data.slug,
            title=data.title,
            domain=data.domain,
            summary=data.summary,
            formula=data.formula,
            related_lesson_ids=data.related_lesson_ids,
            related_course_slugs=data.related_course_slugs,
        )
        return await self.repo.create(concept)


@dataclass(slots=True)
class UpdateConcept:
    repo: ConceptRepository

    async def execute(self, slug: str, data: ConceptInput) -> Concept:
        existing = await self.repo.get_by_slug(slug)
        # Rebuild via the factory so invariants re-run, preserving identity.
        updated = new_concept(
            slug=slug,
            title=data.title,
            domain=data.domain,
            summary=data.summary,
            formula=data.formula,
            related_lesson_ids=data.related_lesson_ids,
            related_course_slugs=data.related_course_slugs,
        )
        updated.id = existing.id
        updated.created_at = existing.created_at
        return await self.repo.update(updated)


@dataclass(slots=True)
class DeleteConcept:
    repo: ConceptRepository

    async def execute(self, slug: str) -> None:
        await self.repo.delete(slug)
