"""Ports the blog context depends on."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from cyberdyne_backend.domain.blog.entities import BlogCategory, BlogPost


@runtime_checkable
class BlogRepository(Protocol):
    async def save(self, post: BlogPost) -> None:
        """Insert or update a blog post.

        Raises ``DuplicateSlugError`` if another post with the same
        slug already exists.
        """
        ...

    async def get_by_slug(self, slug: str, *, include_drafts: bool = False) -> BlogPost:
        """Load a post by slug. Raises ``BlogPostNotFoundError``."""
        ...

    async def list_posts(
        self,
        *,
        category: str | None = None,
        tag: str | None = None,
        include_drafts: bool = False,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[BlogPost], int]:
        """Paginated list. Returns (items, total). Drafts are filtered
        out unless ``include_drafts`` is true (editor scope only)."""
        ...

    async def list_categories(self) -> list[BlogCategory]: ...
