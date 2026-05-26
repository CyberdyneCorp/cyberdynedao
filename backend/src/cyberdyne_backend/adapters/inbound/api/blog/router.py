"""Blog endpoints — public read, admin write, RSS feed."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response

from cyberdyne_backend.adapters.inbound.api.blog.schemas import (
    BlogPostDetailResponse,
    BlogPostListResponse,
    BlogPostSummaryResponse,
    CreateBlogPostRequest,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import (
    EDITOR_SCOPE,
    require_editor,
)
from cyberdyne_backend.application.blog import (
    CreateBlogPost,
    CreateBlogPostCommand,
    GenerateRssFeed,
    GetBlogPost,
    ListBlogPosts,
    ListBlogPostsQuery,
    PublishBlogPost,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.blog import (
    BlogPost,
    BlogPostAlreadyPublishedError,
    BlogPostNotFoundError,
    DuplicateSlugError,
)

public_router = APIRouter(prefix="/api/v1/blog", tags=["blog"])
admin_router = APIRouter(prefix="/api/v1/admin/blog", tags=["blog-admin"])


# Dependency stubs — overridden in main.py.
async def get_list_posts_uc() -> ListBlogPosts:  # pragma: no cover - override target
    raise NotImplementedError


async def get_post_uc() -> GetBlogPost:  # pragma: no cover - override target
    raise NotImplementedError


async def get_create_post_uc() -> CreateBlogPost:  # pragma: no cover - override target
    raise NotImplementedError


async def get_publish_post_uc() -> PublishBlogPost:  # pragma: no cover - override target
    raise NotImplementedError


async def get_rss_uc() -> GenerateRssFeed:  # pragma: no cover - override target
    raise NotImplementedError


def _viewer_can_see_drafts(request: Request) -> bool:
    """True iff the request's principal carries the ``editor`` scope.

    Used by public endpoints to permit drafts when an editor is calling
    (so the editor sees their own work-in-progress) while staying 404
    for everyone else.
    """
    principal = getattr(request.state, "principal", None)
    return isinstance(principal, UserPrincipal) and EDITOR_SCOPE in principal.scopes


def _summary(post: BlogPost) -> BlogPostSummaryResponse:
    return BlogPostSummaryResponse(
        id=post.id,
        slug=post.slug,
        title=post.title,
        excerpt=post.excerpt,
        category_slug=post.category_slug,
        tags=list(post.tags),
        status=post.status.value,
        created_at=post.created_at,
        published_at=post.published_at,
    )


def _detail(post: BlogPost) -> BlogPostDetailResponse:
    return BlogPostDetailResponse(
        **_summary(post).model_dump(by_alias=False),
        body_md=post.body_md,
    )


# ── Public reads ─────────────────────────────────────────────────────


@public_router.get(
    "/posts",
    response_model=BlogPostListResponse,
    response_model_by_alias=True,
)
async def list_blog_posts(
    request: Request,
    use_case: Annotated[ListBlogPosts, Depends(get_list_posts_uc)],
    category: str | None = None,
    tag: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> BlogPostListResponse:
    posts, total = await use_case.execute(
        ListBlogPostsQuery(
            category=category,
            tag=tag,
            include_drafts=_viewer_can_see_drafts(request),
            page=page,
            page_size=page_size,
        )
    )
    return BlogPostListResponse(
        items=[_summary(p) for p in posts],
        total=total,
        page=page,
        page_size=page_size,
    )


@public_router.get(
    "/posts/{slug}",
    response_model=BlogPostDetailResponse,
    response_model_by_alias=True,
)
async def get_blog_post(
    slug: str,
    request: Request,
    use_case: Annotated[GetBlogPost, Depends(get_post_uc)],
) -> BlogPostDetailResponse:
    try:
        post = await use_case.execute(slug, include_drafts=_viewer_can_see_drafts(request))
    except BlogPostNotFoundError as exc:
        raise HTTPException(status_code=404, detail="post not found") from exc
    return _detail(post)


@public_router.get(
    "/rss.xml",
    response_class=Response,
    responses={200: {"content": {"application/rss+xml": {}}}},
)
async def blog_rss(
    use_case: Annotated[GenerateRssFeed, Depends(get_rss_uc)],
) -> Response:
    xml = await use_case.execute()
    return Response(content=xml, media_type="application/rss+xml; charset=utf-8")


# ── Admin writes ─────────────────────────────────────────────────────


@admin_router.post(
    "/posts",
    response_model=BlogPostDetailResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def create_blog_post(
    body: CreateBlogPostRequest,
    use_case: Annotated[CreateBlogPost, Depends(get_create_post_uc)],
    principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> BlogPostDetailResponse:
    try:
        post = await use_case.execute(
            CreateBlogPostCommand(
                title=body.title,
                body_md=body.body_md,
                excerpt=body.excerpt,
                slug=body.slug,
                category_slug=body.category_slug,
                author_user_id=principal.user_id,
                tags=tuple(body.tags),
            )
        )
    except DuplicateSlugError as exc:
        raise HTTPException(status_code=409, detail=f"slug already exists: {exc}") from exc
    return _detail(post)


@admin_router.post(
    "/posts/{slug}/publish",
    response_model=BlogPostDetailResponse,
    response_model_by_alias=True,
)
async def publish_blog_post(
    slug: str,
    use_case: Annotated[PublishBlogPost, Depends(get_publish_post_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> BlogPostDetailResponse:
    try:
        post = await use_case.execute(slug)
    except BlogPostNotFoundError as exc:
        raise HTTPException(status_code=404, detail="post not found") from exc
    except BlogPostAlreadyPublishedError as exc:
        raise HTTPException(status_code=409, detail=f"already published: {exc}") from exc
    return _detail(post)


__all__ = ["admin_router", "public_router"]
