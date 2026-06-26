"""Scan-to-Learn domain entities + pure matching (issue #231).

A photographed question is read into a :class:`ScanQuery` (the extracted
question text, an optional subject, and keywords). The query is embedded and
matched (cosine) against an embedded catalog of course + lesson texts. Ranking
is a pure function over vectors so it is trivially unit-testable; the
embeddings themselves come from an outbound port.

Nothing here touches the network or the DB — the embedding source and the
catalog text source are ports owned by the application/adapter layers.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from uuid import UUID

# Minimum cosine score for a catalog entry to count as a match. Tuned for the
# deterministic set-of-words fallback embedding (keyword overlap): a genuine
# topical hit clears ~0.2 to 0.5 while an unrelated query sits at/near 0 (only
# incidental shared words push it to ~0.15), so this cleanly separates the two.
# OpenAI's dense embeddings score genuine hits far higher, so the same gate is
# conservative there too.
RELEVANCE_THRESHOLD = 0.18


@dataclass(frozen=True, slots=True)
class ScanQuery:
    """What the vision step extracted from the photographed question."""

    question: str
    subject: str | None = None
    keywords: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class CourseMatch:
    """A ranked catalog hit. ``lesson_id`` is set for a lesson-level entry
    (a deep-linkable lesson); ``None`` for a course-level entry."""

    course_slug: str
    lesson_id: UUID | None
    score: float
    match_reason: str


@dataclass(frozen=True, slots=True)
class CatalogEntry:
    """One indexable catalog text: a course or a lesson within one."""

    course_slug: str
    lesson_id: UUID | None
    text: str


def cosine(a: list[float], b: list[float]) -> float:
    """Cosine similarity of two equal-length vectors. Returns 0.0 when either
    vector is empty, zero-norm, or the lengths differ (defensive — callers
    embed with one model, so dimensions match in practice)."""
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = 0.0
    norm_a = 0.0
    norm_b = 0.0
    for x, y in zip(a, b, strict=True):
        dot += x * y
        norm_a += x * x
        norm_b += y * y
    if norm_a <= 0.0 or norm_b <= 0.0:
        return 0.0
    return dot / (math.sqrt(norm_a) * math.sqrt(norm_b))


def rank_matches(
    query_vec: list[float],
    entries_with_vecs: list[tuple[CatalogEntry, list[float]]],
    *,
    top_k: int,
    threshold: float,
) -> list[CourseMatch]:
    """Score every entry by cosine against the query, keep those at/above the
    threshold, and return the top ``top_k`` sorted by descending score."""
    scored: list[CourseMatch] = []
    for entry, vec in entries_with_vecs:
        score = cosine(query_vec, vec)
        if score < threshold:
            continue
        scored.append(
            CourseMatch(
                course_slug=entry.course_slug,
                lesson_id=entry.lesson_id,
                score=score,
                match_reason=_match_reason(entry),
            )
        )
    scored.sort(key=lambda m: m.score, reverse=True)
    return scored[:top_k]


def _match_reason(entry: CatalogEntry) -> str:
    kind = "lesson" if entry.lesson_id is not None else "course"
    return f"matched {kind}: {entry.text}"
