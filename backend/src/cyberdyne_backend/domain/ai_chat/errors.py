"""Domain errors for the AI chat context."""

from __future__ import annotations


class ChatSessionNotFoundError(LookupError):
    """No session with that id exists."""


class ChatProviderError(RuntimeError):
    """The upstream LLM call failed and we have no cached fallback."""
