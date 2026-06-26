"""ASGI app factory.

The only module allowed to import freely across layers — `import-linter`
ignores violations originating here so the factory can wire adapters
without the hexagonal rules getting in its way.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, suppress
from uuid import UUID

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend import __version__
from cyberdyne_backend.adapters.inbound.api.achievements.router import (
    get_my_achievements_uc,
)
from cyberdyne_backend.adapters.inbound.api.achievements.router import (
    public_router as achievements_public_router,
)
from cyberdyne_backend.adapters.inbound.api.activity.router import (
    get_learner_stats_uc,
    get_record_activity_uc,
)
from cyberdyne_backend.adapters.inbound.api.activity.router import (
    public_router as activity_public_router,
)
from cyberdyne_backend.adapters.inbound.api.ai_chat.router import (
    get_history_uc as get_chat_history_uc,
)
from cyberdyne_backend.adapters.inbound.api.ai_chat.router import (
    get_run_turn_uc,
    get_start_session_uc,
    get_stream_turn_uc,
)
from cyberdyne_backend.adapters.inbound.api.ai_chat.router import (
    router as chat_router,
)
from cyberdyne_backend.adapters.inbound.api.analytics.router import (
    admin_router as analytics_admin_router,
)
from cyberdyne_backend.adapters.inbound.api.analytics.router import (
    get_admin_overview_uc,
    get_learner_dashboard_uc,
)
from cyberdyne_backend.adapters.inbound.api.analytics.router import (
    public_router as analytics_public_router,
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
from cyberdyne_backend.adapters.inbound.api.bookmarks.router import (
    get_add_favorite_uc,
    get_list_favorites_uc,
    get_list_recent_uc,
    get_record_recent_uc,
    get_remove_favorite_uc,
)
from cyberdyne_backend.adapters.inbound.api.bookmarks.router import (
    public_router as bookmarks_public_router,
)
from cyberdyne_backend.adapters.inbound.api.code.router import (
    get_run_code_uc,
)
from cyberdyne_backend.adapters.inbound.api.code.router import (
    player_router as code_player_router,
)
from cyberdyne_backend.adapters.inbound.api.concepts.router import (
    admin_router as concepts_admin_router,
)
from cyberdyne_backend.adapters.inbound.api.concepts.router import (
    get_concept_uc,
    get_create_concept_uc,
    get_delete_concept_uc,
    get_list_concepts_uc,
    get_update_concept_uc,
)
from cyberdyne_backend.adapters.inbound.api.concepts.router import (
    public_router as concepts_public_router,
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
    category_admin_router,
    category_public_router,
    get_add_lesson_uc,
    get_course_languages_uc,
    get_course_uc,
    get_create_category_uc,
    get_create_course_uc,
    get_delete_category_uc,
    get_delete_course_uc,
    get_delete_lesson_uc,
    get_list_categories_uc,
    get_list_courses_uc,
    get_my_course_progress_uc,
    get_my_courses_progress_uc,
    get_reorder_courses_uc,
    get_reorder_lessons_uc,
    get_set_course_category_uc,
    get_set_course_deadline_uc,
    get_set_lesson_progress_uc,
    get_set_published_uc,
    get_translation_job_store,
    get_update_category_uc,
    get_update_course_uc,
    get_update_lesson_uc,
    translation_available,
)
from cyberdyne_backend.adapters.inbound.api.courses.router import (
    get_certificate_pdf_uc as get_course_cert_pdf_uc,
)
from cyberdyne_backend.adapters.inbound.api.courses.router import (
    get_issue_certificate_uc as get_issue_course_cert_uc,
)
from cyberdyne_backend.adapters.inbound.api.courses.router import (
    get_my_certificate_uc as get_my_course_cert_uc,
)
from cyberdyne_backend.adapters.inbound.api.courses.router import (
    get_verify_certificate_uc as get_verify_course_cert_uc,
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
    get_create_module_uc,
    get_create_path_uc,
    get_delete_module_tr_uc,
    get_delete_module_uc,
    get_delete_path_tr_uc,
    get_delete_path_uc,
    get_eligibility_uc,
    get_enroll_uc,
    get_issue_certificate_uc,
    get_list_module_tr_uc,
    get_list_modules_uc,
    get_list_path_tr_uc,
    get_list_paths_uc,
    get_my_deadlines_uc,
    get_my_state_uc,
    get_path_gating_uc,
    get_render_pdf_uc,
    get_reorder_path_modules_uc,
    get_set_deadline_uc,
    get_signing_key_info,
    get_update_module_uc,
    get_update_path_uc,
    get_update_progress_uc,
    get_upsert_module_tr_uc,
    get_upsert_path_tr_uc,
    get_verify_certificate_uc,
)
from cyberdyne_backend.adapters.inbound.api.learning.router import (
    public_router as learning_public_router,
)
from cyberdyne_backend.adapters.inbound.api.learning.schemas import (
    SigningKeyResponse,
)
from cyberdyne_backend.adapters.inbound.api.lesson_notes.router import (
    get_delete_note_uc as get_delete_lesson_note_uc,
)
from cyberdyne_backend.adapters.inbound.api.lesson_notes.router import (
    get_list_lesson_notes_uc,
    get_list_user_notes_uc,
    get_sync_note_uc,
)
from cyberdyne_backend.adapters.inbound.api.lesson_notes.router import (
    get_update_note_uc as get_update_lesson_note_uc,
)
from cyberdyne_backend.adapters.inbound.api.lesson_notes.router import (
    lesson_router as lesson_notes_lesson_router,
)
from cyberdyne_backend.adapters.inbound.api.lesson_notes.router import (
    notes_router as lesson_notes_notes_router,
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
from cyberdyne_backend.adapters.inbound.api.notebook.router import (
    get_add_flashcard_uc,
    get_create_note_uc,
    get_delete_flashcard_uc,
    get_delete_note_uc,
    get_generate_flashcards_uc,
    get_list_flashcards_uc,
    get_list_notes_uc,
    get_note_uc,
    get_review_note_uc,
    get_summarize_note_uc,
    get_update_note_uc,
)
from cyberdyne_backend.adapters.inbound.api.notebook.router import (
    public_router as notebook_public_router,
)
from cyberdyne_backend.adapters.inbound.api.quizzes.router import (
    admin_router as quizzes_admin_router,
)
from cyberdyne_backend.adapters.inbound.api.quizzes.router import (
    catalog_router as quizzes_catalog_router,
)
from cyberdyne_backend.adapters.inbound.api.quizzes.router import (
    get_delete_quiz_uc,
    get_explain_answers_uc,
    get_list_attempts_uc,
    get_list_catalog_uc,
    get_quiz_uc,
    get_submit_attempt_uc,
    get_upsert_quiz_uc,
)
from cyberdyne_backend.adapters.inbound.api.quizzes.router import (
    player_router as quizzes_player_router,
)
from cyberdyne_backend.adapters.inbound.api.recommendations.router import (
    get_recommend_courses_uc,
)
from cyberdyne_backend.adapters.inbound.api.recommendations.router import (
    public_router as recommendations_router,
)
from cyberdyne_backend.adapters.inbound.api.skills.router import (
    get_skill_map_uc,
)
from cyberdyne_backend.adapters.inbound.api.skills.router import (
    public_router as skills_public_router,
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
from cyberdyne_backend.adapters.inbound.api.wallet.router import (
    get_wallet_access_uc,
)
from cyberdyne_backend.adapters.inbound.api.wallet.router import (
    router as wallet_router,
)
from cyberdyne_backend.adapters.inbound.health.router import router as health_router
from cyberdyne_backend.adapters.inbound.middleware.auth import (
    AuthMiddleware,
    extract_token,
    get_user_profile_port,
)
from cyberdyne_backend.adapters.outbound.certificates.signer import (
    Ed25519CertificateSigner,
)
from cyberdyne_backend.adapters.outbound.persistence.academy.job_store import (
    SqlAlchemyTranslationJobStore,
)
from cyberdyne_backend.adapters.outbound.persistence.academy.translation_repository import (
    SqlAlchemyTranslationRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.achievements.metrics_reader import (
    SqlAlchemyAchievementMetricsReader,
)
from cyberdyne_backend.adapters.outbound.persistence.achievements.repository import (
    SqlAlchemyAchievementRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.activity.repository import (
    SqlAlchemyActivityRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.ai_chat.repository import (
    SqlAlchemyChatRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.analytics.repository import (
    SqlAlchemyAnalyticsRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.blog.repository import (
    SqlAlchemyBlogRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.bookmarks.repository import (
    SqlAlchemyBookmarkRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.concepts.repository import (
    SqlAlchemyConceptRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.content.repository import (
    SqlAlchemyContentRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.courses.certificate_repository import (
    SqlAlchemyCourseCertificateRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.courses.progress_repository import (
    SqlAlchemyCourseProgressRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.courses.repository import (
    SqlAlchemyCategoryRepository,
    SqlAlchemyCourseRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.leads.repository import (
    SqlAlchemyAskRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.learning.course_link import (
    SqlAlchemyCourseLinkReader,
)
from cyberdyne_backend.adapters.outbound.persistence.learning.repository import (
    SqlAlchemyLearningRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.lesson_notes.repository import (
    SqlAlchemyLessonNoteRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.marketplace.repository import (
    SqlAlchemyMarketplaceRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.notebook.repository import (
    SqlAlchemyNotebookRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.quizzes.catalog_repository import (
    SqlAlchemyQuizCatalogReader,
)
from cyberdyne_backend.adapters.outbound.persistence.quizzes.repository import (
    SqlAlchemyQuizRepository,
)
from cyberdyne_backend.adapters.outbound.persistence.skills.reader import (
    SqlAlchemySkillMapReader,
)
from cyberdyne_backend.adapters.outbound.persistence.uploads.repository import (
    SqlAlchemyUploadRepository,
)
from cyberdyne_backend.adapters.outbound.storage.local import LocalFileStorage
from cyberdyne_backend.application.academy import (
    GetCourseLanguages,
    MarkdownAwareTranslator,
    TranslateCourse,
    TranslationJob,
    TranslationJobView,
    TranslationWorker,
)
from cyberdyne_backend.application.access import GetWalletAccess
from cyberdyne_backend.application.achievements import GetMyAchievements
from cyberdyne_backend.application.activity import (
    GetLearnerStats,
    RecordActivity,
)
from cyberdyne_backend.application.ai_chat import (
    GetChatHistory,
    RunChatTurn,
    StartChatSession,
    StreamChatTurn,
    ToolContext,
    ToolDispatcher,
)
from cyberdyne_backend.application.analytics import (
    GetAdminOverview,
    GetLearnerDashboard,
)
from cyberdyne_backend.application.blog import (
    CreateBlogPost,
    GenerateRssFeed,
    GetBlogPost,
    ListBlogPosts,
    PublishBlogPost,
)
from cyberdyne_backend.application.bookmarks import (
    AddFavorite,
    ListFavorites,
    ListRecent,
    RecordRecentView,
    RemoveFavorite,
)
from cyberdyne_backend.application.code import RunLessonCode
from cyberdyne_backend.application.concepts import (
    CreateConcept,
    DeleteConcept,
    GetConcept,
    ListConcepts,
    UpdateConcept,
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
    AwardCourseCertificate,
    CourseLessonCompleter,
    CreateCategory,
    CreateCourse,
    DeleteCategory,
    DeleteCourse,
    DeleteLesson,
    GetCourse,
    GetMyCourseCertificate,
    GetMyCourseProgress,
    IssueCourseCertificate,
    ListCategories,
    ListCourses,
    ListMyCourseProgress,
    RenderCourseCertificatePdf,
    ReorderCourses,
    ReorderLessons,
    SetCourseCategory,
    SetCourseDeadline,
    SetCoursePublished,
    SetLessonProgress,
    UpdateCategory,
    UpdateCourse,
    UpdateLesson,
    VerifyCourseCertificate,
)
from cyberdyne_backend.application.dao_treasury import (
    GetDaoOverview,
    TreasurySnapshotPrewarmer,
)
from cyberdyne_backend.application.leads import (
    AdminListAsks,
    AdminUpdateAsk,
    CreateAsk,
)
from cyberdyne_backend.application.learning import (
    CheckEnrollmentEligibility,
    CreateModule,
    CreatePath,
    DeleteModule,
    DeleteModuleTranslation,
    DeletePath,
    DeletePathTranslation,
    EnrollInPath,
    GetMyDeadlines,
    GetMyLearningState,
    GetPathGating,
    IssueCertificate,
    ListModules,
    ListModuleTranslations,
    ListPaths,
    ListPathTranslations,
    RenderCertificatePdf,
    ReorderPathModules,
    SetEnrollmentDeadline,
    UpdateModule,
    UpdateModuleProgress,
    UpdatePath,
    UpsertModuleTranslation,
    UpsertPathTranslation,
    VerifyCertificate,
)
from cyberdyne_backend.application.lesson_notes import (
    DeleteLessonNote,
    ListLessonNotes,
    ListUserNotes,
    SyncLessonNote,
    UpdateLessonNote,
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
from cyberdyne_backend.application.notebook import (
    AddFlashcard,
    CreateNote,
    DeleteFlashcard,
    DeleteNote,
    GenerateFlashcards,
    GetNote,
    ListFlashcards,
    ListNotes,
    ReviewNote,
    SummarizeNote,
    UpdateNote,
)
from cyberdyne_backend.application.quizzes import (
    DeleteQuiz,
    ExplainQuizAnswers,
    GetQuiz,
    ListMyAttempts,
    ListQuizCatalog,
    SubmitQuizAttempt,
    UpsertQuiz,
)
from cyberdyne_backend.application.recommendations import RecommendCourses
from cyberdyne_backend.application.skills import GetSkillMap
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

logger = logging.getLogger("cyberdyne_backend.main")

# Size of the translation-worker pool. Each worker drains the job queue
# independently (claims lock their row), so a backlog (e.g. a catalogue-wide
# re-translation) drains roughly N times faster. Kept modest to bound concurrent
# LLM calls and load on the web process.
_TRANSLATION_WORKERS = 4


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)
    # Production guardrail (issue #7): warn — or hard-fail when
    # ENFORCE_PRODUCTION_ADAPTERS=true — if dev-default mocks are still
    # active in staging/production. Runs only when the serving app is
    # built, never during ``alembic upgrade`` / tooling.
    settings.check_production_adapters(logger)
    container = Container(settings)
    # Shared file-storage adapter (creates the media root if missing).
    file_storage = LocalFileStorage(settings.media_root)

    # ── Durable translation worker ────────────────────────────────────
    # A long-lived task drains the translation-job queue, replacing the old
    # in-process BackgroundTask that a redeploy would kill mid-run. Both the
    # store ops and each job's TranslateCourse get their OWN short-lived
    # session (committed per unit of work), never a request-scoped one.

    class _WorkerJobStore:
        """``TranslationJobStore`` that opens a fresh session per call so the
        worker's claims/marks are each their own committed transaction."""

        async def enqueue(self, course_slug: str, language: str) -> None:
            async with session_scope() as session:
                await SqlAlchemyTranslationJobStore(session).enqueue(course_slug, language)

        async def claim_next(self) -> TranslationJob | None:
            async with session_scope() as session:
                return await SqlAlchemyTranslationJobStore(session).claim_next()

        async def mark_done(self, job_id: UUID) -> None:
            async with session_scope() as session:
                await SqlAlchemyTranslationJobStore(session).mark_done(job_id)

        async def mark_failed(self, job_id: UUID, error: str) -> None:
            async with session_scope() as session:
                await SqlAlchemyTranslationJobStore(session).mark_failed(job_id, error)

        async def requeue_running(self) -> int:
            async with session_scope() as session:
                return await SqlAlchemyTranslationJobStore(session).requeue_running()

        async def list_jobs(self, course_slug: str) -> list[TranslationJobView]:
            async with session_scope() as session:
                return await SqlAlchemyTranslationJobStore(session).list_jobs(course_slug)

    @asynccontextmanager
    async def _translate_course_scope() -> AsyncIterator[TranslateCourse]:
        # One committed session per job, with its own LLM client.
        async with session_scope() as session:
            yield TranslateCourse(
                course_repo=SqlAlchemyCourseRepository(session),
                quiz_repo=SqlAlchemyQuizRepository(session),
                translation_repo=SqlAlchemyTranslationRepository(session),
                translator=MarkdownAwareTranslator(llm=container.chat_llm),
            )

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
        # Phase 1's public endpoints don't make outbound CyberdyneAuth-
        # authed calls, so we don't start the service-token provider
        # here. Phase 6 will: ``await container.service_token_provider.start()``.
        worker_tasks: list[asyncio.Task[None]] = []
        if settings.openai_api_key is not None:
            # Only run workers when translation is actually available (mirrors
            # the translation_available() gate). They requeue any job stranded
            # ``running`` by the last restart, then drain in parallel — each
            # claim_next() locks its row (FOR UPDATE SKIP LOCKED), so a small
            # pool never claims the same job and a backlog drains N times faster.
            for _ in range(_TRANSLATION_WORKERS):
                worker = TranslationWorker(
                    store=_WorkerJobStore(),
                    translate_course_factory=_translate_course_scope,
                )
                worker_tasks.append(asyncio.create_task(worker.run_forever()))
        if settings.dao_snapshot_prewarm and settings.dao_treasury_address:
            # Keep the treasury snapshot cache warm so the DaoView never
            # eats a cold on-chain read. Inert without a treasury address.
            prewarmer = TreasurySnapshotPrewarmer(
                reader=container.chain_reader,
                treasury_address=settings.dao_treasury_address,
                interval_s=settings.dao_snapshot_ttl_s,
            )
            worker_tasks.append(asyncio.create_task(prewarmer.run_forever()))
        try:
            yield
        finally:
            for task in worker_tasks:
                task.cancel()
            for task in worker_tasks:
                with suppress(asyncio.CancelledError):
                    await task
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
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )

    app.add_middleware(AuthMiddleware, auth_port=container.auth_port)

    # Per-request use-case wiring. The session lifecycle is owned by
    # ``session_scope``: commits on clean exit, rolls back on raise.
    async def _list_team_dep() -> AsyncIterator[ListTeam]:
        async with session_scope() as session:
            yield ListTeam(repo=SqlAlchemyContentRepository(session))

    # Concepts library — public browse/search + admin authoring (issue #168).
    async def _list_concepts_dep() -> AsyncIterator[ListConcepts]:
        async with session_scope() as session:
            yield ListConcepts(repo=SqlAlchemyConceptRepository(session))

    async def _get_concept_dep() -> AsyncIterator[GetConcept]:
        async with session_scope() as session:
            yield GetConcept(repo=SqlAlchemyConceptRepository(session))

    async def _create_concept_dep() -> AsyncIterator[CreateConcept]:
        async with session_scope() as session:
            yield CreateConcept(repo=SqlAlchemyConceptRepository(session))

    async def _update_concept_dep() -> AsyncIterator[UpdateConcept]:
        async with session_scope() as session:
            yield UpdateConcept(repo=SqlAlchemyConceptRepository(session))

    async def _delete_concept_dep() -> AsyncIterator[DeleteConcept]:
        async with session_scope() as session:
            yield DeleteConcept(repo=SqlAlchemyConceptRepository(session))

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

    async def _learner_dashboard_dep() -> AsyncIterator[GetLearnerDashboard]:
        async with session_scope() as session:
            yield GetLearnerDashboard(repo=SqlAlchemyAnalyticsRepository(session))

    # Achievements/badges — earned + in-progress (issue #163).
    async def _my_achievements_dep() -> AsyncIterator[GetMyAchievements]:
        async with session_scope() as session:
            yield GetMyAchievements(
                reader=SqlAlchemyAchievementMetricsReader(session),
                repo=SqlAlchemyAchievementRepository(session),
            )

    # Learner activity + derived stats (issue #164).
    async def _record_activity_dep() -> AsyncIterator[RecordActivity]:
        async with session_scope() as session:
            yield RecordActivity(repo=SqlAlchemyActivityRepository(session))

    async def _learner_stats_dep() -> AsyncIterator[GetLearnerStats]:
        async with session_scope() as session:
            yield GetLearnerStats(repo=SqlAlchemyActivityRepository(session))

    async def _admin_overview_dep() -> AsyncIterator[GetAdminOverview]:
        async with session_scope() as session:
            yield GetAdminOverview(repo=SqlAlchemyAnalyticsRepository(session))

    async def _recommend_courses_dep() -> AsyncIterator[RecommendCourses]:
        async with session_scope() as session:
            yield RecommendCourses(
                courses=SqlAlchemyCourseRepository(session),
                analytics=SqlAlchemyAnalyticsRepository(session),
                llm=container.chat_llm,
            )

    # Skill Map — per-domain mastery + weak areas (issue #165).
    async def _skill_map_dep() -> AsyncIterator[GetSkillMap]:
        async with session_scope() as session:
            yield GetSkillMap(reader=SqlAlchemySkillMapReader(session))

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

    async def _list_categories_dep() -> AsyncIterator[ListCategories]:
        async with session_scope() as session:
            yield ListCategories(repo=SqlAlchemyCategoryRepository(session))

    async def _create_category_dep() -> AsyncIterator[CreateCategory]:
        async with session_scope() as session:
            yield CreateCategory(repo=SqlAlchemyCategoryRepository(session))

    async def _delete_category_dep() -> AsyncIterator[DeleteCategory]:
        async with session_scope() as session:
            yield DeleteCategory(repo=SqlAlchemyCategoryRepository(session))

    async def _update_category_dep() -> AsyncIterator[UpdateCategory]:
        async with session_scope() as session:
            yield UpdateCategory(repo=SqlAlchemyCategoryRepository(session))

    async def _set_course_category_dep() -> AsyncIterator[SetCourseCategory]:
        async with session_scope() as session:
            yield SetCourseCategory(
                course_repo=SqlAlchemyCourseRepository(session),
                category_repo=SqlAlchemyCategoryRepository(session),
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

    async def _set_course_deadline_dep() -> AsyncIterator[SetCourseDeadline]:
        async with session_scope() as session:
            yield SetCourseDeadline(repo=SqlAlchemyCourseRepository(session))

    async def _issue_course_cert_dep() -> AsyncIterator[IssueCourseCertificate]:
        async with session_scope() as session:
            yield IssueCourseCertificate(
                courses=SqlAlchemyCourseRepository(session),
                progress=SqlAlchemyCourseProgressRepository(session),
                certificates=SqlAlchemyCourseCertificateRepository(session),
                signer=container.certificate_signer,
            )

    async def _my_course_cert_dep() -> AsyncIterator[GetMyCourseCertificate]:
        async with session_scope() as session:
            yield GetMyCourseCertificate(
                certificates=SqlAlchemyCourseCertificateRepository(session)
            )

    async def _verify_course_cert_dep() -> AsyncIterator[VerifyCourseCertificate]:
        async with session_scope() as session:
            yield VerifyCourseCertificate(
                certificates=SqlAlchemyCourseCertificateRepository(session),
                signer=container.certificate_signer,
            )

    async def _course_cert_pdf_dep() -> AsyncIterator[RenderCourseCertificatePdf]:
        async with session_scope() as session:
            yield RenderCourseCertificatePdf(
                certificates=SqlAlchemyCourseCertificateRepository(session),
                courses=SqlAlchemyCourseRepository(session),
                renderer=container.certificate_pdf_renderer,
                verify_url_base=settings.public_site_url,
            )

    async def _delete_course_dep() -> AsyncIterator[DeleteCourse]:
        async with session_scope() as session:
            yield DeleteCourse(repo=SqlAlchemyCourseRepository(session))

    async def _course_languages_dep() -> AsyncIterator[GetCourseLanguages]:
        async with session_scope() as session:
            yield GetCourseLanguages(
                course_repo=SqlAlchemyCourseRepository(session),
                quiz_repo=SqlAlchemyQuizRepository(session),
                translation_repo=SqlAlchemyTranslationRepository(session),
            )

    def _translation_available_dep() -> bool:
        return settings.openai_api_key is not None

    async def _translation_job_store_dep() -> AsyncIterator[SqlAlchemyTranslationJobStore]:
        async with session_scope() as session:
            yield SqlAlchemyTranslationJobStore(session)

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

    async def _set_lesson_progress_dep() -> AsyncIterator[SetLessonProgress]:
        async with session_scope() as session:
            yield SetLessonProgress(
                courses=SqlAlchemyCourseRepository(session),
                progress=SqlAlchemyCourseProgressRepository(session),
                awarder=AwardCourseCertificate(
                    courses=SqlAlchemyCourseRepository(session),
                    progress=SqlAlchemyCourseProgressRepository(session),
                    certificates=SqlAlchemyCourseCertificateRepository(session),
                    signer=container.certificate_signer,
                ),
            )

    async def _my_course_progress_dep() -> AsyncIterator[GetMyCourseProgress]:
        async with session_scope() as session:
            yield GetMyCourseProgress(
                courses=SqlAlchemyCourseRepository(session),
                progress=SqlAlchemyCourseProgressRepository(session),
            )

    async def _my_courses_progress_dep() -> AsyncIterator[ListMyCourseProgress]:
        async with session_scope() as session:
            yield ListMyCourseProgress(
                courses=SqlAlchemyCourseRepository(session),
                progress=SqlAlchemyCourseProgressRepository(session),
            )

    async def _get_quiz_dep() -> AsyncIterator[GetQuiz]:
        async with session_scope() as session:
            yield GetQuiz(repo=SqlAlchemyQuizRepository(session))

    # Notebook notes CRUD (issue #161).
    async def _create_note_dep() -> AsyncIterator[CreateNote]:
        async with session_scope() as session:
            yield CreateNote(repo=SqlAlchemyNotebookRepository(session))

    async def _list_notes_dep() -> AsyncIterator[ListNotes]:
        async with session_scope() as session:
            yield ListNotes(repo=SqlAlchemyNotebookRepository(session))

    async def _get_note_dep() -> AsyncIterator[GetNote]:
        async with session_scope() as session:
            yield GetNote(repo=SqlAlchemyNotebookRepository(session))

    async def _update_note_dep() -> AsyncIterator[UpdateNote]:
        async with session_scope() as session:
            yield UpdateNote(repo=SqlAlchemyNotebookRepository(session))

    async def _delete_note_dep() -> AsyncIterator[DeleteNote]:
        async with session_scope() as session:
            yield DeleteNote(repo=SqlAlchemyNotebookRepository(session))

    # Notebook flashcards (issue #161, part 2).
    async def _add_flashcard_dep() -> AsyncIterator[AddFlashcard]:
        async with session_scope() as session:
            yield AddFlashcard(repo=SqlAlchemyNotebookRepository(session))

    async def _list_flashcards_dep() -> AsyncIterator[ListFlashcards]:
        async with session_scope() as session:
            yield ListFlashcards(repo=SqlAlchemyNotebookRepository(session))

    async def _delete_flashcard_dep() -> AsyncIterator[DeleteFlashcard]:
        async with session_scope() as session:
            yield DeleteFlashcard(repo=SqlAlchemyNotebookRepository(session))

    async def _review_note_dep() -> AsyncIterator[ReviewNote]:
        async with session_scope() as session:
            yield ReviewNote(repo=SqlAlchemyNotebookRepository(session))

    # Notebook AI generation (issue #187) — reuse the chat LLM client.
    async def _generate_flashcards_dep() -> AsyncIterator[GenerateFlashcards]:
        async with session_scope() as session:
            yield GenerateFlashcards(
                repo=SqlAlchemyNotebookRepository(session),
                llm=container.chat_llm,
            )

    async def _summarize_note_dep() -> AsyncIterator[SummarizeNote]:
        async with session_scope() as session:
            yield SummarizeNote(
                repo=SqlAlchemyNotebookRepository(session),
                llm=container.chat_llm,
            )

    async def _upsert_quiz_dep() -> AsyncIterator[UpsertQuiz]:
        async with session_scope() as session:
            yield UpsertQuiz(repo=SqlAlchemyQuizRepository(session))

    async def _delete_quiz_dep() -> AsyncIterator[DeleteQuiz]:
        async with session_scope() as session:
            yield DeleteQuiz(repo=SqlAlchemyQuizRepository(session))

    async def _submit_attempt_dep() -> AsyncIterator[SubmitQuizAttempt]:
        async with session_scope() as session:
            yield SubmitQuizAttempt(
                repo=SqlAlchemyQuizRepository(session),
                lesson_completer=CourseLessonCompleter(
                    progress=SqlAlchemyCourseProgressRepository(session),
                    awarder=AwardCourseCertificate(
                        courses=SqlAlchemyCourseRepository(session),
                        progress=SqlAlchemyCourseProgressRepository(session),
                        certificates=SqlAlchemyCourseCertificateRepository(session),
                        signer=container.certificate_signer,
                    ),
                ),
            )

    async def _list_attempts_dep() -> AsyncIterator[ListMyAttempts]:
        async with session_scope() as session:
            yield ListMyAttempts(repo=SqlAlchemyQuizRepository(session))

    async def _list_quiz_catalog_dep() -> AsyncIterator[ListQuizCatalog]:
        async with session_scope() as session:
            yield ListQuizCatalog(reader=SqlAlchemyQuizCatalogReader(session))

    async def _explain_answers_dep() -> AsyncIterator[ExplainQuizAnswers]:
        async with session_scope() as session:
            yield ExplainQuizAnswers(
                repo=SqlAlchemyQuizRepository(session),
                llm=container.chat_llm,
            )

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
            yield ListModules(
                repo=SqlAlchemyLearningRepository(session),
                course_reader=SqlAlchemyCourseLinkReader(
                    SqlAlchemyCourseRepository(session),
                    SqlAlchemyCourseProgressRepository(session),
                ),
            )

    async def _create_module_dep() -> AsyncIterator[CreateModule]:
        async with session_scope() as session:
            yield CreateModule(
                repo=SqlAlchemyLearningRepository(session),
                course_reader=SqlAlchemyCourseLinkReader(
                    SqlAlchemyCourseRepository(session),
                    SqlAlchemyCourseProgressRepository(session),
                ),
            )

    async def _update_module_dep() -> AsyncIterator[UpdateModule]:
        async with session_scope() as session:
            yield UpdateModule(
                repo=SqlAlchemyLearningRepository(session),
                course_reader=SqlAlchemyCourseLinkReader(
                    SqlAlchemyCourseRepository(session),
                    SqlAlchemyCourseProgressRepository(session),
                ),
            )

    async def _delete_module_dep() -> AsyncIterator[DeleteModule]:
        async with session_scope() as session:
            yield DeleteModule(repo=SqlAlchemyLearningRepository(session))

    async def _create_path_dep() -> AsyncIterator[CreatePath]:
        async with session_scope() as session:
            yield CreatePath(repo=SqlAlchemyLearningRepository(session))

    async def _update_path_dep() -> AsyncIterator[UpdatePath]:
        async with session_scope() as session:
            yield UpdatePath(repo=SqlAlchemyLearningRepository(session))

    async def _delete_path_dep() -> AsyncIterator[DeletePath]:
        async with session_scope() as session:
            yield DeletePath(repo=SqlAlchemyLearningRepository(session))

    async def _reorder_path_modules_dep() -> AsyncIterator[ReorderPathModules]:
        async with session_scope() as session:
            yield ReorderPathModules(repo=SqlAlchemyLearningRepository(session))

    async def _list_module_tr_dep() -> AsyncIterator[ListModuleTranslations]:
        async with session_scope() as session:
            yield ListModuleTranslations(repo=SqlAlchemyLearningRepository(session))

    async def _upsert_module_tr_dep() -> AsyncIterator[UpsertModuleTranslation]:
        async with session_scope() as session:
            yield UpsertModuleTranslation(repo=SqlAlchemyLearningRepository(session))

    async def _delete_module_tr_dep() -> AsyncIterator[DeleteModuleTranslation]:
        async with session_scope() as session:
            yield DeleteModuleTranslation(repo=SqlAlchemyLearningRepository(session))

    async def _list_path_tr_dep() -> AsyncIterator[ListPathTranslations]:
        async with session_scope() as session:
            yield ListPathTranslations(repo=SqlAlchemyLearningRepository(session))

    async def _upsert_path_tr_dep() -> AsyncIterator[UpsertPathTranslation]:
        async with session_scope() as session:
            yield UpsertPathTranslation(repo=SqlAlchemyLearningRepository(session))

    async def _delete_path_tr_dep() -> AsyncIterator[DeletePathTranslation]:
        async with session_scope() as session:
            yield DeletePathTranslation(repo=SqlAlchemyLearningRepository(session))

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
            yield GetMyLearningState(
                repo=SqlAlchemyLearningRepository(session),
                course_reader=SqlAlchemyCourseLinkReader(
                    SqlAlchemyCourseRepository(session),
                    SqlAlchemyCourseProgressRepository(session),
                ),
            )

    # Per-user lesson notes (issue #188).
    async def _sync_lesson_note_dep() -> AsyncIterator[SyncLessonNote]:
        async with session_scope() as session:
            yield SyncLessonNote(repo=SqlAlchemyLessonNoteRepository(session))

    async def _list_lesson_notes_dep() -> AsyncIterator[ListLessonNotes]:
        async with session_scope() as session:
            yield ListLessonNotes(repo=SqlAlchemyLessonNoteRepository(session))

    async def _list_user_notes_dep() -> AsyncIterator[ListUserNotes]:
        async with session_scope() as session:
            yield ListUserNotes(repo=SqlAlchemyLessonNoteRepository(session))

    async def _update_lesson_note_dep() -> AsyncIterator[UpdateLessonNote]:
        async with session_scope() as session:
            yield UpdateLessonNote(repo=SqlAlchemyLessonNoteRepository(session))

    async def _delete_lesson_note_dep() -> AsyncIterator[DeleteLessonNote]:
        async with session_scope() as session:
            yield DeleteLessonNote(repo=SqlAlchemyLessonNoteRepository(session))

    # Favorites/bookmarks + recently-viewed (issue #162).
    async def _list_favorites_dep() -> AsyncIterator[ListFavorites]:
        async with session_scope() as session:
            yield ListFavorites(repo=SqlAlchemyBookmarkRepository(session))

    async def _add_favorite_dep() -> AsyncIterator[AddFavorite]:
        async with session_scope() as session:
            yield AddFavorite(repo=SqlAlchemyBookmarkRepository(session))

    async def _remove_favorite_dep() -> AsyncIterator[RemoveFavorite]:
        async with session_scope() as session:
            yield RemoveFavorite(repo=SqlAlchemyBookmarkRepository(session))

    async def _record_recent_dep() -> AsyncIterator[RecordRecentView]:
        async with session_scope() as session:
            yield RecordRecentView(repo=SqlAlchemyBookmarkRepository(session))

    async def _list_recent_dep() -> AsyncIterator[ListRecent]:
        async with session_scope() as session:
            yield ListRecent(repo=SqlAlchemyBookmarkRepository(session))

    async def _path_gating_dep() -> AsyncIterator[GetPathGating]:
        async with session_scope() as session:
            yield GetPathGating(
                repo=SqlAlchemyLearningRepository(session),
                course_reader=SqlAlchemyCourseLinkReader(
                    SqlAlchemyCourseRepository(session),
                    SqlAlchemyCourseProgressRepository(session),
                ),
            )

    async def _eligibility_dep() -> AsyncIterator[CheckEnrollmentEligibility]:
        async with session_scope() as session:
            yield CheckEnrollmentEligibility(
                repo=SqlAlchemyLearningRepository(session),
                course_reader=SqlAlchemyCourseLinkReader(
                    SqlAlchemyCourseRepository(session),
                    SqlAlchemyCourseProgressRepository(session),
                ),
            )

    async def _issue_certificate_dep() -> AsyncIterator[IssueCertificate]:
        async with session_scope() as session:
            yield IssueCertificate(
                repo=SqlAlchemyLearningRepository(session),
                signer=container.certificate_signer,
                course_reader=SqlAlchemyCourseLinkReader(
                    SqlAlchemyCourseRepository(session),
                    SqlAlchemyCourseProgressRepository(session),
                ),
            )

    async def _verify_certificate_dep() -> AsyncIterator[VerifyCertificate]:
        async with session_scope() as session:
            yield VerifyCertificate(
                repo=SqlAlchemyLearningRepository(session),
                signer=container.certificate_signer,
            )

    def _signing_key_info_dep() -> SigningKeyResponse:
        # Publish the verification key: the Ed25519 public key for external
        # verifiers, or just the algorithm (null key) for the HMAC scheme.
        signer = container.certificate_signer
        if isinstance(signer, Ed25519CertificateSigner):
            return SigningKeyResponse(algorithm="ed25519", public_key=signer.public_key_b64)
        return SigningKeyResponse(algorithm="hmac-sha256", public_key=None)

    async def _render_pdf_dep() -> AsyncIterator[RenderCertificatePdf]:
        async with session_scope() as session:
            yield RenderCertificatePdf(
                repo=SqlAlchemyLearningRepository(session),
                renderer=container.certificate_pdf_renderer,
                verify_url_base=settings.public_site_url,
            )

    async def _my_deadlines_dep() -> AsyncIterator[GetMyDeadlines]:
        async with session_scope() as session:
            yield GetMyDeadlines(repo=SqlAlchemyLearningRepository(session))

    async def _set_deadline_dep() -> AsyncIterator[SetEnrollmentDeadline]:
        async with session_scope() as session:
            yield SetEnrollmentDeadline(repo=SqlAlchemyLearningRepository(session))

    async def _dao_overview_dep() -> AsyncIterator[GetDaoOverview]:
        # No DB session needed — chain reads are HTTP-only.
        yield GetDaoOverview(
            reader=container.chain_reader,
            treasury_address=settings.dao_treasury_address,
            holders=settings.dao_holders_count,
        )

    async def _wallet_access_dep() -> AsyncIterator[GetWalletAccess]:
        # No DB session — access reads are chain-only (stub for now).
        yield GetWalletAccess(reader=container.access_reader)

    async def _run_code_dep() -> AsyncIterator[RunLessonCode]:
        # No DB session — execution is HTTP-only against the MATLAB engine
        # (matlab lessons) or the Python interpreter sandbox (python lessons).
        yield RunLessonCode(matlab=container.matlab, python=container.python)

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

    async def _chat_profile(request: Request) -> UserProfile | None:
        # Best-effort profile enrichment: if the caller is a signed-in
        # user, fetch their /users/me so the agent can personalize and
        # pre-fill leads. Service tokens / anonymous / upstream errors
        # all resolve to None and the turn runs un-personalized.
        principal = getattr(request.state, "principal", None)
        if isinstance(principal, UserPrincipal):
            token = extract_token(request)
            if token:
                return await container.user_profile_port.get_profile(token)
        return None

    def _chat_tools_ctx(
        request: Request, session: AsyncSession, profile: UserProfile | None
    ) -> ToolContext:
        learning_repo = SqlAlchemyLearningRepository(session)
        blog_repo = SqlAlchemyBlogRepository(session)
        course_repo = SqlAlchemyCourseRepository(session)
        return ToolContext(
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
            python=container.python,
            cyberflies=container.cyberflies,
            documents=container.document_renderer,
            # Forward the user's bearer so the agent's MATLAB / Python /
            # Cyberflies calls run as (and only see) that user.
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
            # New learning surface so the agent can guide + recommend.
            list_courses=ListCourses(repo=course_repo),
            get_course=GetCourse(repo=course_repo),
            get_my_course_progress=GetMyCourseProgress(
                courses=course_repo,
                progress=SqlAlchemyCourseProgressRepository(session),
            ),
            get_my_deadlines=GetMyDeadlines(repo=learning_repo),
            path_gating=GetPathGating(repo=learning_repo),
            get_quiz=GetQuiz(repo=SqlAlchemyQuizRepository(session)),
            learner_dashboard=GetLearnerDashboard(repo=SqlAlchemyAnalyticsRepository(session)),
            list_user_notes=ListUserNotes(repo=SqlAlchemyLessonNoteRepository(session)),
            list_notebook_notes=ListNotes(repo=SqlAlchemyNotebookRepository(session)),
            list_note_flashcards=ListFlashcards(repo=SqlAlchemyNotebookRepository(session)),
            get_wallet_access=GetWalletAccess(reader=container.access_reader),
            user_id=profile.user_id if profile else None,
        )

    async def _run_turn_dep(request: Request) -> AsyncIterator[RunChatTurn]:
        profile = await _chat_profile(request)
        async with session_scope() as session:
            yield RunChatTurn(
                repo=SqlAlchemyChatRepository(session),
                llm=container.chat_llm,
                dispatcher=ToolDispatcher(_chat_tools_ctx(request, session, profile)),
                user=profile,
            )

    async def _stream_turn_dep(request: Request) -> AsyncIterator[StreamChatTurn]:
        # Same wiring as _run_turn_dep; the session stays open for the whole
        # SSE stream because FastAPI defers yield-dependency cleanup until the
        # StreamingResponse is fully consumed.
        profile = await _chat_profile(request)
        async with session_scope() as session:
            yield StreamChatTurn(
                repo=SqlAlchemyChatRepository(session),
                llm=container.chat_llm,
                dispatcher=ToolDispatcher(_chat_tools_ctx(request, session, profile)),
                user=profile,
            )

    app.dependency_overrides[get_list_team_uc] = _list_team_dep
    app.dependency_overrides[get_list_concepts_uc] = _list_concepts_dep
    app.dependency_overrides[get_concept_uc] = _get_concept_dep
    app.dependency_overrides[get_create_concept_uc] = _create_concept_dep
    app.dependency_overrides[get_update_concept_uc] = _update_concept_dep
    app.dependency_overrides[get_delete_concept_uc] = _delete_concept_dep
    app.dependency_overrides[get_cyberdyne_page_uc] = _cyberdyne_page_dep
    app.dependency_overrides[get_list_projects_uc] = _list_projects_dep
    app.dependency_overrides[get_services_page_uc] = _services_page_dep
    app.dependency_overrides[get_contact_page_uc] = _contact_page_dep
    app.dependency_overrides[get_list_resources_uc] = _list_resources_dep
    app.dependency_overrides[get_create_ask_uc] = _create_ask_dep
    app.dependency_overrides[get_admin_list_asks_uc] = _admin_list_asks_dep
    app.dependency_overrides[get_admin_update_ask_uc] = _admin_update_ask_dep
    app.dependency_overrides[get_learner_dashboard_uc] = _learner_dashboard_dep
    app.dependency_overrides[get_my_achievements_uc] = _my_achievements_dep
    app.dependency_overrides[get_record_activity_uc] = _record_activity_dep
    app.dependency_overrides[get_learner_stats_uc] = _learner_stats_dep
    app.dependency_overrides[get_recommend_courses_uc] = _recommend_courses_dep
    app.dependency_overrides[get_skill_map_uc] = _skill_map_dep
    app.dependency_overrides[get_admin_overview_uc] = _admin_overview_dep
    app.dependency_overrides[get_list_posts_uc] = _list_blog_posts_dep
    app.dependency_overrides[get_post_uc] = _get_blog_post_dep
    app.dependency_overrides[get_create_post_uc] = _create_blog_post_dep
    app.dependency_overrides[get_publish_post_uc] = _publish_blog_post_dep
    app.dependency_overrides[get_rss_uc] = _rss_feed_dep
    app.dependency_overrides[get_list_courses_uc] = _list_courses_dep
    app.dependency_overrides[get_course_uc] = _get_course_dep
    app.dependency_overrides[get_create_course_uc] = _create_course_dep
    app.dependency_overrides[get_update_course_uc] = _update_course_dep
    app.dependency_overrides[get_list_categories_uc] = _list_categories_dep
    app.dependency_overrides[get_create_category_uc] = _create_category_dep
    app.dependency_overrides[get_delete_category_uc] = _delete_category_dep
    app.dependency_overrides[get_update_category_uc] = _update_category_dep
    app.dependency_overrides[get_set_course_category_uc] = _set_course_category_dep
    app.dependency_overrides[get_set_published_uc] = _set_published_dep
    app.dependency_overrides[get_set_course_deadline_uc] = _set_course_deadline_dep
    app.dependency_overrides[get_issue_course_cert_uc] = _issue_course_cert_dep
    app.dependency_overrides[get_my_course_cert_uc] = _my_course_cert_dep
    app.dependency_overrides[get_verify_course_cert_uc] = _verify_course_cert_dep
    app.dependency_overrides[get_course_cert_pdf_uc] = _course_cert_pdf_dep
    app.dependency_overrides[get_delete_course_uc] = _delete_course_dep
    app.dependency_overrides[get_reorder_courses_uc] = _reorder_courses_dep
    app.dependency_overrides[get_course_languages_uc] = _course_languages_dep
    app.dependency_overrides[get_translation_job_store] = _translation_job_store_dep
    app.dependency_overrides[translation_available] = _translation_available_dep
    app.dependency_overrides[get_add_lesson_uc] = _add_lesson_dep
    app.dependency_overrides[get_update_lesson_uc] = _update_lesson_dep
    app.dependency_overrides[get_delete_lesson_uc] = _delete_lesson_dep
    app.dependency_overrides[get_reorder_lessons_uc] = _reorder_lessons_dep
    app.dependency_overrides[get_set_lesson_progress_uc] = _set_lesson_progress_dep
    app.dependency_overrides[get_my_course_progress_uc] = _my_course_progress_dep
    app.dependency_overrides[get_my_courses_progress_uc] = _my_courses_progress_dep
    app.dependency_overrides[get_quiz_uc] = _get_quiz_dep
    app.dependency_overrides[get_create_note_uc] = _create_note_dep
    app.dependency_overrides[get_list_notes_uc] = _list_notes_dep
    app.dependency_overrides[get_note_uc] = _get_note_dep
    app.dependency_overrides[get_update_note_uc] = _update_note_dep
    app.dependency_overrides[get_delete_note_uc] = _delete_note_dep
    app.dependency_overrides[get_add_flashcard_uc] = _add_flashcard_dep
    app.dependency_overrides[get_list_flashcards_uc] = _list_flashcards_dep
    app.dependency_overrides[get_delete_flashcard_uc] = _delete_flashcard_dep
    app.dependency_overrides[get_review_note_uc] = _review_note_dep
    app.dependency_overrides[get_generate_flashcards_uc] = _generate_flashcards_dep
    app.dependency_overrides[get_summarize_note_uc] = _summarize_note_dep
    app.dependency_overrides[get_upsert_quiz_uc] = _upsert_quiz_dep
    app.dependency_overrides[get_delete_quiz_uc] = _delete_quiz_dep
    app.dependency_overrides[get_submit_attempt_uc] = _submit_attempt_dep
    app.dependency_overrides[get_list_attempts_uc] = _list_attempts_dep
    app.dependency_overrides[get_list_catalog_uc] = _list_quiz_catalog_dep
    app.dependency_overrides[get_explain_answers_uc] = _explain_answers_dep
    app.dependency_overrides[get_save_upload_uc] = _save_upload_dep
    app.dependency_overrides[get_save_uploads_uc] = _save_uploads_dep
    app.dependency_overrides[get_upload_uc] = _get_upload_dep
    app.dependency_overrides[get_list_modules_uc] = _list_modules_dep
    app.dependency_overrides[get_list_paths_uc] = _list_paths_dep
    app.dependency_overrides[get_create_module_uc] = _create_module_dep
    app.dependency_overrides[get_update_module_uc] = _update_module_dep
    app.dependency_overrides[get_delete_module_uc] = _delete_module_dep
    app.dependency_overrides[get_create_path_uc] = _create_path_dep
    app.dependency_overrides[get_update_path_uc] = _update_path_dep
    app.dependency_overrides[get_delete_path_uc] = _delete_path_dep
    app.dependency_overrides[get_reorder_path_modules_uc] = _reorder_path_modules_dep
    app.dependency_overrides[get_list_module_tr_uc] = _list_module_tr_dep
    app.dependency_overrides[get_upsert_module_tr_uc] = _upsert_module_tr_dep
    app.dependency_overrides[get_delete_module_tr_uc] = _delete_module_tr_dep
    app.dependency_overrides[get_list_path_tr_uc] = _list_path_tr_dep
    app.dependency_overrides[get_upsert_path_tr_uc] = _upsert_path_tr_dep
    app.dependency_overrides[get_delete_path_tr_uc] = _delete_path_tr_dep
    app.dependency_overrides[get_enroll_uc] = _enroll_dep
    app.dependency_overrides[get_sync_note_uc] = _sync_lesson_note_dep
    app.dependency_overrides[get_list_lesson_notes_uc] = _list_lesson_notes_dep
    app.dependency_overrides[get_list_user_notes_uc] = _list_user_notes_dep
    app.dependency_overrides[get_update_lesson_note_uc] = _update_lesson_note_dep
    app.dependency_overrides[get_delete_lesson_note_uc] = _delete_lesson_note_dep
    app.dependency_overrides[get_update_progress_uc] = _update_progress_dep
    app.dependency_overrides[get_my_state_uc] = _my_state_dep
    app.dependency_overrides[get_list_favorites_uc] = _list_favorites_dep
    app.dependency_overrides[get_add_favorite_uc] = _add_favorite_dep
    app.dependency_overrides[get_remove_favorite_uc] = _remove_favorite_dep
    app.dependency_overrides[get_record_recent_uc] = _record_recent_dep
    app.dependency_overrides[get_list_recent_uc] = _list_recent_dep
    app.dependency_overrides[get_path_gating_uc] = _path_gating_dep
    app.dependency_overrides[get_eligibility_uc] = _eligibility_dep
    app.dependency_overrides[get_issue_certificate_uc] = _issue_certificate_dep
    app.dependency_overrides[get_verify_certificate_uc] = _verify_certificate_dep
    app.dependency_overrides[get_signing_key_info] = _signing_key_info_dep
    app.dependency_overrides[get_render_pdf_uc] = _render_pdf_dep
    app.dependency_overrides[get_my_deadlines_uc] = _my_deadlines_dep
    app.dependency_overrides[get_set_deadline_uc] = _set_deadline_dep
    app.dependency_overrides[get_dao_overview_uc] = _dao_overview_dep
    app.dependency_overrides[get_wallet_access_uc] = _wallet_access_dep
    app.dependency_overrides[get_run_code_uc] = _run_code_dep
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
    app.dependency_overrides[get_stream_turn_uc] = _stream_turn_dep
    # Lets require_editor fall back to a /users/me admin-flag check when
    # introspection doesn't surface it. Reuses the container's cached
    # profile client.
    app.dependency_overrides[get_user_profile_port] = lambda: container.user_profile_port

    app.include_router(health_router)
    app.include_router(content_router)
    app.include_router(concepts_public_router)
    app.include_router(concepts_admin_router)
    app.include_router(leads_public_router)
    app.include_router(leads_admin_router)
    app.include_router(analytics_public_router)
    app.include_router(achievements_public_router)
    app.include_router(activity_public_router)
    app.include_router(analytics_admin_router)
    app.include_router(recommendations_router)
    app.include_router(skills_public_router)
    app.include_router(blog_public_router)
    app.include_router(blog_admin_router)
    app.include_router(learning_public_router)
    app.include_router(lesson_notes_lesson_router)
    app.include_router(lesson_notes_notes_router)
    app.include_router(learning_admin_router)
    app.include_router(bookmarks_public_router)
    app.include_router(courses_public_router)
    app.include_router(courses_admin_router)
    app.include_router(category_public_router)
    app.include_router(category_admin_router)
    app.include_router(notebook_public_router)
    app.include_router(quizzes_player_router)
    app.include_router(quizzes_admin_router)
    app.include_router(quizzes_catalog_router)
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
    app.include_router(wallet_router)
    app.include_router(code_player_router)
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
