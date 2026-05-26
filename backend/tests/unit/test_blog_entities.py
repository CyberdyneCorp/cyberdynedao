"""Tests for the blog domain entities + ``new_blog_post`` factory."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from cyberdyne_backend.domain.blog import (
    BlogPostAlreadyPublishedError,
    BlogPostStatus,
    new_blog_post,
)
from cyberdyne_backend.domain.blog.entities import _first_paragraph, normalize_slug


class TestNormalizeSlug:
    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ("Hello World", "hello-world"),
            ("  Foo Bar!  ", "foo-bar"),
            ("multi   spaces", "multi-spaces"),
            ("PunCt..Uation??", "punct-uation"),
            ("---trim---", "trim"),
        ],
    )
    def test_cases(self, raw: str, expected: str) -> None:
        assert normalize_slug(raw) == expected


class TestNewBlogPost:
    def test_starts_in_draft_with_derived_slug(self) -> None:
        post = new_blog_post(title="Hello World", body_md="paragraph 1\n\nparagraph 2")
        assert post.status is BlogPostStatus.DRAFT
        assert post.slug == "hello-world"
        assert post.published_at is None
        assert post.excerpt == "paragraph 1"

    def test_uses_explicit_slug_when_provided(self) -> None:
        post = new_blog_post(title="Whatever", body_md="x", slug="My Custom Slug")
        assert post.slug == "my-custom-slug"

    def test_uses_explicit_excerpt(self) -> None:
        post = new_blog_post(title="x", body_md="long content", excerpt="hand-written")
        assert post.excerpt == "hand-written"

    def test_strips_whitespace_tags_drops_empties(self) -> None:
        post = new_blog_post(title="x", body_md="x", tags=["  a ", "", "b"])
        assert post.tags == ("a", "b")

    def test_empty_title_rejected(self) -> None:
        with pytest.raises(ValueError):
            new_blog_post(title="   ", body_md="x")

    def test_empty_body_rejected(self) -> None:
        with pytest.raises(ValueError):
            new_blog_post(title="t", body_md="   ")

    def test_slug_normalising_to_empty_rejected(self) -> None:
        with pytest.raises(ValueError):
            new_blog_post(title="!!!!", body_md="x")


class TestVisibilityAndPublish:
    def test_drafts_are_invisible_to_anon(self) -> None:
        post = new_blog_post(title="t", body_md="x")
        assert not post.is_visible_to_anonymous()

    def test_publish_promotes_status_and_sets_timestamps(self) -> None:
        post = new_blog_post(title="t", body_md="x")
        fixed = datetime(2030, 1, 1, tzinfo=UTC)
        post.publish(now=fixed)
        assert post.status is BlogPostStatus.PUBLISHED
        assert post.published_at == fixed
        assert post.updated_at == fixed
        assert post.is_visible_to_anonymous()

    def test_publish_twice_raises(self) -> None:
        post = new_blog_post(title="t", body_md="x")
        post.publish()
        with pytest.raises(BlogPostAlreadyPublishedError):
            post.publish()


class TestFirstParagraph:
    def test_skips_headings(self) -> None:
        body = "# Heading\n\nReal first paragraph."
        assert _first_paragraph(body) == "Real first paragraph."

    def test_trims_long_paragraph_at_word_boundary(self) -> None:
        long = "word " * 100
        result = _first_paragraph(long, max_chars=20)
        assert len(result) <= 21  # +1 for the ellipsis
        assert result.endswith("…")

    def test_empty_body_returns_empty(self) -> None:
        assert _first_paragraph("\n\n\n") == ""
