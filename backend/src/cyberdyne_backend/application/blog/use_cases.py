"""Use cases for the blog context."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from cyberdyne_backend.domain.blog import (
    BlogPost,
    BlogRepository,
    new_blog_post,
)

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


@dataclass(slots=True)
class ListBlogPostsQuery:
    category: str | None = None
    tag: str | None = None
    include_drafts: bool = False
    page: int = 1
    page_size: int = DEFAULT_PAGE_SIZE


@dataclass(slots=True)
class ListBlogPosts:
    repo: BlogRepository

    async def execute(self, q: ListBlogPostsQuery) -> tuple[list[BlogPost], int]:
        return await self.repo.list_posts(
            category=q.category,
            tag=q.tag,
            include_drafts=q.include_drafts,
            page=max(1, q.page),
            page_size=min(max(1, q.page_size), MAX_PAGE_SIZE),
        )


@dataclass(slots=True)
class GetBlogPost:
    repo: BlogRepository

    async def execute(self, slug: str, *, include_drafts: bool = False) -> BlogPost:
        return await self.repo.get_by_slug(slug, include_drafts=include_drafts)


@dataclass(slots=True)
class CreateBlogPostCommand:
    title: str
    body_md: str
    excerpt: str = ""
    slug: str | None = None
    category_slug: str | None = None
    author_user_id: UUID | None = None
    tags: tuple[str, ...] = ()


@dataclass(slots=True)
class CreateBlogPost:
    repo: BlogRepository

    async def execute(self, cmd: CreateBlogPostCommand) -> BlogPost:
        post = new_blog_post(
            title=cmd.title,
            body_md=cmd.body_md,
            excerpt=cmd.excerpt,
            slug=cmd.slug,
            category_slug=cmd.category_slug,
            author_user_id=cmd.author_user_id,
            tags=cmd.tags,
        )
        await self.repo.save(post)
        return post


@dataclass(slots=True)
class PublishBlogPost:
    repo: BlogRepository

    async def execute(self, slug: str) -> BlogPost:
        post = await self.repo.get_by_slug(slug, include_drafts=True)
        post.publish()
        await self.repo.save(post)
        return post


@dataclass(slots=True)
class GenerateRssFeed:
    """Builds a minimal Atom-style RSS XML for the last N published posts.

    Returns the XML as a string — the router writes it directly.
    """

    repo: BlogRepository
    site_url: str
    feed_title: str = "Cyberdyne Blog"
    feed_description: str = "Latest from the Cyberdyne builder collective."
    limit: int = 50

    async def execute(self) -> str:
        posts, _total = await self.repo.list_posts(
            include_drafts=False, page=1, page_size=self.limit
        )
        # Hand-rolled XML — escapes all interpolation; small, readable,
        # zero dependencies. If we ever ship a richer feed we'll move to
        # ``feedgen``.
        items_xml = "\n".join(self._render_item(p) for p in posts)
        last_build = (
            posts[0].published_at.isoformat() if posts and posts[0].published_at is not None else ""
        )
        return (
            "<?xml version='1.0' encoding='UTF-8'?>\n"
            "<rss version='2.0'>\n"
            "<channel>\n"
            f"  <title>{_xml_escape(self.feed_title)}</title>\n"
            f"  <link>{_xml_escape(self.site_url)}</link>\n"
            f"  <description>{_xml_escape(self.feed_description)}</description>\n"
            f"  <lastBuildDate>{_xml_escape(last_build)}</lastBuildDate>\n"
            f"{items_xml}\n"
            "</channel>\n"
            "</rss>\n"
        )

    def _render_item(self, post: BlogPost) -> str:
        link = f"{self.site_url.rstrip('/')}/blog/{post.slug}"
        pub = post.published_at.isoformat() if post.published_at else ""
        return (
            "  <item>\n"
            f"    <title>{_xml_escape(post.title)}</title>\n"
            f"    <link>{_xml_escape(link)}</link>\n"
            f"    <guid>{_xml_escape(str(post.id))}</guid>\n"
            f"    <pubDate>{_xml_escape(pub)}</pubDate>\n"
            f"    <description>{_xml_escape(post.excerpt)}</description>\n"
            "  </item>"
        )


def _xml_escape(value: str | datetime | None) -> str:
    if value is None:
        return ""
    s = value.isoformat() if isinstance(value, datetime) else str(value)
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )
