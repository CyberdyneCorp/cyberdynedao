"""Concepts library endpoints — public browse/search + admin authoring.

Public routes are unauthenticated reads of the concept-card catalogue
(the Concepts nav). Admin routes require the ``editor`` scope. See #168.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response

from cyberdyne_backend.adapters.inbound.api.concepts.schemas import (
    ConceptListResponse,
    ConceptResponse,
    ConceptWriteRequest,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import require_editor
from cyberdyne_backend.application.concepts import (
    DEFAULT_CONCEPT_LIMIT,
    MAX_CONCEPT_LIMIT,
    ConceptInput,
    CreateConcept,
    DeleteConcept,
    GetConcept,
    ListConcepts,
    UpdateConcept,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.concepts import (
    Concept,
    ConceptNotFoundError,
    ConceptPage,
    DuplicateConceptError,
    InvalidConceptError,
)

public_router = APIRouter(prefix="/api/v1/concepts", tags=["concepts"])
admin_router = APIRouter(prefix="/api/v1/admin/concepts", tags=["concepts-admin"])


# Dependency stubs — overridden in main.py.
async def get_list_concepts_uc() -> ListConcepts:  # pragma: no cover - override target
    raise NotImplementedError


async def get_concept_uc() -> GetConcept:  # pragma: no cover - override target
    raise NotImplementedError


async def get_create_concept_uc() -> CreateConcept:  # pragma: no cover - override target
    raise NotImplementedError


async def get_update_concept_uc() -> UpdateConcept:  # pragma: no cover - override target
    raise NotImplementedError


async def get_delete_concept_uc() -> DeleteConcept:  # pragma: no cover - override target
    raise NotImplementedError


def _concept_response(c: Concept) -> ConceptResponse:
    return ConceptResponse(
        id=c.id,
        slug=c.slug,
        title=c.title,
        domain=c.domain,
        summary=c.summary,
        formula=c.formula,
        related_lessons=list(c.related_lesson_ids),
        related_courses=list(c.related_course_slugs),
        created_at=c.created_at,
        updated_at=c.updated_at,
    )


def _list_response(page: ConceptPage) -> ConceptListResponse:
    return ConceptListResponse(
        items=[_concept_response(c) for c in page.items],
        next_cursor=page.next_cursor,
    )


def _input_from(body: ConceptWriteRequest) -> ConceptInput:
    return ConceptInput(
        slug=body.slug,
        title=body.title,
        domain=body.domain,
        summary=body.summary,
        formula=body.formula,
        related_lesson_ids=tuple(body.related_lessons),
        related_course_slugs=tuple(body.related_courses),
    )


# ── Public browse / search ───────────────────────────────────────────


@public_router.get("", response_model=ConceptListResponse, response_model_by_alias=True)
async def list_concepts(
    use_case: Annotated[ListConcepts, Depends(get_list_concepts_uc)],
    q: Annotated[str | None, Query(max_length=128)] = None,
    domain: Annotated[str | None, Query(max_length=64)] = None,
    cursor: Annotated[str | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=MAX_CONCEPT_LIMIT)] = DEFAULT_CONCEPT_LIMIT,
) -> ConceptListResponse:
    page = await use_case.execute(query=q, domain=domain, cursor=cursor, limit=limit)
    return _list_response(page)


@public_router.get("/{slug}", response_model=ConceptResponse, response_model_by_alias=True)
async def get_concept(
    slug: str,
    use_case: Annotated[GetConcept, Depends(get_concept_uc)],
) -> ConceptResponse:
    try:
        concept = await use_case.execute(slug)
    except ConceptNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _concept_response(concept)


# ── Admin authoring (editor scope) ───────────────────────────────────


@admin_router.post(
    "", response_model=ConceptResponse, response_model_by_alias=True, status_code=201
)
async def create_concept(
    body: ConceptWriteRequest,
    use_case: Annotated[CreateConcept, Depends(get_create_concept_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> ConceptResponse:
    try:
        concept = await use_case.execute(_input_from(body))
    except InvalidConceptError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except DuplicateConceptError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return _concept_response(concept)


@admin_router.put("/{slug}", response_model=ConceptResponse, response_model_by_alias=True)
async def update_concept(
    slug: str,
    body: ConceptWriteRequest,
    use_case: Annotated[UpdateConcept, Depends(get_update_concept_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> ConceptResponse:
    try:
        concept = await use_case.execute(slug, _input_from(body))
    except ConceptNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except InvalidConceptError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _concept_response(concept)


@admin_router.delete("/{slug}", status_code=204)
async def delete_concept(
    slug: str,
    use_case: Annotated[DeleteConcept, Depends(get_delete_concept_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> Response:
    try:
        await use_case.execute(slug)
    except ConceptNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Response(status_code=204)


__all__ = ["admin_router", "public_router"]
