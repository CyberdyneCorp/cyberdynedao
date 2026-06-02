"""Courses endpoints — public catalogue + admin authoring."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request

from cyberdyne_backend.adapters.inbound.api.courses.schemas import (
    CourseDetailResponse,
    CourseProgressResponse,
    CourseSummaryResponse,
    CreateCourseRequest,
    CreateLessonRequest,
    LessonProgressResponse,
    LessonResponse,
    ReorderCoursesRequest,
    ReorderLessonsRequest,
    SetLessonProgressRequest,
    UpdateCourseRequest,
    UpdateLessonRequest,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import (
    EDITOR_SCOPE,
    require_editor,
    require_principal,
)
from cyberdyne_backend.application.courses import (
    AddLesson,
    AddLessonCommand,
    CreateCourse,
    CreateCourseCommand,
    DeleteCourse,
    DeleteLesson,
    GetCourse,
    GetMyCourseProgress,
    ListCourses,
    ReorderCourses,
    ReorderLessons,
    SetCoursePublished,
    SetLessonProgress,
    UpdateCourse,
    UpdateCourseCommand,
    UpdateLesson,
    UpdateLessonCommand,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.courses import (
    Course,
    CourseNotFoundError,
    CourseProgress,
    DuplicateCourseSlugError,
    InvalidCourseLevelError,
    InvalidLessonContentError,
    Lesson,
    LessonNotFoundError,
    parse_level,
)

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


def _viewer_can_see_drafts(request: Request) -> bool:
    principal = getattr(request.state, "principal", None)
    return isinstance(principal, UserPrincipal) and EDITOR_SCOPE in principal.scopes


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


def _lesson_response(lesson: Lesson) -> LessonResponse:
    return LessonResponse(
        id=lesson.id,
        course_id=lesson.course_id,
        title=lesson.title,
        lesson_type=lesson.lesson_type.value,
        sort_order=lesson.sort_order,
        content_url=lesson.content_url,
        text_body=lesson.text_body,
        duration=lesson.duration,
    )


def _summary(course: Course) -> CourseSummaryResponse:
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
    )


def _detail(course: Course) -> CourseDetailResponse:
    return CourseDetailResponse(
        **_summary(course).model_dump(by_alias=False),
        lessons=[_lesson_response(les) for les in course.lessons],
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
) -> CourseDetailResponse:
    try:
        course = await use_case.execute(slug, include_drafts=_viewer_can_see_drafts(request))
    except CourseNotFoundError as exc:
        raise HTTPException(status_code=404, detail="course not found") from exc
    return _detail(course)


# ── Learner progress ─────────────────────────────────────────────────


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
