"""Scan-to-Learn application layer (issue #231).

Three pieces:

  * :class:`CatalogTextSource` — port over the courses repository that yields
    one indexable text per published course and per lesson (no vectors).
  * :class:`CatalogSearchIndex` — builds the embedded index lazily, caches the
    embedded entries in memory, and answers similarity searches. The cache is
    held by the index instance; the composition root keeps one instance per
    process so the catalog is embedded once, not per scan.
  * :class:`ScanToLearn` — reads the photographed question, builds a query
    string, searches, and reports matches or a no-match (carrying the query).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from cyberdyne_backend.domain.course_finder import (
    RELEVANCE_THRESHOLD,
    CatalogEntry,
    CourseMatch,
    EmbeddingPort,
    ScanQuery,
    VisionQuestionReaderPort,
    rank_matches,
)


@runtime_checkable
class CatalogTextSource(Protocol):
    async def entries(self) -> list[CatalogEntry]:
        """All indexable catalog texts (published courses + their lessons)."""
        ...


class CatalogSearchIndex:
    """Embedded catalog index with an in-memory cache.

    The first :meth:`search` (or explicit :meth:`build`) embeds every catalog
    text once; later searches reuse the cached vectors and only embed the
    query. Tests can bypass the build entirely by injecting prebuilt
    ``entries_with_vecs`` via :meth:`with_prebuilt`.
    """

    def __init__(
        self,
        *,
        source: CatalogTextSource,
        embedder: EmbeddingPort,
        threshold: float = RELEVANCE_THRESHOLD,
    ) -> None:
        self._source = source
        self._embedder = embedder
        self._threshold = threshold
        self._index: list[tuple[CatalogEntry, list[float]]] | None = None

    @classmethod
    def with_prebuilt(
        cls,
        entries_with_vecs: list[tuple[CatalogEntry, list[float]]],
        *,
        embedder: EmbeddingPort,
        threshold: float = RELEVANCE_THRESHOLD,
    ) -> CatalogSearchIndex:
        """An index whose catalog vectors are already known — used by tests so
        they never need a real catalog source."""
        index = cls(source=_EmptyTextSource(), embedder=embedder, threshold=threshold)
        index._index = list(entries_with_vecs)
        return index

    async def build(self) -> None:
        """Embed the whole catalog once and cache it. Idempotent."""
        if self._index is not None:
            return
        entries = await self._source.entries()
        if not entries:
            self._index = []
            return
        vectors = await self._embedder.embed([e.text for e in entries])
        self._index = list(zip(entries, vectors, strict=True))

    async def search(self, query_text: str, *, top_k: int = 5) -> list[CourseMatch]:
        await self.build()
        index = self._index or []
        if not index or not query_text.strip():
            return []
        query_vec = (await self._embedder.embed([query_text]))[0]
        return rank_matches(query_vec, index, top_k=top_k, threshold=self._threshold)


class _EmptyTextSource:
    """Source used by prebuilt indexes — its entries are never read."""

    async def entries(self) -> list[CatalogEntry]:  # pragma: no cover - never reached
        return []


@dataclass(frozen=True, slots=True)
class ScanResult:
    """Outcome of a scan: the extracted query plus any ranked matches."""

    query: ScanQuery
    matches: list[CourseMatch]

    @property
    def no_match(self) -> bool:
        return not self.matches


class ScanToLearn:
    """Read a photographed question and return ranked catalog matches.

    The image is analyzed only; nothing is persisted. A below-threshold result
    is a no-match carrying the extracted query so the client can offer to
    request the course (issue #232 consumes that — not called here)."""

    def __init__(
        self,
        *,
        reader: VisionQuestionReaderPort,
        index: CatalogSearchIndex,
        top_k: int = 5,
    ) -> None:
        self._reader = reader
        self._index = index
        self._top_k = top_k

    async def execute(self, *, image_bytes: bytes, content_type: str) -> ScanResult:
        query = await self._reader.read_question(image_bytes=image_bytes, content_type=content_type)
        matches = await self._index.search(_query_text(query), top_k=self._top_k)
        return ScanResult(query=query, matches=matches)


def _query_text(query: ScanQuery) -> str:
    """Fold the extracted question + subject + keywords into one search string."""
    parts = [query.question]
    if query.subject:
        parts.append(query.subject)
    parts.extend(query.keywords)
    return " ".join(p for p in parts if p).strip()
