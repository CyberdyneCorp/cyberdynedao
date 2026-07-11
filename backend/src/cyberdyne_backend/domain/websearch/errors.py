"""Errors for the websearch context."""

from __future__ import annotations


class WebSearchError(Exception):
    """Base class for websearch-context errors."""


class InvalidQueryError(WebSearchError):
    """The query is empty or otherwise unusable."""


class SearchUnavailableError(WebSearchError):
    """Web search is not configured (no SERPAPI key) — the capability is off."""


class SearchProviderError(WebSearchError):
    """The search engine could not be reached or rejected the request
    (network error, bad key, quota exhausted) — retryable or ops-fixable,
    not the caller's fault."""
