"""Notebook notes endpoints (issue #161, part 1 — notes CRUD).

The learner's per-user "living memory". All routes are scoped to the
authenticated user; no cross-user access is possible. Flashcards +
spaced-review scheduling are follow-ups.
"""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response

from cyberdyne_backend.adapters.inbound.api.notebook.schemas import (
    FlashcardResponse,
    FlashcardWriteRequest,
    NoteListResponse,
    NoteResponse,
    NoteWriteRequest,
    ReviewRequest,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.application.notebook import (
    DEFAULT_NOTE_LIMIT,
    MAX_NOTE_LIMIT,
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
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.notebook import (
    Flashcard,
    FlashcardNotFoundError,
    InvalidFlashcardError,
    InvalidNoteError,
    Note,
    NoteFields,
    NoteNotFoundError,
    NotePage,
    parse_note_type,
    parse_review_rating,
)

public_router = APIRouter(prefix="/api/v1/notebook", tags=["notebook"])


# Dependency stubs — overridden in main.py.
async def get_create_note_uc() -> CreateNote:  # pragma: no cover - override target
    raise NotImplementedError


async def get_list_notes_uc() -> ListNotes:  # pragma: no cover - override target
    raise NotImplementedError


async def get_note_uc() -> GetNote:  # pragma: no cover - override target
    raise NotImplementedError


async def get_update_note_uc() -> UpdateNote:  # pragma: no cover - override target
    raise NotImplementedError


async def get_delete_note_uc() -> DeleteNote:  # pragma: no cover - override target
    raise NotImplementedError


async def get_add_flashcard_uc() -> AddFlashcard:  # pragma: no cover - override target
    raise NotImplementedError


async def get_list_flashcards_uc() -> ListFlashcards:  # pragma: no cover - override target
    raise NotImplementedError


async def get_delete_flashcard_uc() -> DeleteFlashcard:  # pragma: no cover - override target
    raise NotImplementedError


async def get_review_note_uc() -> ReviewNote:  # pragma: no cover - override target
    raise NotImplementedError


async def get_generate_flashcards_uc() -> GenerateFlashcards:  # pragma: no cover - override target
    raise NotImplementedError


async def get_summarize_note_uc() -> SummarizeNote:  # pragma: no cover - override target
    raise NotImplementedError


def _flashcard_response(f: Flashcard) -> FlashcardResponse:
    return FlashcardResponse(
        id=f.id,
        note_id=f.note_id,
        question=f.question,
        answer=f.answer,
        created_at=f.created_at,
    )


def _require_user(principal: UserPrincipal) -> UserPrincipal:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    return principal


def _note_response(n: Note) -> NoteResponse:
    return NoteResponse(
        id=n.id,
        title=n.title,
        type=n.type.value,
        body=n.body,
        course_slug=n.course_slug,
        lesson_id=n.lesson_id,
        code=n.code,
        language=n.language,
        run_result=n.run_result,
        plot_refs=list(n.plot_refs),
        tags=list(n.tags),
        reviewed_at=n.reviewed_at,
        next_review_at=n.next_review_at,
        review_interval_days=n.review_interval_days,
        ai_summary=n.ai_summary,
        created_at=n.created_at,
        updated_at=n.updated_at,
    )


def _fields_from(body: NoteWriteRequest) -> NoteFields:
    return NoteFields(
        title=body.title,
        type=parse_note_type(body.type),
        body=body.body,
        course_slug=body.course_slug,
        lesson_id=body.lesson_id,
        code=body.code,
        language=body.language,
        run_result=body.run_result,
        plot_refs=tuple(body.plot_refs),
        tags=tuple(body.tags),
    )


def _list_response(page: NotePage) -> NoteListResponse:
    return NoteListResponse(
        items=[_note_response(n) for n in page.items],
        next_cursor=page.next_cursor,
    )


@public_router.post(
    "/notes", response_model=NoteResponse, response_model_by_alias=True, status_code=201
)
async def create_note(
    body: NoteWriteRequest,
    use_case: Annotated[CreateNote, Depends(get_create_note_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> NoteResponse:
    user = _require_user(principal)
    try:
        note = await use_case.execute(user_id=user.user_id, fields=_fields_from(body))
    except InvalidNoteError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _note_response(note)


@public_router.get("/notes", response_model=NoteListResponse, response_model_by_alias=True)
async def list_notes(
    use_case: Annotated[ListNotes, Depends(get_list_notes_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
    type: Annotated[str | None, Query()] = None,
    q: Annotated[str | None, Query(max_length=128)] = None,
    due: Annotated[bool, Query()] = False,
    cursor: Annotated[str | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=MAX_NOTE_LIMIT)] = DEFAULT_NOTE_LIMIT,
) -> NoteListResponse:
    """List the learner's notes. ``due=true`` returns only notes whose
    spaced-review schedule is due now (``nextReviewAt <= now``)."""
    user = _require_user(principal)
    note_type = parse_note_type(type) if type is not None else None
    page = await use_case.execute(
        user_id=user.user_id, type=note_type, query=q, due=due, cursor=cursor, limit=limit
    )
    return _list_response(page)


@public_router.get("/notes/{note_id}", response_model=NoteResponse, response_model_by_alias=True)
async def get_note(
    note_id: UUID,
    use_case: Annotated[GetNote, Depends(get_note_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> NoteResponse:
    user = _require_user(principal)
    try:
        note = await use_case.execute(user_id=user.user_id, note_id=note_id)
    except NoteNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _note_response(note)


@public_router.patch("/notes/{note_id}", response_model=NoteResponse, response_model_by_alias=True)
async def update_note(
    note_id: UUID,
    body: NoteWriteRequest,
    use_case: Annotated[UpdateNote, Depends(get_update_note_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> NoteResponse:
    user = _require_user(principal)
    try:
        note = await use_case.execute(
            user_id=user.user_id, note_id=note_id, fields=_fields_from(body)
        )
    except NoteNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except InvalidNoteError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _note_response(note)


@public_router.delete("/notes/{note_id}", status_code=204)
async def delete_note(
    note_id: UUID,
    use_case: Annotated[DeleteNote, Depends(get_delete_note_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> Response:
    user = _require_user(principal)
    try:
        await use_case.execute(user_id=user.user_id, note_id=note_id)
    except NoteNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Response(status_code=204)


# ── Flashcards ────────────────────────────────────────────────────────


@public_router.post(
    "/notes/{note_id}/flashcards",
    response_model=FlashcardResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def add_flashcard(
    note_id: UUID,
    body: FlashcardWriteRequest,
    use_case: Annotated[AddFlashcard, Depends(get_add_flashcard_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> FlashcardResponse:
    user = _require_user(principal)
    try:
        card = await use_case.execute(
            user_id=user.user_id,
            note_id=note_id,
            question=body.question,
            answer=body.answer,
        )
    except NoteNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except InvalidFlashcardError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _flashcard_response(card)


@public_router.get(
    "/notes/{note_id}/flashcards",
    response_model=list[FlashcardResponse],
    response_model_by_alias=True,
)
async def list_flashcards(
    note_id: UUID,
    use_case: Annotated[ListFlashcards, Depends(get_list_flashcards_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> list[FlashcardResponse]:
    user = _require_user(principal)
    try:
        cards = await use_case.execute(user_id=user.user_id, note_id=note_id)
    except NoteNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return [_flashcard_response(c) for c in cards]


@public_router.delete("/notes/{note_id}/flashcards/{flashcard_id}", status_code=204)
async def delete_flashcard(
    note_id: UUID,
    flashcard_id: UUID,
    use_case: Annotated[DeleteFlashcard, Depends(get_delete_flashcard_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> Response:
    user = _require_user(principal)
    try:
        await use_case.execute(user_id=user.user_id, note_id=note_id, flashcard_id=flashcard_id)
    except (NoteNotFoundError, FlashcardNotFoundError) as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Response(status_code=204)


# ── Spaced review ─────────────────────────────────────────────────────


@public_router.post(
    "/notes/{note_id}/review",
    response_model=NoteResponse,
    response_model_by_alias=True,
)
async def review_note(
    note_id: UUID,
    body: ReviewRequest,
    use_case: Annotated[ReviewNote, Depends(get_review_note_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> NoteResponse:
    """Record a spaced-review of a note. The `rating`
    (`again`/`hard`/`good`/`easy`) advances the review interval and
    reschedules `nextReviewAt`; the updated note is returned."""
    user = _require_user(principal)
    try:
        note = await use_case.execute(
            user_id=user.user_id,
            note_id=note_id,
            rating=parse_review_rating(body.rating),
        )
    except NoteNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _note_response(note)


# ── AI generation (issue #187) ────────────────────────────────────────


@public_router.post(
    "/notes/{note_id}/flashcards/generate",
    response_model=list[FlashcardResponse],
    response_model_by_alias=True,
    status_code=201,
)
async def generate_flashcards(
    note_id: UUID,
    use_case: Annotated[GenerateFlashcards, Depends(get_generate_flashcards_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> list[FlashcardResponse]:
    """LLM-generate flashcards from the note and persist them (they then
    appear in `GET /notes/{id}/flashcards` and the `?due=` review queue).
    Returns the created cards — empty if the model produced none (e.g. the
    offline fallback when no API key is configured)."""
    user = _require_user(principal)
    try:
        cards = await use_case.execute(user_id=user.user_id, note_id=note_id)
    except NoteNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return [_flashcard_response(c) for c in cards]


@public_router.post(
    "/notes/{note_id}/summary",
    response_model=NoteResponse,
    response_model_by_alias=True,
)
async def summarize_note(
    note_id: UUID,
    use_case: Annotated[SummarizeNote, Depends(get_summarize_note_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> NoteResponse:
    """LLM-summarize the note, persist the summary onto it (`aiSummary`),
    and return the updated note."""
    user = _require_user(principal)
    try:
        note = await use_case.execute(user_id=user.user_id, note_id=note_id)
    except NoteNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _note_response(note)


__all__ = ["public_router"]
