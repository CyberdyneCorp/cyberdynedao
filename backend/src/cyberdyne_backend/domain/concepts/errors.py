"""Domain errors for the concepts context."""

from __future__ import annotations


class ConceptNotFoundError(LookupError):
    """Raised when a concept cannot be found by slug."""


class InvalidConceptError(ValueError):
    """Raised when a concept fails its invariants."""


class DuplicateConceptError(ValueError):
    """Raised when creating a concept whose slug already exists."""
