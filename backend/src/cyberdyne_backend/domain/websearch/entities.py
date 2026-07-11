"""Web search domain entities.

The websearch context wraps read-only access to a web search engine
(SERPAPI over Google), exposing organic results and — when the engine
provides one — a direct answer. It exists to give the chat agents
open-web grounding; it stores nothing and owns no persistence.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Result-count bounds. The engine caps a single page; callers asking for
# more than this get the ceiling rather than an error.
MIN_RESULTS = 1
MAX_RESULTS = 20
DEFAULT_RESULTS = 10


def clamp_num_results(num: int) -> int:
    return max(MIN_RESULTS, min(num, MAX_RESULTS))


@dataclass(frozen=True, slots=True)
class SearchResult:
    """One organic search result."""

    position: int
    title: str
    url: str
    snippet: str = ""
    source: str = ""


@dataclass(frozen=True, slots=True)
class SearchResponse:
    """A search query's results plus an optional direct answer."""

    query: str
    results: tuple[SearchResult, ...] = field(default_factory=tuple)
    # A concise direct answer when the engine surfaces one (answer box);
    # ``None`` when it only returned organic links.
    answer: str | None = None
