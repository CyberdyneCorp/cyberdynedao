"""Courses endpoints — public catalogue + admin authoring."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, Response

from cyberdyne_backend.adapters.inbound.api.courses.schemas import (
    CourseCertificateResponse,
    CourseCertificateVerificationResponse,
    CourseDetailResponse,
    CourseLanguagesResponse,
    CourseProgressResponse,
    CourseSummaryResponse,
    CourseTranslationStartedResponse,
    CreateCourseRequest,
    CreateLessonRequest,
    LessonProgressResponse,
    LessonResponse,
    MyCourseProgressItem,
    ReorderCoursesRequest,
    ReorderLessonsRequest,
    SetCourseDeadlineRequest,
    SetLessonProgressRequest,
    UpdateCourseRequest,
    UpdateLessonRequest,
)
from cyberdyne_backend.adapters.inbound.api.locale import resolve_locale
from cyberdyne_backend.adapters.inbound.middleware.auth import (
    EDITOR_SCOPE,
    require_editor,
    require_principal,
)
from cyberdyne_backend.application.academy import (
    SUPPORTED_LANGUAGES,
    GetCourseLanguages,
)
from cyberdyne_backend.application.courses import (
    AddLesson,
    AddLessonCommand,
    CreateCourse,
    CreateCourseCommand,
    DeleteCourse,
    DeleteLesson,
    GetCourse,
    GetMyCourseCertificate,
    GetMyCourseProgress,
    IssueCourseCertificate,
    ListCourses,
    ListMyCourseProgress,
    RenderCourseCertificatePdf,
    ReorderCourses,
    ReorderLessons,
    SetCourseDeadline,
    SetCoursePublished,
    SetLessonProgress,
    UpdateCourse,
    UpdateCourseCommand,
    UpdateLesson,
    UpdateLessonCommand,
    VerifyCourseCertificate,
)
from cyberdyne_backend.application.courses.certificates import CourseCertificateVerification
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.courses import (
    Course,
    CourseCertificate,
    CourseCertificateNotEligibleError,
    CourseCertificateNotFoundError,
    CourseNotFoundError,
    CourseProgress,
    DuplicateCourseSlugError,
    InvalidCourseLevelError,
    InvalidLessonContentError,
    Lesson,
    LessonNotFoundError,
    parse_level,
)
from cyberdyne_backend.domain.learning import days_remaining, deadline_status

public_router = APIRouter(prefix="/api/v1/courses", tags=["courses"])
admin_router = APIRouter(prefix="/api/v1/admin/courses", tags=["courses-admin"])


# Dependency stubs — overridden in main.py.
async def get_list_courses_uc() -> ListCourses:  # pragma: no cover - override target
    raise NotImplementedError


async def get_course_uc() -> GetCourse:  # pragma: no cover - override target
    raise NotImplementedError


async def get_create_course_uc() -> CreateCourse:  # pragma: no cover - override target
    raise NotImplementedError


async def get_update_course_uc() -> UpdateCourse:  # pragma: no cover - override target
    raise NotImplementedError


async def get_set_published_uc() -> SetCoursePublished:  # pragma: no cover - override target
    raise NotImplementedError


async def get_delete_course_uc() -> DeleteCourse:  # pragma: no cover - override target
    raise NotImplementedError


async def get_reorder_courses_uc() -> ReorderCourses:  # pragma: no cover - override target
    raise NotImplementedError


async def get_add_lesson_uc() -> AddLesson:  # pragma: no cover - override target
    raise NotImplementedError


async def get_update_lesson_uc() -> UpdateLesson:  # pragma: no cover - override target
    raise NotImplementedError


async def get_delete_lesson_uc() -> DeleteLesson:  # pragma: no cover - override target
    raise NotImplementedError


async def get_reorder_lessons_uc() -> ReorderLessons:  # pragma: no cover - override target
    raise NotImplementedError


async def get_set_lesson_progress_uc() -> SetLessonProgress:  # pragma: no cover - override target
    raise NotImplementedError


async def get_my_course_progress_uc() -> GetMyCourseProgress:  # pragma: no cover - override target
    raise NotImplementedError


async def get_set_course_deadline_uc() -> SetCourseDeadline:  # pragma: no cover - override target
    raise NotImplementedError


async def get_issue_certificate_uc() -> (
    IssueCourseCertificate
):  # pragma: no cover - override target
    raise NotImplementedError


async def get_my_certificate_uc() -> GetMyCourseCertificate:  # pragma: no cover - override target
    raise NotImplementedError


async def get_verify_certificate_uc() -> (
    VerifyCourseCertificate
):  # pragma: no cover - override target
    raise NotImplementedError


async def get_certificate_pdf_uc() -> (
    RenderCourseCertificatePdf
):  # pragma: no cover - override target
    raise NotImplementedError


async def get_course_languages_uc() -> GetCourseLanguages:  # pragma: no cover - override target
    raise NotImplementedError


# Returns an async callable ``(slug, language) -> None`` that translates one
# course in its OWN session + LLM client — safe to run as a background task
# after the request's session has closed. Overridden in main.py.
async def get_translate_course_runner() -> Callable[
    [str, str], Awaitable[None]
]:  # pragma: no cover - override target
    raise NotImplementedError


def translation_available() -> bool:  # pragma: no cover - override target
    # Overridden in main.py from settings (OpenAI key present?).
    raise NotImplementedError


def _viewer_is_authenticated(request: Request) -> bool:
    # Any signed-in CyberdyneAuth user, regardless of scope — used to decide
    # whether a viewer may read past the first lesson of a course.
    return isinstance(getattr(request.state, "principal", None), UserPrincipal)


def _viewer_can_see_drafts(request: Request) -> bool:
    # Must mirror ``require_editor``: a caller who can author courses must
    # also be able to *see* the drafts they author. Honour both the
    # ``editor`` scope and the CyberdyneAuth ``is_admin`` flag — otherwise
    # an admin can create a draft (201) but never see it in the catalogue.
    principal = getattr(request.state, "principal", None)
    if not isinstance(principal, UserPrincipal):
        return False
    return EDITOR_SCOPE in principal.scopes or principal.is_admin


def _certificate_response(cert: CourseCertificate) -> CourseCertificateResponse:
    return CourseCertificateResponse(
        id=cert.id,
        user_id=cert.user_id,
        course_slug=cert.course_slug,
        issued_at=cert.issued_at,
        verification_hash=cert.verification_hash,
    )


def _verification_response(
    result: CourseCertificateVerification,
) -> CourseCertificateVerificationResponse:
    return CourseCertificateVerificationResponse(
        valid=result.valid,
        certificate=(
            _certificate_response(result.certificate) if result.certificate is not None else None
        ),
    )


def _progress_response(progress: CourseProgress) -> CourseProgressResponse:
    return CourseProgressResponse(
        course_id=progress.course_id,
        slug=progress.slug,
        total_lessons=progress.total_lessons,
        completed_lessons=progress.completed_lessons,
        percent=progress.percent,
        completed=progress.completed,
        lessons=[
            LessonProgressResponse(
                lesson_id=view.lesson_id,
                title=view.title,
                percent=view.percent,
                completed=view.completed,
            )
            for view in progress.lessons
        ],
    )


# ── Response builders ────────────────────────────────────────────────


def _lesson_response(lesson: Lesson, *, include_body: bool = True) -> LessonResponse:
    # ``include_body`` is False for the lessons a guest may not read yet: we
    # keep the metadata (title, type, duration) so the syllabus still renders,
    # but withhold the actual content so it never reaches the client.
    return LessonResponse(
        id=lesson.id,
        course_id=lesson.course_id,
        title=lesson.title,
        lesson_type=lesson.lesson_type.value,
        sort_order=lesson.sort_order,
        content_url=lesson.content_url if include_body else None,
        text_body=lesson.text_body if include_body else None,
        duration=lesson.duration,
    )


def _summary(course: Course) -> CourseSummaryResponse:
    now = datetime.now(tz=UTC)
    return CourseSummaryResponse(
        id=course.id,
        slug=course.slug,
        title=course.title,
        description=course.description,
        level=course.level.value,
        status=course.status.value,
        mandatory=course.mandatory,
        sort_order=course.sort_order,
        lesson_count=len(course.lessons),
        created_at=course.created_at,
        published_at=course.published_at,
        due_at=course.due_at,
        deadline_status=deadline_status(course.due_at, now=now).value,
        days_remaining=days_remaining(course.due_at, now=now),
    )


def _detail(course: Course, *, full_content: bool = True) -> CourseDetailResponse:
    # Guests (``full_content=False``) may only read the FIRST lesson; the rest
    # come back with their bodies stripped. Authenticated viewers get the lot.
    return CourseDetailResponse(
        **_summary(course).model_dump(by_alias=False),
        lessons=[
            _lesson_response(les, include_body=full_content or idx == 0)
            for idx, les in enumerate(course.lessons)
        ],
    )


# ── Public catalogue ─────────────────────────────────────────────────


@public_router.get(
    "",
    response_model=list[CourseSummaryResponse],
    response_model_by_alias=True,
)
async def list_courses(
    request: Request,
    use_case: Annotated[ListCourses, Depends(get_list_courses_uc)],
    locale: Annotated[str, Depends(resolve_locale)],
    level: str | None = None,
) -> list[CourseSummaryResponse]:
    parsed_level = None
    if level is not None:
        try:
            parsed_level = parse_level(level)
        except InvalidCourseLevelError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
    courses = await use_case.execute(
        level=parsed_level,
        include_drafts=_viewer_can_see_drafts(request),
        locale=locale,
    )
    return [_summary(c) for c in courses]


@public_router.get(
    "/{slug}",
    response_model=CourseDetailResponse,
    response_model_by_alias=True,
)
async def get_course(
    slug: str,
    request: Request,
    use_case: Annotated[GetCourse, Depends(get_course_uc)],
    locale: Annotated[str, Depends(resolve_locale)],
) -> CourseDetailResponse:
    try:
        course = await use_case.execute(
            slug, include_drafts=_viewer_can_see_drafts(request), locale=locale
        )
    except CourseNotFoundError as exc:
        raise HTTPException(status_code=404, detail="course not found") from exc
    return _detail(course, full_content=_viewer_is_authenticated(request))


# ── Learner progress ─────────────────────────────────────────────────


async def get_my_courses_progress_uc() -> ListMyCourseProgress:  # pragma: no cover
    raise NotImplementedError


# Declared BEFORE "/{slug}/progress" so "me" isn't captured as a slug.
@public_router.get(
    "/me/progress",
    response_model=list[MyCourseProgressItem],
    response_model_by_alias=True,
)
async def list_my_courses_progress(
    use_case: Annotated[ListMyCourseProgress, Depends(get_my_courses_progress_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> list[MyCourseProgressItem]:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    items = await use_case.execute(user_id=principal.user_id)
    # Only surface courses the learner has actually started — the catalogue
    # shows "Start" for the rest.
    return [
        MyCourseProgressItem(
            slug=p.slug,
            total_lessons=p.total_lessons,
            completed_lessons=p.completed_lessons,
            percent=p.percent,
            completed=p.completed,
        )
        for p in items
        if p.completed_lessons > 0
    ]


@public_router.get(
    "/{slug}/progress",
    response_model=CourseProgressResponse,
    response_model_by_alias=True,
)
async def get_my_course_progress(
    slug: str,
    use_case: Annotated[GetMyCourseProgress, Depends(get_my_course_progress_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> CourseProgressResponse:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    try:
        progress = await use_case.execute(user_id=principal.user_id, slug=slug)
    except CourseNotFoundError as exc:
        raise HTTPException(status_code=404, detail="course not found") from exc
    return _progress_response(progress)


@public_router.put(
    "/{slug}/lessons/{lesson_id}/progress",
    response_model=CourseProgressResponse,
    response_model_by_alias=True,
)
async def set_lesson_progress(
    slug: str,
    lesson_id: UUID,
    body: SetLessonProgressRequest,
    use_case: Annotated[SetLessonProgress, Depends(get_set_lesson_progress_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> CourseProgressResponse:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    try:
        progress = await use_case.execute(
            user_id=principal.user_id, slug=slug, lesson_id=lesson_id, percent=body.percent
        )
    except CourseNotFoundError as exc:
        raise HTTPException(status_code=404, detail="course not found") from exc
    except LessonNotFoundError as exc:
        raise HTTPException(status_code=404, detail="lesson not found") from exc
    return _progress_response(progress)


# ── Certificates ─────────────────────────────────────────────────────


@public_router.get(
    "/certificates/{certificate_id}/verify",
    response_model=CourseCertificateVerificationResponse,
    response_model_by_alias=True,
)
async def verify_course_certificate(
    certificate_id: UUID,
    use_case: Annotated[VerifyCourseCertificate, Depends(get_verify_certificate_uc)],
) -> CourseCertificateVerificationResponse:
    """Public: confirm a course certificate's signature matches its
    claims. Unknown ids return ``valid: false`` (not 404)."""
    return _verification_response(await use_case.execute(certificate_id))


@public_router.get(
    "/certificates/{certificate_id}/pdf",
    response_class=Response,
    responses={200: {"content": {"application/pdf": {}}}},
)
async def download_course_certificate_pdf(
    certificate_id: UUID,
    use_case: Annotated[RenderCourseCertificatePdf, Depends(get_certificate_pdf_uc)],
) -> Response:
    # Public download — the certificate id is the bearer token, same as verify.
    try:
        pdf = await use_case.execute(certificate_id)
    except CourseCertificateNotFoundError as exc:
        raise HTTPException(status_code=404, detail="certificate not found") from exc
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="certificate-{certificate_id}.pdf"'},
    )


@public_router.post(
    "/{slug}/certificate",
    response_model=CourseCertificateResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def issue_course_certificate(
    slug: str,
    use_case: Annotated[IssueCourseCertificate, Depends(get_issue_certificate_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> CourseCertificateResponse:
    """Claim the signed-in learner's certificate for a completed course.
    Idempotent (returns the existing certificate); 409 if not every
    lesson is complete yet."""
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    try:
        cert = await use_case.execute(user_id=principal.user_id, slug=slug)
    except CourseNotFoundError as exc:
        raise HTTPException(status_code=404, detail="course not found") from exc
    except CourseCertificateNotEligibleError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return _certificate_response(cert)


@public_router.get(
    "/{slug}/certificate",
    response_model=CourseCertificateResponse,
    response_model_by_alias=True,
)
async def get_my_course_certificate(
    slug: str,
    use_case: Annotated[GetMyCourseCertificate, Depends(get_my_certificate_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> CourseCertificateResponse:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    cert = await use_case.execute(user_id=principal.user_id, course_slug=slug)
    if cert is None:
        raise HTTPException(status_code=404, detail="certificate not found")
    return _certificate_response(cert)


# ── Admin — course authoring ─────────────────────────────────────────


@admin_router.post(
    "",
    response_model=CourseDetailResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def create_course(
    body: CreateCourseRequest,
    use_case: Annotated[CreateCourse, Depends(get_create_course_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> CourseDetailResponse:
    try:
        course = await use_case.execute(
            CreateCourseCommand(
                title=body.title,
                description=body.description,
                level=body.level,
                slug=body.slug,
                mandatory=body.mandatory,
                sort_order=body.sort_order,
            )
        )
    except DuplicateCourseSlugError as exc:
        raise HTTPException(status_code=409, detail=f"slug already exists: {exc}") from exc
    return _detail(course)


@admin_router.patch(
    "/{slug}",
    response_model=CourseDetailResponse,
    response_model_by_alias=True,
)
async def update_course(
    slug: str,
    body: UpdateCourseRequest,
    use_case: Annotated[UpdateCourse, Depends(get_update_course_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> CourseDetailResponse:
    try:
        course = await use_case.execute(
            slug,
            UpdateCourseCommand(
                title=body.title,
                description=body.description,
                mandatory=body.mandatory,
                sort_order=body.sort_order,
            ),
        )
    except CourseNotFoundError as exc:
        raise HTTPException(status_code=404, detail="course not found") from exc
    return _detail(course)


@admin_router.post(
    "/{slug}/publish",
    response_model=CourseDetailResponse,
    response_model_by_alias=True,
)
async def publish_course(
    slug: str,
    use_case: Annotated[SetCoursePublished, Depends(get_set_published_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> CourseDetailResponse:
    try:
        course = await use_case.execute(slug, published=True)
    except CourseNotFoundError as exc:
        raise HTTPException(status_code=404, detail="course not found") from exc
    return _detail(course)


@admin_router.post(
    "/{slug}/unpublish",
    response_model=CourseDetailResponse,
    response_model_by_alias=True,
)
async def unpublish_course(
    slug: str,
    use_case: Annotated[SetCoursePublished, Depends(get_set_published_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> CourseDetailResponse:
    try:
        course = await use_case.execute(slug, published=False)
    except CourseNotFoundError as exc:
        raise HTTPException(status_code=404, detail="course not found") from exc
    return _detail(course)


@admin_router.put(
    "/{slug}/deadline",
    response_model=CourseDetailResponse,
    response_model_by_alias=True,
)
async def set_course_deadline(
    slug: str,
    body: SetCourseDeadlineRequest,
    use_case: Annotated[SetCourseDeadline, Depends(get_set_course_deadline_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> CourseDetailResponse:
    try:
        course = await use_case.execute(slug, due_at=body.due_at)
    except CourseNotFoundError as exc:
        raise HTTPException(status_code=404, detail="course not found") from exc
    return _detail(course)


@admin_router.delete("/{slug}", status_code=204)
async def delete_course(
    slug: str,
    use_case: Annotated[DeleteCourse, Depends(get_delete_course_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> None:
    try:
        await use_case.execute(slug)
    except CourseNotFoundError as exc:
        raise HTTPException(status_code=404, detail="course not found") from exc


@admin_router.post(
    "/reorder",
    response_model=list[CourseSummaryResponse],
    response_model_by_alias=True,
)
async def reorder_courses(
    body: ReorderCoursesRequest,
    use_case: Annotated[ReorderCourses, Depends(get_reorder_courses_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> list[CourseSummaryResponse]:
    try:
        courses = await use_case.execute(body.order)
    except CourseNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"course not found: {exc}") from exc
    return [_summary(c) for c in courses]


# ── Admin — translations ─────────────────────────────────────────────


@admin_router.get(
    "/{slug}/translations",
    response_model=CourseLanguagesResponse,
    response_model_by_alias=True,
)
async def get_course_languages(
    slug: str,
    use_case: Annotated[GetCourseLanguages, Depends(get_course_languages_uc)],
    can_translate: Annotated[bool, Depends(translation_available)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> CourseLanguagesResponse:
    """Languages this course is available in + whether translation can run."""
    try:
        available = await use_case.execute(slug)
    except CourseNotFoundError as exc:
        raise HTTPException(status_code=404, detail="course not found") from exc
    return CourseLanguagesResponse(
        available=available,
        supported=list(SUPPORTED_LANGUAGES),
        can_translate=can_translate,
    )


@admin_router.post(
    "/{slug}/translations/{language}",
    response_model=CourseTranslationStartedResponse,
    response_model_by_alias=True,
    status_code=202,
)
async def translate_course(
    slug: str,
    language: str,
    background_tasks: BackgroundTasks,
    languages_uc: Annotated[GetCourseLanguages, Depends(get_course_languages_uc)],
    runner: Annotated[Callable[[str, str], Awaitable[None]], Depends(get_translate_course_runner)],
    can_translate: Annotated[bool, Depends(translation_available)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> CourseTranslationStartedResponse:
    """Kick off a background translation of the course into ``language``.

    Returns 202 immediately — a single course is many LLM calls and would
    exceed proxy timeouts. The client polls ``GET …/translations`` until the
    language appears in ``available``. Idempotent: re-running only fills gaps.
    """
    if language not in SUPPORTED_LANGUAGES or language == "en":
        raise HTTPException(status_code=422, detail=f"unsupported language: {language}")
    if not can_translate:
        raise HTTPException(status_code=503, detail="translation unavailable (no OpenAI key)")
    # 404 before scheduling work if the slug is unknown.
    try:
        await languages_uc.execute(slug)
    except CourseNotFoundError as exc:
        raise HTTPException(status_code=404, detail="course not found") from exc
    background_tasks.add_task(runner, slug, language)
    return CourseTranslationStartedResponse(slug=slug, language=language)


# ── Admin — lesson authoring ─────────────────────────────────────────


@admin_router.post(
    "/{slug}/lessons",
    response_model=LessonResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def add_lesson(
    slug: str,
    body: CreateLessonRequest,
    use_case: Annotated[AddLesson, Depends(get_add_lesson_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> LessonResponse:
    try:
        lesson = await use_case.execute(
            slug,
            AddLessonCommand(
                title=body.title,
                lesson_type=body.lesson_type,
                content_url=body.content_url,
                text_body=body.text_body,
                duration=body.duration,
                sort_order=body.sort_order,
            ),
        )
    except CourseNotFoundError as exc:
        raise HTTPException(status_code=404, detail="course not found") from exc
    except InvalidLessonContentError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _lesson_response(lesson)


@admin_router.patch(
    "/{slug}/lessons/{lesson_id}",
    response_model=LessonResponse,
    response_model_by_alias=True,
)
async def update_lesson(
    slug: str,
    lesson_id: UUID,
    body: UpdateLessonRequest,
    use_case: Annotated[UpdateLesson, Depends(get_update_lesson_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> LessonResponse:
    try:
        lesson = await use_case.execute(
            slug,
            lesson_id,
            UpdateLessonCommand(
                title=body.title,
                content_url=body.content_url,
                text_body=body.text_body,
                duration=body.duration,
                sort_order=body.sort_order,
            ),
        )
    except CourseNotFoundError as exc:
        raise HTTPException(status_code=404, detail="course not found") from exc
    except LessonNotFoundError as exc:
        raise HTTPException(status_code=404, detail="lesson not found") from exc
    except InvalidLessonContentError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _lesson_response(lesson)


@admin_router.delete("/{slug}/lessons/{lesson_id}", status_code=204)
async def delete_lesson(
    slug: str,
    lesson_id: UUID,
    use_case: Annotated[DeleteLesson, Depends(get_delete_lesson_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> None:
    try:
        await use_case.execute(slug, lesson_id)
    except CourseNotFoundError as exc:
        raise HTTPException(status_code=404, detail="course not found") from exc
    except LessonNotFoundError as exc:
        raise HTTPException(status_code=404, detail="lesson not found") from exc


@admin_router.post(
    "/{slug}/lessons/reorder",
    response_model=CourseDetailResponse,
    response_model_by_alias=True,
)
async def reorder_lessons(
    slug: str,
    body: ReorderLessonsRequest,
    use_case: Annotated[ReorderLessons, Depends(get_reorder_lessons_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> CourseDetailResponse:
    try:
        course = await use_case.execute(slug, body.order)
    except CourseNotFoundError as exc:
        raise HTTPException(status_code=404, detail="course not found") from exc
    return _detail(course)


__all__ = ["admin_router", "public_router"]
