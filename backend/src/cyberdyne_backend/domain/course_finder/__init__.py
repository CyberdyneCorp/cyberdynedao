"""Scan-to-Learn bounded context (issue #231).

Reads a photographed question, embeds it, and matches it (cosine) against an
embedded catalog of course + lesson texts. Below-threshold scans return a
no-match carrying the extracted query so the client can offer "Request this
course" (the #232 demand registry consumes that separately).
"""

from cyberdyne_backend.domain.course_finder.entities import (
    RELEVANCE_THRESHOLD,
    CatalogEntry,
    CourseMatch,
    ScanQuery,
    cosine,
    rank_matches,
)
from cyberdyne_backend.domain.course_finder.ports import (
    EmbeddingPort,
    VisionQuestionReaderPort,
)

__all__ = [
    "RELEVANCE_THRESHOLD",
    "CatalogEntry",
    "CourseMatch",
    "EmbeddingPort",
    "ScanQuery",
    "VisionQuestionReaderPort",
    "cosine",
    "rank_matches",
]
