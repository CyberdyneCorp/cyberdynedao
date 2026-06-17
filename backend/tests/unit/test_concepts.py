"""Unit tests for concepts domain + use cases (issue #168)."""

from __future__ import annotations

import asyncio

import pytest

from cyberdyne_backend.application.concepts import (
    ConceptInput,
    ListConcepts,
    UpdateConcept,
)
from cyberdyne_backend.domain.concepts import (
    Concept,
    ConceptPage,
    InvalidConceptError,
    new_concept,
)


def test_new_concept_validates_and_trims() -> None:
    c = new_concept(
        slug="ohms-law",
        title="  Ohm's Law  ",
        domain="Electronics",
        summary="V = I·R",
        formula=" V=IR ",
    )
    assert c.title == "Ohm's Law"
    assert c.formula == "V=IR"
    assert c.updated_at is not None


def test_new_concept_rejects_bad_slug() -> None:
    with pytest.raises(InvalidConceptError):
        new_concept(slug="Ohms Law", title="t", domain="d", summary="s")


def test_new_concept_rejects_empty_summary() -> None:
    with pytest.raises(InvalidConceptError):
        new_concept(slug="x", title="t", domain="d", summary="   ")


class _FakeRepo:
    def __init__(self) -> None:
        self.by_slug: dict[str, Concept] = {}
        self.calls: list[dict] = []

    async def get_by_slug(self, slug: str) -> Concept:
        return self.by_slug[slug]

    async def list_concepts(self, *, query=None, domain=None, cursor=None, limit=20):
        self.calls.append({"query": query, "domain": domain, "cursor": cursor, "limit": limit})
        return ConceptPage(items=list(self.by_slug.values()), next_cursor=None)

    async def update(self, concept: Concept) -> Concept:
        self.by_slug[concept.slug] = concept
        return concept


def test_list_clamps_limit() -> None:
    repo = _FakeRepo()
    asyncio.run(ListConcepts(repo=repo).execute(limit=9999))
    asyncio.run(ListConcepts(repo=repo).execute(limit=0))
    assert repo.calls[0]["limit"] == 100
    assert repo.calls[1]["limit"] == 1


def test_update_preserves_id_and_created_at() -> None:
    repo = _FakeRepo()
    original = new_concept(slug="kvl", title="KVL", domain="EE", summary="sum=0")
    repo.by_slug["kvl"] = original

    out = asyncio.run(
        UpdateConcept(repo=repo).execute(
            "kvl",
            ConceptInput(
                slug="kvl",
                title="Kirchhoff Voltage Law",
                domain="EE",
                summary="sum of voltages = 0",
            ),
        )
    )
    assert out.id == original.id  # identity preserved
    assert out.created_at == original.created_at  # creation time preserved
    assert out.title == "Kirchhoff Voltage Law"
