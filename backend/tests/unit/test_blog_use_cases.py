"""Use-case tests for the blog context, with a hand-written fake repo."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from cyberdyne_backend.application.blog import (
    CreateBlogPost,
    CreateBlogPostCommand,
    GenerateRssFeed,
    GetBlogPost,
    ListBlogPosts,
    ListBlogPostsQuery,
    PublishBlogPost,
)
from cyberdyne_backend.domain.blog import (
    BlogCategory,
    BlogPost,
    BlogPostNotFoundError,
    BlogPostStatus,
    BlogRepository,
    DuplicateSlugError,
    new_blog_post,
)


class FakeBlogRepo:
    def __init__(self, seed: list[BlogPost] | None = None) -> None:
        self._posts: dict[str, BlogPost] = {p.slug: p for p in (seed or [])}

    async def save(self, post: BlogPost) -> None:
        # Detect slug collisions only when adding a *different* post id
        # with an existing slug.
        existing = self._posts.get(post.slug)
        if existing is not None and existing.id != post.id:
            raise DuplicateSlugError(post.slug)
        self._posts[post.slug] = post

    async def get_by_slug(self, slug: str, *, include_drafts: bool = False) -> BlogPost:
        post = self._posts.get(slug)
        if post is None:
            raise BlogPostNotFoundError(slug)
        if not include_drafts and post.status is not BlogPostStatus.PUBLISHED:
            raise BlogPostNotFoundError(slug)
        return post

    async def list_posts(
        self,
        *,
        category: str | None = None,
        tag: str | None = None,
        include_drafts: bool = False,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[BlogPost], int]:
        items = list(self._posts.values())
        if not include_drafts:
            items = [p for p in items if p.status is BlogPostStatus.PUBLISHED]
        if category:
            items = [p for p in items if p.category_slug == category]
        if tag:
            items = [p for p in items if tag in p.tags]
        items.sort(
            key=lambda p: p.published_at or p.created_at,
            reverse=True,
        )
        total = len(items)
        return items[(page - 1) * page_size : page * page_size], total

    async def list_categories(self) -> list[BlogCategory]:
        return []


# Smoke test against the AsyncRepository Protocol so we know the fake
# is structurally compatible with the port.
def test_fake_repo_matches_port() -> None:
    assert isinstance(FakeBlogRepo(), BlogRepository)


# ── CreateBlogPost ───────────────────────────────────────────────────


class TestCreateBlogPost:
    async def test_creates_draft(self) -> None:
        repo = FakeBlogRepo()
        uc = CreateBlogPost(repo=repo)
        post = await uc.execute(CreateBlogPostCommand(title="Hello", body_md="content"))
        assert post.status is BlogPostStatus.DRAFT
        assert post.slug == "hello"

    async def test_collision_raises(self) -> None:
        existing = new_blog_post(title="Hello", body_md="content")
        repo = FakeBlogRepo(seed=[existing])
        uc = CreateBlogPost(repo=repo)
        with pytest.raises(DuplicateSlugError):
            await uc.execute(CreateBlogPostCommand(title="Hello", body_md="other"))


# ── PublishBlogPost ──────────────────────────────────────────────────


class TestPublishBlogPost:
    async def test_publishes_draft(self) -> None:
        draft = new_blog_post(title="Hi", body_md="x")
        repo = FakeBlogRepo(seed=[draft])
        uc = PublishBlogPost(repo=repo)
        result = await uc.execute(draft.slug)
        assert result.status is BlogPostStatus.PUBLISHED
        assert result.published_at is not None

    async def test_missing_post_raises(self) -> None:
        repo = FakeBlogRepo()
        uc = PublishBlogPost(repo=repo)
        with pytest.raises(BlogPostNotFoundError):
            await uc.execute("missing")


# ── GetBlogPost ──────────────────────────────────────────────────────


class TestGetBlogPost:
    async def test_published_visible_to_anon(self) -> None:
        published = new_blog_post(title="x", body_md="x")
        published.publish()
        repo = FakeBlogRepo(seed=[published])
        uc = GetBlogPost(repo=repo)
        assert (await uc.execute(published.slug)).slug == published.slug

    async def test_draft_404_for_anon(self) -> None:
        draft = new_blog_post(title="x", body_md="x")
        repo = FakeBlogRepo(seed=[draft])
        uc = GetBlogPost(repo=repo)
        with pytest.raises(BlogPostNotFoundError):
            await uc.execute(draft.slug)

    async def test_draft_visible_when_include_drafts_true(self) -> None:
        draft = new_blog_post(title="x", body_md="x")
        repo = FakeBlogRepo(seed=[draft])
        uc = GetBlogPost(repo=repo)
        assert (await uc.execute(draft.slug, include_drafts=True)).slug == draft.slug


# ── ListBlogPosts ────────────────────────────────────────────────────


class TestListBlogPosts:
    async def test_excludes_drafts_for_anon(self) -> None:
        draft = new_blog_post(title="a", body_md="x")
        published = new_blog_post(title="b", body_md="y")
        published.publish()
        uc = ListBlogPosts(repo=FakeBlogRepo(seed=[draft, published]))
        items, total = await uc.execute(ListBlogPostsQuery())
        assert total == 1
        assert items[0].slug == published.slug

    async def test_includes_drafts_for_editor(self) -> None:
        draft = new_blog_post(title="a", body_md="x")
        published = new_blog_post(title="b", body_md="y")
        published.publish()
        uc = ListBlogPosts(repo=FakeBlogRepo(seed=[draft, published]))
        items, total = await uc.execute(ListBlogPostsQuery(include_drafts=True))
        assert total == 2
        assert {i.slug for i in items} == {draft.slug, published.slug}

    async def test_page_size_clamped(self) -> None:
        uc = ListBlogPosts(repo=FakeBlogRepo())
        items, total = await uc.execute(ListBlogPostsQuery(page=0, page_size=10000))
        assert items == []
        assert total == 0


# ── GenerateRssFeed ──────────────────────────────────────────────────


class TestGenerateRssFeed:
    async def test_returns_well_formed_xml_with_published_posts(self) -> None:
        post = new_blog_post(title="<unsafe & html>", body_md="x")
        post.publish(now=datetime(2030, 1, 1, tzinfo=UTC))
        uc = GenerateRssFeed(
            repo=FakeBlogRepo(seed=[post]),
            site_url="https://example.com/",
        )
        xml = await uc.execute()
        assert "<?xml" in xml
        assert "<rss version='2.0'>" in xml
        # HTML-unsafe characters in the title escape correctly.
        assert "&amp;" in xml
        assert "&lt;unsafe" in xml
        assert "https://example.com/blog/" in xml

    async def test_empty_feed(self) -> None:
        uc = GenerateRssFeed(repo=FakeBlogRepo(), site_url="https://example.com")
        xml = await uc.execute()
        assert "<rss" in xml
        assert "<item>" not in xml
