"""Domain errors for the blog context."""

from __future__ import annotations


class BlogPostNotFoundError(LookupError):
    """No blog post with the requested slug exists (or it's a draft
    and the caller has no editor scope)."""


class DuplicateSlugError(ValueError):
    """A post with this slug already exists."""


class BlogPostAlreadyPublishedError(ValueError):
    """The post is already in the ``published`` state."""
