"""Blog domain entities."""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID

from cyberdyne_backend.domain.blog.errors import BlogPostAlreadyPublishedError


class BlogPostStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"


@dataclass(frozen=True, slots=True)
class BlogCategory:
    slug: str
    name: str
    palette: str


_SLUG_RE = re.compile(r"[^a-z0-9]+")


def normalize_slug(text: str) -> str:
    """Lowercase, replace non-alphanumerics with hyphens, trim hyphens.

    Used both for blog post slugs and to validate inputs from the admin
    POST endpoint. Two posts can never collide on slug — repository
    enforces that with a unique constraint and surfaces ``DuplicateSlugError``.
    """
    cleaned = _SLUG_RE.sub("-", text.strip().lower()).strip("-")
    return cleaned


@dataclass(slots=True)
class BlogPost:
    id: UUID
    slug: str
    title: str
    body_md: str
    excerpt: str
    category_slug: str | None
    author_user_id: UUID | None
    status: BlogPostStatus
    tags: tuple[str, ...]
    created_at: datetime
    published_at: datetime | None = None
    updated_at: datetime | None = None

    def is_visible_to_anonymous(self) -> bool:
        return self.status is BlogPostStatus.PUBLISHED and self.published_at is not None

    def publish(self, now: datetime | None = None) -> None:
        if self.status is BlogPostStatus.PUBLISHED:
            raise BlogPostAlreadyPublishedError(self.slug)
        self.status = BlogPostStatus.PUBLISHED
        self.published_at = now or datetime.now(tz=UTC)
        self.updated_at = self.published_at


def new_blog_post(
    *,
    title: str,
    body_md: str,
    excerpt: str = "",
    slug: str | None = None,
    category_slug: str | None = None,
    author_user_id: UUID | None = None,
    tags: list[str] | tuple[str, ...] = (),
    now: datetime | None = None,
) -> BlogPost:
    if not title.strip():
        raise ValueError("title cannot be empty")
    if not body_md.strip():
        raise ValueError("body_md cannot be empty")
    effective_slug = normalize_slug(slug) if slug else normalize_slug(title)
    if not effective_slug:
        raise ValueError("slug normalises to empty")
    created_at = now or datetime.now(tz=UTC)
    derived_excerpt = excerpt.strip() or _first_paragraph(body_md)
    return BlogPost(
        id=uuid.uuid4(),
        slug=effective_slug,
        title=title.strip(),
        body_md=body_md.strip(),
        excerpt=derived_excerpt,
        category_slug=category_slug,
        author_user_id=author_user_id,
        status=BlogPostStatus.DRAFT,
        tags=tuple(t.strip() for t in tags if t.strip()),
        created_at=created_at,
    )


def _first_paragraph(body_md: str, max_chars: int = 280) -> str:
    """Pick the first non-empty paragraph as a fallback excerpt."""
    for raw in body_md.split("\n\n"):
        para = raw.strip()
        if not para or para.startswith("#"):
            continue
        if len(para) <= max_chars:
            return para
        # Trim at a word boundary so the excerpt isn't cut mid-word.
        trimmed = para[:max_chars].rsplit(" ", 1)[0]
        return f"{trimmed}…"
    return ""
