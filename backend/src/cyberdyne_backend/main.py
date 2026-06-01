"""ASGI app factory.

The only module allowed to import freely across layers — `import-linter`
ignores violations originating here so the factory can wire adapters
without the hexagonal rules getting in its way.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from cyberdyne_backend import __version__
from cyberdyne_backend.adapters.inbound.api.ai_chat.router import (
    get_history_uc as get_chat_history_uc,
)
from cyberdyne_backend.adapters.inbound.api.ai_chat.router import (
    get_run_turn_uc,
    get_start_session_uc,
)
from cyberdyne_backend.adapters.inbound.api.ai_chat.router import (
    router as chat_router,
)
from cyberdyne_backend.adapters.inbound.api.blog.router import (
    admin_router as blog_admin_router,
)
from cyberdyne_backend.adapters.inbound.api.blog.router import (
    get_create_post_uc,
    get_list_posts_uc,
    get_post_uc,
    get_publish_post_uc,
    get_rss_uc,
)
from cyberdyne_backend.adapters.inbound.api.blog.router import (
    public_router as blog_public_router,
)
from cyberdyne_backend.adapters.inbound.api.content.router import (
    get_contact_page_uc,
    get_cyberdyne_page_uc,
    get_list_projects_uc,
    get_list_resources_uc,
    get_list_team_uc,
    get_services_page_uc,
)
from cyberdyne_backend.adapters.inbound.api.content.router import (
    router as content_router,
)
from cyberdyne_backend.adapters.inbound.api.courses.router import (
    admin_router as courses_admin_router,
)
from cyberdyne_backend.adapters.inbound.api.courses.router import (
    get_add_lesson_uc,
    get_course_uc,
    get_create_course_uc,
    get_delete_course_uc,
    get_delete_lesson_uc,
    get_list_courses_uc,
    get_reorder_courses_uc,
    get_reorder_lessons_uc,
    get_set_published_uc,
    get_update_course_uc,
    get_update_lesson_uc,
)
from cyberdyne_backend.adapters.inbound.api.courses.router import (
    public_router as courses_public_router,
)
from cyberdyne_backend.adapters.inbound.api.dao.router import (
    get_dao_overview_uc,
)
from cyberdyne_backend.adapters.inbound.api.dao.router import (
    router as dao_router,
)
from cyberdyne_backend.adapters.inbound.api.leads.router import (
    admin_router as leads_admin_router,
)
from cyberdyne_backend.adapters.inbound.api.leads.router import (
    get_admin_list_asks_uc,
    get_admin_update_ask_uc,
    get_create_ask_uc,
)
from cyberdyne_backend.adapters.inbound.api.leads.router import (
    public_router as leads_public_router,
)
from cyberdyne_backend.adapters.inbound.api.learning.router import (
    admin_router as learning_admin_router,
)
from cyberdyne_backend.adapters.inbound.api.learning.router import (
    get_eligibility_uc,
    get_enroll_uc,
    get_issue_certificate_uc,
    get_list_modules_uc,
    get_list_paths_uc,
    get_my_state_uc,
    get_path_gating_uc,
    get_update_progress_uc,
)
from cyberdyne_backend.adapters.inbound.api.learning.router import (
    public_router as learning_public_router,
)
from cyberdyne_backend.adapters.inbound.api.marketplace.router import (
    admin_router as marketplace_admin_router,
)
from cyberdyne_backend.adapters.inbound.api.marketplace.router import (
    get_create_checkout_uc,
    get_handle_webhook_uc,
    get_list_products_uc,
    get_my_licenses_uc,
    get_my_orders_uc,
    get_revoke_license_uc,
    get_webhook_verifier,
)
from cyberdyne_backend.adapters.inbound.api.marketplace.router import (
    me_router as marketplace_me_router,
)
from cyberdyne_backend.adapters.inbound.api.marketplace.router import (
    public_router as marketplace_public_router,
)
from cyberdyne_backend.adapters.inbound.api.marketplace.router import (
    webhook_router as marketplace_webhook_router,
)
from cyberdyne_backend.adapters.inbound.api.quizzes.router import (
    admin_router as quizzes_admin_router,
)
from cyberdyne_backend.adapters.inbound.api.quizzes.router import (
    get_delete_quiz_uc,
    get_list_attempts_uc,
    get_quiz_uc,
    get_submit_attempt_uc,
    get_upsert_quiz_uc,
)
from cyberdyne_backend.adapters.inbound.api.quizzes.router import (
    player_router as quizzes_player_router,
)
from cyberdyne_backend.adapters.inbound.api.uploads.router import (
    admin_router as uploads_admin_router,
)
from cyberdyne_backend.adapters.inbound.api.uploads.router import (
    get_save_upload_uc,
    get_save_uploads_uc,
    get_upload_uc,
)
from cyberdyne_backend.adapters.inbound.api.uploads.router import (
    public_router as uploads_public_router,
)
from cyberdyne_backend.adapters.inbound.health.router import router as health_router
from cyberdyne_backend.adapters.inbound.middleware.auth import AuthMiddleware, extract_token
from cyberdyne_backend.adapters.outbound.persistence.ai_chat.repository import (
    SqlAlchemyChatRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.blog.repository import (
    SqlAlchemyBlogRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.content.repository import (
    SqlAlchemyContentRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.courses.repository import (
    SqlAlchemyCourseRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.leads.repository import (
    SqlAlchemyAskRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.learning.repository import (
    SqlAlchemyLearningRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.marketplace.repository import (
    SqlAlchemyMarketplaceRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.quizzes.repository import (
    SqlAlchemyQuizRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.uploads.repository import (
    SqlAlchemyUploadRepository,
)
from cyberdyne_backend.adapters.outbound.storage.local import LocalFileStorage
from cyberdyne_backend.application.ai_chat import (
    GetChatHistory,
    RunChatTurn,
    StartChatSession,
    ToolContext,
    ToolDispatcher,
)
from cyberdyne_backend.application.blog import (
    CreateBlogPost,
    GenerateRssFeed,
    GetBlogPost,
    ListBlogPosts,
    PublishBlogPost,
)
from cyberdyne_backend.application.content.use_cases import (
    GetContactPage,
    GetCyberdynePage,
    GetServicesPage,
    ListProjects,
    ListResourceGroups,
    ListTeam,
)
from cyberdyne_backend.application.courses import (
    AddLesson,
    CreateCourse,
    DeleteCourse,
    DeleteLesson,
    GetCourse,
    ListCourses,
    ReorderCourses,
    ReorderLessons,
    SetCoursePublished,
    UpdateCourse,
    UpdateLesson,
)
from cyberdyne_backend.application.dao_treasury import GetDaoOverview
from cyberdyne_backend.application.leads import (
    AdminListAsks,
    AdminUpdateAsk,
    CreateAsk,
)
from cyberdyne_backend.application.learning import (
    CheckEnrollmentEligibility,
    EnrollInPath,
    GetMyLearningState,
    GetPathGating,
    IssueCertificate,
    ListModules,
    ListPaths,
    UpdateModuleProgress,
)
from cyberdyne_backend.application.marketplace import (
    CreateCheckoutSession,
    HandleStripeWebhook,
    ListMyLicenses,
    ListMyOrders,
    RevokeLicense,
)
from cyberdyne_backend.application.marketplace import (
    ListProducts as ListMarketplaceProducts,
)
from cyberdyne_backend.application.marketplace.use_cases import GetProduct
from cyberdyne_backend.application.quizzes import (
    DeleteQuiz,
    GetQuiz,
    ListMyAttempts,
    SubmitQuizAttempt,
    UpsertQuiz,
)
from cyberdyne_backend.application.uploads import (
    GetUpload,
    SaveUpload,
    SaveUploads,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal, UserProfile
from cyberdyne_backend.infrastructure.container import Container
from cyberdyne_backend.infrastructure.database.engine import (
    dispose_engine,
    session_scope,
)
from cyberdyne_backend.infrastructure.logging import configure_logging
from cyberdyne_backend.infrastructure.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)
    container = Container(settings)
    # Shared file-storage adapter (creates the media root if missing).
    file_storage = LocalFileStorage(settings.media_root)

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
        # Phase 1's public endpoints don't make outbound CyberdyneAuth-
        # authed calls, so we don't start the service-token provider
        # here. Phase 6 will: ``await container.service_token_provider.start()``.
        try:
            yield
        finally:
            await container.aclose()
            await dispose_engine()

    app = FastAPI(
        title="Cyberdyne Backend",
        version=__version__,
        description="Hexagonal FastAPI service backing the Cyberdyne SvelteKit frontend.",
        # Expose docs/openapi at default paths outside of prod.
        # /docs + /openapi.json are public on every environment — this is a
        # marketing + DAO surface where the API is consumed by our own
        # frontend, the chat agent, and partner integrations. Hiding the
        # schema in prod buys nothing.
        docs_url="/docs",
        redoc_url=None,
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # CORS must be installed before the auth middleware so the preflight
    # OPTIONS requests don't go through token introspection.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )

    app.add_middleware(AuthMiddleware, auth_port=container.auth_port)

    # Per-request use-case wiring. The session lifecycle is owned by
    # ``session_scope``: commits on clean exit, rolls back on raise.
    async def _list_team_dep() -> AsyncIterator[ListTeam]:
        async with session_scope() as session:
            yield ListTeam(repo=SqlAlchemyContentRepository(session))

    async def _cyberdyne_page_dep() -> AsyncIterator[GetCyberdynePage]:
        async with session_scope() as session:
            yield GetCyberdynePage(repo=SqlAlchemyContentRepository(session))

    async def _list_projects_dep() -> AsyncIterator[ListProjects]:
        async with session_scope() as session:
            yield ListProjects(repo=SqlAlchemyContentRepository(session))

    async def _services_page_dep() -> AsyncIterator[GetServicesPage]:
        async with session_scope() as session:
            yield GetServicesPage(repo=SqlAlchemyContentRepository(session))

    async def _contact_page_dep() -> AsyncIterator[GetContactPage]:
        async with session_scope() as session:
            yield GetContactPage(repo=SqlAlchemyContentRepository(session))

    async def _list_resources_dep() -> AsyncIterator[ListResourceGroups]:
        async with session_scope() as session:
            yield ListResourceGroups(repo=SqlAlchemyContentRepository(session))

    async def _create_ask_dep() -> AsyncIterator[CreateAsk]:
        async with session_scope() as session:
            yield CreateAsk(
                repo=SqlAlchemyAskRepository(session),
                captcha=container.captcha_port,
                notifier=container.email_notifier,
            )

    async def _admin_list_asks_dep() -> AsyncIterator[AdminListAsks]:
        async with session_scope() as session:
            yield AdminListAsks(repo=SqlAlchemyAskRepository(session))

    async def _admin_update_ask_dep() -> AsyncIterator[AdminUpdateAsk]:
        async with session_scope() as session:
            yield AdminUpdateAsk(repo=SqlAlchemyAskRepository(session))

    async def _list_blog_posts_dep() -> AsyncIterator[ListBlogPosts]:
        async with session_scope() as session:
            yield ListBlogPosts(repo=SqlAlchemyBlogRepository(session))

    async def _get_blog_post_dep() -> AsyncIterator[GetBlogPost]:
        async with session_scope() as session:
            yield GetBlogPost(repo=SqlAlchemyBlogRepository(session))

    async def _create_blog_post_dep() -> AsyncIterator[CreateBlogPost]:
        async with session_scope() as session:
            yield CreateBlogPost(repo=SqlAlchemyBlogRepository(session))

    async def _publish_blog_post_dep() -> AsyncIterator[PublishBlogPost]:
        async with session_scope() as session:
            yield PublishBlogPost(repo=SqlAlchemyBlogRepository(session))

    async def _rss_feed_dep() -> AsyncIterator[GenerateRssFeed]:
        async with session_scope() as session:
            yield GenerateRssFeed(
                repo=SqlAlchemyBlogRepository(session),
                site_url=settings.public_site_url,
            )

    async def _list_courses_dep() -> AsyncIterator[ListCourses]:
        async with session_scope() as session:
            yield ListCourses(repo=SqlAlchemyCourseRepository(session))

    async def _get_course_dep() -> AsyncIterator[GetCourse]:
        async with session_scope() as session:
            yield GetCourse(repo=SqlAlchemyCourseRepository(session))

    async def _create_course_dep() -> AsyncIterator[CreateCourse]:
        async with session_scope() as session:
            yield CreateCourse(repo=SqlAlchemyCourseRepository(session))

    async def _update_course_dep() -> AsyncIterator[UpdateCourse]:
        async with session_scope() as session:
            yield UpdateCourse(repo=SqlAlchemyCourseRepository(session))

    async def _set_published_dep() -> AsyncIterator[SetCoursePublished]:
        async with session_scope() as session:
            yield SetCoursePublished(repo=SqlAlchemyCourseRepository(session))

    async def _delete_course_dep() -> AsyncIterator[DeleteCourse]:
        async with session_scope() as session:
            yield DeleteCourse(repo=SqlAlchemyCourseRepository(session))

    async def _reorder_courses_dep() -> AsyncIterator[ReorderCourses]:
        async with session_scope() as session:
            yield ReorderCourses(repo=SqlAlchemyCourseRepository(session))

    async def _add_lesson_dep() -> AsyncIterator[AddLesson]:
        async with session_scope() as session:
            yield AddLesson(repo=SqlAlchemyCourseRepository(session))

    async def _update_lesson_dep() -> AsyncIterator[UpdateLesson]:
        async with session_scope() as session:
            yield UpdateLesson(repo=SqlAlchemyCourseRepository(session))

    async def _delete_lesson_dep() -> AsyncIterator[DeleteLesson]:
        async with session_scope() as session:
            yield DeleteLesson(repo=SqlAlchemyCourseRepository(session))

    async def _reorder_lessons_dep() -> AsyncIterator[ReorderLessons]:
        async with session_scope() as session:
            yield ReorderLessons(repo=SqlAlchemyCourseRepository(session))

    async def _get_quiz_dep() -> AsyncIterator[GetQuiz]:
        async with session_scope() as session:
            yield GetQuiz(repo=SqlAlchemyQuizRepository(session))

    async def _upsert_quiz_dep() -> AsyncIterator[UpsertQuiz]:
        async with session_scope() as session:
            yield UpsertQuiz(repo=SqlAlchemyQuizRepository(session))

    async def _delete_quiz_dep() -> AsyncIterator[DeleteQuiz]:
        async with session_scope() as session:
            yield DeleteQuiz(repo=SqlAlchemyQuizRepository(session))

    async def _submit_attempt_dep() -> AsyncIterator[SubmitQuizAttempt]:
        async with session_scope() as session:
            yield SubmitQuizAttempt(repo=SqlAlchemyQuizRepository(session))

    async def _list_attempts_dep() -> AsyncIterator[ListMyAttempts]:
        async with session_scope() as session:
            yield ListMyAttempts(repo=SqlAlchemyQuizRepository(session))

    async def _save_upload_dep() -> AsyncIterator[SaveUpload]:
        async with session_scope() as session:
            yield SaveUpload(
                repo=SqlAlchemyUploadRepository(session),
                storage=file_storage,
                media_url_prefix=settings.media_url_prefix,
            )

    async def _save_uploads_dep() -> AsyncIterator[SaveUploads]:
        async with session_scope() as session:
            yield SaveUploads(
                inner=SaveUpload(
                    repo=SqlAlchemyUploadRepository(session),
                    storage=file_storage,
                    media_url_prefix=settings.media_url_prefix,
                )
            )

    async def _get_upload_dep() -> AsyncIterator[GetUpload]:
        async with session_scope() as session:
            yield GetUpload(repo=SqlAlchemyUploadRepository(session))

    async def _list_modules_dep() -> AsyncIterator[ListModules]:
        async with session_scope() as session:
            yield ListModules(repo=SqlAlchemyLearningRepository(session))

    async def _list_paths_dep() -> AsyncIterator[ListPaths]:
        async with session_scope() as session:
            yield ListPaths(repo=SqlAlchemyLearningRepository(session))

    async def _enroll_dep() -> AsyncIterator[EnrollInPath]:
        async with session_scope() as session:
            yield EnrollInPath(repo=SqlAlchemyLearningRepository(session))

    async def _update_progress_dep() -> AsyncIterator[UpdateModuleProgress]:
        async with session_scope() as session:
            yield UpdateModuleProgress(repo=SqlAlchemyLearningRepository(session))

    async def _my_state_dep() -> AsyncIterator[GetMyLearningState]:
        async with session_scope() as session:
            yield GetMyLearningState(repo=SqlAlchemyLearningRepository(session))

    async def _path_gating_dep() -> AsyncIterator[GetPathGating]:
        async with session_scope() as session:
            yield GetPathGating(repo=SqlAlchemyLearningRepository(session))

    async def _eligibility_dep() -> AsyncIterator[CheckEnrollmentEligibility]:
        async with session_scope() as session:
            yield CheckEnrollmentEligibility(repo=SqlAlchemyLearningRepository(session))

    async def _issue_certificate_dep() -> AsyncIterator[IssueCertificate]:
        async with session_scope() as session:
            yield IssueCertificate(
                repo=SqlAlchemyLearningRepository(session),
                signer=container.certificate_signer,
            )

    async def _dao_overview_dep() -> AsyncIterator[GetDaoOverview]:
        # No DB session needed — chain reads are HTTP-only.
        yield GetDaoOverview(
            reader=container.chain_reader,
            treasury_address=settings.dao_treasury_address,
            holders=settings.dao_holders_count,
        )

    async def _list_marketplace_products_dep() -> AsyncIterator[ListMarketplaceProducts]:
        async with session_scope() as session:
            yield ListMarketplaceProducts(repo=SqlAlchemyMarketplaceRepository(session))

    async def _create_checkout_dep() -> AsyncIterator[CreateCheckoutSession]:
        async with session_scope() as session:
            yield CreateCheckoutSession(
                repo=SqlAlchemyMarketplaceRepository(session),
                checkout=container.stripe_checkout,
                success_url=settings.stripe_success_url,
                cancel_url=settings.stripe_cancel_url,
            )

    async def _handle_webhook_dep() -> AsyncIterator[HandleStripeWebhook]:
        async with session_scope() as session:
            yield HandleStripeWebhook(
                marketplace=SqlAlchemyMarketplaceRepository(session),
                learning=SqlAlchemyLearningRepository(session),
                email_notifier=container.license_email_notifier,
            )

    async def _my_orders_dep() -> AsyncIterator[ListMyOrders]:
        async with session_scope() as session:
            yield ListMyOrders(repo=SqlAlchemyMarketplaceRepository(session))

    async def _my_licenses_dep() -> AsyncIterator[ListMyLicenses]:
        async with session_scope() as session:
            yield ListMyLicenses(repo=SqlAlchemyMarketplaceRepository(session))

    async def _revoke_license_dep() -> AsyncIterator[RevokeLicense]:
        async with session_scope() as session:
            yield RevokeLicense(repo=SqlAlchemyMarketplaceRepository(session))

    def _webhook_verifier_dep() -> object:
        return container.stripe_webhook_verifier

    async def _start_session_dep() -> AsyncIterator[StartChatSession]:
        async with session_scope() as session:
            yield StartChatSession(repo=SqlAlchemyChatRepository(session))

    async def _chat_history_dep() -> AsyncIterator[GetChatHistory]:
        async with session_scope() as session:
            yield GetChatHistory(repo=SqlAlchemyChatRepository(session))

    async def _run_turn_dep(request: Request) -> AsyncIterator[RunChatTurn]:
        # Best-effort profile enrichment: if the caller is a signed-in
        # user, fetch their /users/me so the agent can personalize and
        # pre-fill leads. Service tokens / anonymous / upstream errors
        # all resolve to None and the turn runs un-personalized.
        principal = getattr(request.state, "principal", None)
        profile: UserProfile | None = None
        if isinstance(principal, UserPrincipal):
            token = extract_token(request)
            if token:
                profile = await container.user_profile_port.get_profile(token)
        async with session_scope() as session:
            chat_repo = SqlAlchemyChatRepository(session)
            learning_repo = SqlAlchemyLearningRepository(session)
            blog_repo = SqlAlchemyBlogRepository(session)
            tools_ctx = ToolContext(
                list_projects=ListProjects(repo=SqlAlchemyContentRepository(session)),
                list_paths=ListPaths(repo=learning_repo),
                get_product=GetProduct(repo=SqlAlchemyMarketplaceRepository(session)),
                learning_repo=learning_repo,
                knowledge=container.knowledge_search,
                ask_repo=SqlAlchemyAskRepository(session),
                captcha=container.captcha_port,
                ask_notifier=container.email_notifier,
                user=profile,
                matlab=container.matlab,
                # Forward the user's bearer so the agent's MATLAB calls
                # run in that user's per-session workspace.
                bearer=extract_token(request),
                # A-tools: DAO treasury (HTTP-only), blog (read), and
                # learning actions that run as the signed-in user.
                dao_overview=GetDaoOverview(
                    reader=container.chain_reader,
                    treasury_address=settings.dao_treasury_address,
                    holders=settings.dao_holders_count,
                ),
                list_blog_posts=ListBlogPosts(repo=blog_repo),
                get_blog_post=GetBlogPost(repo=blog_repo),
                enroll_in_path=EnrollInPath(repo=learning_repo),
                get_my_learning=GetMyLearningState(repo=learning_repo),
                update_progress=UpdateModuleProgress(repo=learning_repo),
                user_id=profile.user_id if profile else None,
            )
            yield RunChatTurn(
                repo=chat_repo,
                llm=container.chat_llm,
                dispatcher=ToolDispatcher(tools_ctx),
                user=profile,
            )

    app.dependency_overrides[get_list_team_uc] = _list_team_dep
    app.dependency_overrides[get_cyberdyne_page_uc] = _cyberdyne_page_dep
    app.dependency_overrides[get_list_projects_uc] = _list_projects_dep
    app.dependency_overrides[get_services_page_uc] = _services_page_dep
    app.dependency_overrides[get_contact_page_uc] = _contact_page_dep
    app.dependency_overrides[get_list_resources_uc] = _list_resources_dep
    app.dependency_overrides[get_create_ask_uc] = _create_ask_dep
    app.dependency_overrides[get_admin_list_asks_uc] = _admin_list_asks_dep
    app.dependency_overrides[get_admin_update_ask_uc] = _admin_update_ask_dep
    app.dependency_overrides[get_list_posts_uc] = _list_blog_posts_dep
    app.dependency_overrides[get_post_uc] = _get_blog_post_dep
    app.dependency_overrides[get_create_post_uc] = _create_blog_post_dep
    app.dependency_overrides[get_publish_post_uc] = _publish_blog_post_dep
    app.dependency_overrides[get_rss_uc] = _rss_feed_dep
    app.dependency_overrides[get_list_courses_uc] = _list_courses_dep
    app.dependency_overrides[get_course_uc] = _get_course_dep
    app.dependency_overrides[get_create_course_uc] = _create_course_dep
    app.dependency_overrides[get_update_course_uc] = _update_course_dep
    app.dependency_overrides[get_set_published_uc] = _set_published_dep
    app.dependency_overrides[get_delete_course_uc] = _delete_course_dep
    app.dependency_overrides[get_reorder_courses_uc] = _reorder_courses_dep
    app.dependency_overrides[get_add_lesson_uc] = _add_lesson_dep
    app.dependency_overrides[get_update_lesson_uc] = _update_lesson_dep
    app.dependency_overrides[get_delete_lesson_uc] = _delete_lesson_dep
    app.dependency_overrides[get_reorder_lessons_uc] = _reorder_lessons_dep
    app.dependency_overrides[get_quiz_uc] = _get_quiz_dep
    app.dependency_overrides[get_upsert_quiz_uc] = _upsert_quiz_dep
    app.dependency_overrides[get_delete_quiz_uc] = _delete_quiz_dep
    app.dependency_overrides[get_submit_attempt_uc] = _submit_attempt_dep
    app.dependency_overrides[get_list_attempts_uc] = _list_attempts_dep
    app.dependency_overrides[get_save_upload_uc] = _save_upload_dep
    app.dependency_overrides[get_save_uploads_uc] = _save_uploads_dep
    app.dependency_overrides[get_upload_uc] = _get_upload_dep
    app.dependency_overrides[get_list_modules_uc] = _list_modules_dep
    app.dependency_overrides[get_list_paths_uc] = _list_paths_dep
    app.dependency_overrides[get_enroll_uc] = _enroll_dep
    app.dependency_overrides[get_update_progress_uc] = _update_progress_dep
    app.dependency_overrides[get_my_state_uc] = _my_state_dep
    app.dependency_overrides[get_path_gating_uc] = _path_gating_dep
    app.dependency_overrides[get_eligibility_uc] = _eligibility_dep
    app.dependency_overrides[get_issue_certificate_uc] = _issue_certificate_dep
    app.dependency_overrides[get_dao_overview_uc] = _dao_overview_dep
    app.dependency_overrides[get_list_products_uc] = _list_marketplace_products_dep
    app.dependency_overrides[get_create_checkout_uc] = _create_checkout_dep
    app.dependency_overrides[get_handle_webhook_uc] = _handle_webhook_dep
    app.dependency_overrides[get_my_orders_uc] = _my_orders_dep
    app.dependency_overrides[get_my_licenses_uc] = _my_licenses_dep
    app.dependency_overrides[get_revoke_license_uc] = _revoke_license_dep
    app.dependency_overrides[get_webhook_verifier] = _webhook_verifier_dep
    app.dependency_overrides[get_start_session_uc] = _start_session_dep
    app.dependency_overrides[get_chat_history_uc] = _chat_history_dep
    app.dependency_overrides[get_run_turn_uc] = _run_turn_dep

    app.include_router(health_router)
    app.include_router(content_router)
    app.include_router(leads_public_router)
    app.include_router(leads_admin_router)
    app.include_router(blog_public_router)
    app.include_router(blog_admin_router)
    app.include_router(learning_public_router)
    app.include_router(learning_admin_router)
    app.include_router(courses_public_router)
    app.include_router(courses_admin_router)
    app.include_router(quizzes_player_router)
    app.include_router(quizzes_admin_router)
    app.include_router(uploads_admin_router)
    app.include_router(uploads_public_router)
    # Serve uploaded media read-only. check_dir=False so the mount is
    # valid even before the first upload creates a category subdir.
    app.mount(
        settings.media_url_prefix,
        StaticFiles(directory=settings.media_root, check_dir=False),
        name="media",
    )
    app.include_router(dao_router)
    app.include_router(marketplace_public_router)
    app.include_router(marketplace_me_router)
    app.include_router(marketplace_webhook_router)
    app.include_router(marketplace_admin_router)
    app.include_router(chat_router)
    return app


# Module-level ASGI app for uvicorn (``cyberdyne_backend.main:app``).
app = create_app()


def main() -> None:
    """Entry point used by the project script."""
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "cyberdyne_backend.main:app",
        host="0.0.0.0",  # binding to all interfaces inside a container is intended
        port=settings.port,
        log_level=settings.log_level.lower(),
    )
