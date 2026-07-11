"""Web search context: read-only open-web search for the chat agents."""

from cyberdyne_backend.domain.websearch.entities import (
    DEFAULT_RESULTS,
    MAX_RESULTS,
    MIN_RESULTS,
    SearchResponse,
    SearchResult,
    clamp_num_results,
)
from cyberdyne_backend.domain.websearch.errors import (
    InvalidQueryError,
    SearchProviderError,
    SearchUnavailableError,
    WebSearchError,
)
from cyberdyne_backend.domain.websearch.ports import WebSearchPort

__all__ = [
    "DEFAULT_RESULTS",
    "MAX_RESULTS",
    "MIN_RESULTS",
    "InvalidQueryError",
    "SearchProviderError",
    "SearchResponse",
    "SearchResult",
    "SearchUnavailableError",
    "WebSearchError",
    "WebSearchPort",
    "clamp_num_results",
]
