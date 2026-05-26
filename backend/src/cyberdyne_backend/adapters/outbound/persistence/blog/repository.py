"""SQLAlchemy adapter for ``BlogRepository``."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.blog.models import (
    BlogCategoryRow,
    BlogPostRow,
)
from cyberdyne_backend.domain.blog import (
    BlogCategory,
    BlogPost,
    BlogPostNotFoundError,
    BlogPostStatus,
    DuplicateSlugError,
)


def _row_to_post(row: BlogPostRow) -> BlogPost:
    return BlogPost(
        id=row.id,
        slug=row.slug,
        title=row.title,
        body_md=row.body_md,
        excerpt=row.excerpt,
        category_slug=row.category_slug,
        author_user_id=row.author_user_id,
        status=BlogPostStatus(row.status),
        tags=tuple(row.tags),
        created_at=row.created_at,
        published_at=row.published_at,
        updated_at=row.updated_at,
    )


class SqlAlchemyBlogRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, post: BlogPost) -> None:
        existing = await self._session.get(BlogPostRow, post.id)
        if existing is None:
            # Check for slug collision before insert so we can raise a
            # typed error instead of an IntegrityError.
            collision = await self._session.execute(
                select(BlogPostRow.id).where(BlogPostRow.slug == post.slug)
            )
            if collision.scalar_one_or_none() is not None:
                raise DuplicateSlugError(post.slug)
            self._session.add(
                BlogPostRow(
                    id=post.id,
                    slug=post.slug,
                    title=post.title,
                    body_md=post.body_md,
                    excerpt=post.excerpt,
                    category_slug=post.category_slug,
                    author_user_id=post.author_user_id,
                    status=post.status.value,
                    tags=list(post.tags),
                    created_at=post.created_at,
                    published_at=post.published_at,
                    updated_at=post.updated_at,
                )
            )
        else:
            existing.title = post.title
            existing.body_md = post.body_md
            existing.excerpt = post.excerpt
            existing.category_slug = post.category_slug
            existing.author_user_id = post.author_user_id
            existing.status = post.status.value
            existing.tags = list(post.tags)
            existing.published_at = post.published_at
            existing.updated_at = post.updated_at
        try:
            await self._session.flush()
        except IntegrityError as exc:
            raise DuplicateSlugError(post.slug) from exc

    async def get_by_slug(self, slug: str, *, include_drafts: bool = False) -> BlogPost:
        stmt = select(BlogPostRow).where(BlogPostRow.slug == slug)
        if not include_drafts:
            stmt = stmt.where(BlogPostRow.status == BlogPostStatus.PUBLISHED.value)
        row = (await self._session.execute(stmt)).scalar_one_or_none()
        if row is None:
            raise BlogPostNotFoundError(slug)
        return _row_to_post(row)

    async def list_posts(
        self,
        *,
        category: str | None = None,
        tag: str | None = None,
        include_drafts: bool = False,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[BlogPost], int]:
        stmt = select(BlogPostRow)
        count_stmt = select(func.count(BlogPostRow.id))
        if not include_drafts:
            stmt = stmt.where(BlogPostRow.status == BlogPostStatus.PUBLISHED.value)
            count_stmt = count_stmt.where(BlogPostRow.status == BlogPostStatus.PUBLISHED.value)
        if category:
            stmt = stmt.where(BlogPostRow.category_slug == category)
            count_stmt = count_stmt.where(BlogPostRow.category_slug == category)
        # Tag filtering on a JSON column — dialect-specific. For Phase 3
        # we filter in Python on the page slice to keep it portable
        # between sqlite (test) and Postgres (prod). Pagination still
        # happens at the DB level on the un-tag-filtered set; tag
        # filter is best-effort within the page. Promote to a proper
        # `tags` table if traffic warrants it.
        total = (await self._session.execute(count_stmt)).scalar_one()
        stmt = (
            stmt.order_by(
                BlogPostRow.published_at.desc().nullslast(), BlogPostRow.created_at.desc()
            )
            .offset(max(0, (page - 1) * page_size))
            .limit(page_size)
        )
        rows = (await self._session.execute(stmt)).scalars().all()
        posts = [_row_to_post(r) for r in rows]
        if tag:
            posts = [p for p in posts if tag in p.tags]
        return posts, total

    async def list_categories(self) -> list[BlogCategory]:
        rows = (
            (await self._session.execute(select(BlogCategoryRow).order_by(BlogCategoryRow.slug)))
            .scalars()
            .all()
        )
        return [BlogCategory(slug=r.slug, name=r.name, palette=r.palette) for r in rows]
