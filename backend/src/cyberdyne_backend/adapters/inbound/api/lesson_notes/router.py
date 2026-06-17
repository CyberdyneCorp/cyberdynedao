"""Per-user lesson notes endpoints (issue #188).

Lesson-scoped annotations (optional highlighted quote + body) the client
syncs from on-device storage. All routes are scoped to the authenticated
user. POST accepts a client-supplied ``id`` so re-sync is idempotent.
"""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response

from cyberdyne_backend.adapters.inbound.api.lesson_notes.schemas import (
    CreateLessonNoteRequest,
    LessonNoteListResponse,
    LessonNoteResponse,
    UpdateLessonNoteRequest,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.application.lesson_notes import (
    DEFAULT_NOTES_LIMIT,
    MAX_NOTES_LIMIT,
    DeleteLessonNote,
    ListLessonNotes,
    ListUserNotes,
    SyncLessonNote,
    UpdateLessonNote,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.lesson_notes import (
    InvalidLessonNoteError,
    LessonNote,
    LessonNoteNotFoundError,
    LessonNotePage,
)

# Notes are reached two ways: nested under a lesson (create + list) and
# flat by id / across a course (the client's export + edit/delete paths).
lesson_router = APIRouter(prefix="/api/v1/lessons", tags=["lesson-notes"])
notes_router = APIRouter(prefix="/api/v1/notes", tags=["lesson-notes"])


# Dependency stubs — overridden in main.py.
async def get_sync_note_uc() -> SyncLessonNote:  # pragma: no cover - override target
    raise NotImplementedError


async def get_list_lesson_notes_uc() -> ListLessonNotes:  # pragma: no cover - override target
    raise NotImplementedError


async def get_list_user_notes_uc() -> ListUserNotes:  # pragma: no cover - override target
    raise NotImplementedError


async def get_update_note_uc() -> UpdateLessonNote:  # pragma: no cover - override target
    raise NotImplementedError


async def get_delete_note_uc() -> DeleteLessonNote:  # pragma: no cover - override target
    raise NotImplementedError


def _require_user(principal: UserPrincipal) -> UserPrincipal:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    return principal


def _note_response(n: LessonNote) -> LessonNoteResponse:
    return LessonNoteResponse(
        id=n.id,
        course_slug=n.course_slug,
        lesson_id=n.lesson_id,
        quote=n.quote,
        body=n.body,
        created_at=n.created_at,
        updated_at=n.updated_at,
    )


# ── Lesson-nested: create + list ──────────────────────────────────────


@lesson_router.post(
    "/{lesson_id}/notes",
    response_model=LessonNoteResponse,
    response_model_by_alias=True,
)
async def sync_lesson_note(
    lesson_id: str,
    body: CreateLessonNoteRequest,
    response: Response,
    use_case: Annotated[SyncLessonNote, Depends(get_sync_note_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> LessonNoteResponse:
    """Create a note (or idempotently update one whose client-supplied
    ``id`` already exists). Returns 201 on create, 200 on idempotent
    update."""
    user = _require_user(principal)
    try:
        result = await use_case.execute(
            user_id=user.user_id,
            lesson_id=lesson_id,
            course_slug=body.course_slug,
            body=body.body,
            quote=body.quote,
            note_id=body.id,
        )
    except InvalidLessonNoteError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    response.status_code = 201 if result.created else 200
    return _note_response(result.note)


@lesson_router.get(
    "/{lesson_id}/notes",
    response_model=list[LessonNoteResponse],
    response_model_by_alias=True,
)
async def list_lesson_notes(
    lesson_id: str,
    use_case: Annotated[ListLessonNotes, Depends(get_list_lesson_notes_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> list[LessonNoteResponse]:
    user = _require_user(principal)
    notes = await use_case.execute(user_id=user.user_id, lesson_id=lesson_id)
    return [_note_response(n) for n in notes]


# ── Flat: list-across / update / delete ───────────────────────────────


@notes_router.get("", response_model=LessonNoteListResponse, response_model_by_alias=True)
async def list_notes(
    use_case: Annotated[ListUserNotes, Depends(get_list_user_notes_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
    course_slug: Annotated[str | None, Query(alias="courseSlug")] = None,
    cursor: Annotated[str | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=MAX_NOTES_LIMIT)] = DEFAULT_NOTES_LIMIT,
) -> LessonNoteListResponse:
    user = _require_user(principal)
    page: LessonNotePage = await use_case.execute(
        user_id=user.user_id, course_slug=course_slug, cursor=cursor, limit=limit
    )
    return LessonNoteListResponse(
        items=[_note_response(n) for n in page.items],
        next_cursor=page.next_cursor,
    )


@notes_router.patch("/{note_id}", response_model=LessonNoteResponse, response_model_by_alias=True)
async def update_note(
    note_id: UUID,
    body: UpdateLessonNoteRequest,
    use_case: Annotated[UpdateLessonNote, Depends(get_update_note_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> LessonNoteResponse:
    user = _require_user(principal)
    # Distinguish "quote omitted" from an explicit "quote": null.
    quote_set = "quote" in body.model_fields_set
    try:
        note = await use_case.execute(
            user_id=user.user_id,
            note_id=note_id,
            body=body.body,
            quote=body.quote,
            quote_set=quote_set,
        )
    except LessonNoteNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except InvalidLessonNoteError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _note_response(note)


@notes_router.delete("/{note_id}", status_code=204)
async def delete_note(
    note_id: UUID,
    use_case: Annotated[DeleteLessonNote, Depends(get_delete_note_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> Response:
    user = _require_user(principal)
    try:
        await use_case.execute(user_id=user.user_id, note_id=note_id)
    except LessonNoteNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Response(status_code=204)


__all__ = ["lesson_router", "notes_router"]
