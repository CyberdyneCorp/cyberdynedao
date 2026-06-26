"""Unit tests for Scan-to-Learn matching (issue #231).

Covers the pure ranking maths, the deterministic static embedder, the in-memory
search index (with injected vectors), and the ScanToLearn use case with a fake
vision reader + injected index.
"""

from __future__ import annotations

import uuid

import pytest

from cyberdyne_backend.adapters.outbound.llm.embedding_client import StaticEmbeddingClient
from cyberdyne_backend.application.course_finder import CatalogSearchIndex, ScanToLearn
from cyberdyne_backend.domain.course_finder import (
    RELEVANCE_THRESHOLD,
    CatalogEntry,
    ScanQuery,
    cosine,
    rank_matches,
)

# Async tests are collected automatically (asyncio_mode = "auto"); sync helpers
# below stay sync, so no module-level asyncio marker.


# ── cosine ─────────────────────────────────────────────────────────────


def test_cosine_identical_vectors_is_one() -> None:
    assert cosine([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]) == pytest.approx(1.0)


def test_cosine_orthogonal_vectors_is_zero() -> None:
    assert cosine([1.0, 0.0], [0.0, 1.0]) == pytest.approx(0.0)


def test_cosine_handles_empty_zero_and_mismatched() -> None:
    assert cosine([], [1.0]) == 0.0
    assert cosine([0.0, 0.0], [1.0, 1.0]) == 0.0
    assert cosine([1.0, 2.0], [1.0]) == 0.0


# ── rank_matches ───────────────────────────────────────────────────────


def test_rank_matches_sorts_desc_filters_threshold_and_caps_top_k() -> None:
    query = [1.0, 0.0]
    entries = [
        (CatalogEntry("a", None, "exact"), [1.0, 0.0]),  # cosine 1.0
        (CatalogEntry("b", None, "partial"), [1.0, 1.0]),  # cosine ~0.707
        (CatalogEntry("c", None, "orthogonal"), [0.0, 1.0]),  # cosine 0.0 (dropped)
    ]
    matches = rank_matches(query, entries, top_k=5, threshold=0.3)
    assert [m.course_slug for m in matches] == ["a", "b"]
    assert matches[0].score > matches[1].score

    top1 = rank_matches(query, entries, top_k=1, threshold=0.3)
    assert [m.course_slug for m in top1] == ["a"]


def test_rank_matches_reason_names_kind() -> None:
    lesson_id = uuid.uuid4()
    entries = [
        (CatalogEntry("course-a", None, "Course A. About"), [1.0, 0.0]),
        (CatalogEntry("course-a", lesson_id, "Course A — Lesson 1"), [1.0, 0.0]),
    ]
    matches = rank_matches([1.0, 0.0], entries, top_k=5, threshold=0.0)
    by_lesson = {m.lesson_id: m for m in matches}
    assert "course:" in by_lesson[None].match_reason
    assert "lesson:" in by_lesson[lesson_id].match_reason


# ── StaticEmbeddingClient ──────────────────────────────────────────────


async def test_static_embedder_is_deterministic_and_normalized() -> None:
    embedder = StaticEmbeddingClient()
    [first] = await embedder.embed(["Linear algebra eigenvalues"])
    [again] = await embedder.embed(["Linear algebra eigenvalues"])
    assert first == again
    norm = sum(v * v for v in first) ** 0.5
    assert norm == pytest.approx(1.0)


async def test_static_embedder_keyword_overlap_scores_higher() -> None:
    embedder = StaticEmbeddingClient()
    query, related, unrelated = await embedder.embed(
        [
            "eigenvalues of a matrix",
            "matrix eigenvalues linear algebra",
            "photosynthesis in plant cells",
        ]
    )
    assert cosine(query, related) > cosine(query, unrelated)


async def test_static_embedder_empty_text_is_zero_vector() -> None:
    embedder = StaticEmbeddingClient()
    [vec] = await embedder.embed(["!!! ???"])
    assert all(v == 0.0 for v in vec)


# ── CatalogSearchIndex ─────────────────────────────────────────────────


async def _prebuilt_index() -> CatalogSearchIndex:
    embedder = StaticEmbeddingClient()
    texts = [
        "Linear Algebra. Vectors, matrices, eigenvalues and eigenvectors.",
        "Organic Chemistry. Carbon compounds, reactions and synthesis.",
    ]
    vectors = await embedder.embed(texts)
    entries = [
        CatalogEntry("linear-algebra", None, texts[0]),
        CatalogEntry("organic-chemistry", None, texts[1]),
    ]
    return CatalogSearchIndex.with_prebuilt(
        list(zip(entries, vectors, strict=True)), embedder=embedder
    )


async def test_index_returns_best_course_first() -> None:
    index = await _prebuilt_index()
    matches = await index.search("how do I compute eigenvalues of a matrix")
    assert matches
    assert matches[0].course_slug == "linear-algebra"


async def test_index_returns_empty_for_unrelated_query() -> None:
    index = await _prebuilt_index()
    matches = await index.search("ancient roman military tactics and siege warfare")
    assert matches == []


async def test_index_builds_from_source_once() -> None:
    embedder = StaticEmbeddingClient()
    entries = [CatalogEntry("calculus", None, "Calculus. Derivatives and integrals.")]

    class _CountingSource:
        def __init__(self) -> None:
            self.calls = 0

        async def entries(self) -> list[CatalogEntry]:
            self.calls += 1
            return entries

    source = _CountingSource()
    index = CatalogSearchIndex(source=source, embedder=embedder)
    await index.search("derivatives and integrals calculus")
    await index.search("integrals")
    assert source.calls == 1  # catalog embedded once, cached thereafter


async def test_index_empty_catalog_returns_no_matches() -> None:
    class _EmptySource:
        async def entries(self) -> list[CatalogEntry]:
            return []

    index = CatalogSearchIndex(source=_EmptySource(), embedder=StaticEmbeddingClient())
    assert await index.search("anything") == []


async def test_index_blank_query_returns_no_matches() -> None:
    index = await _prebuilt_index()
    assert await index.search("   ") == []


# ── ScanToLearn ────────────────────────────────────────────────────────


class _FakeReader:
    def __init__(self, query: ScanQuery) -> None:
        self._query = query
        self.seen: tuple[bytes, str] | None = None

    async def read_question(self, *, image_bytes: bytes, content_type: str) -> ScanQuery:
        self.seen = (image_bytes, content_type)
        return self._query


async def test_scan_returns_matches_for_in_catalog_topic() -> None:
    index = await _prebuilt_index()
    reader = _FakeReader(
        ScanQuery(question="Find the eigenvalues of A", subject="Math", keywords=("matrix",))
    )
    use_case = ScanToLearn(reader=reader, index=index)
    result = await use_case.execute(image_bytes=b"img", content_type="image/png")
    assert not result.no_match
    assert result.matches[0].course_slug == "linear-algebra"
    assert result.query.question == "Find the eigenvalues of A"
    assert reader.seen == (b"img", "image/png")


async def test_scan_no_match_returns_extracted_query() -> None:
    index = await _prebuilt_index()
    query = ScanQuery(question="Explain Roman siege warfare", subject="History", keywords=())
    use_case = ScanToLearn(reader=_FakeReader(query), index=index)
    result = await use_case.execute(image_bytes=b"x", content_type="image/jpeg")
    assert result.no_match
    assert result.matches == []
    assert result.query == query


def test_relevance_threshold_is_sane() -> None:
    assert 0.0 < RELEVANCE_THRESHOLD < 1.0
