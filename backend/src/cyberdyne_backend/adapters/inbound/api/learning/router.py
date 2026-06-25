"""Learning endpoints — public catalogue + authenticated state + admin
certificate issuance."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response

from cyberdyne_backend.adapters.inbound.api.learning.schemas import (
    CertificateResponse,
    CertificateVerificationResponse,
    CreateModuleRequest,
    CreatePathRequest,
    EligibilityResponse,
    EnrollmentDeadlineResponse,
    EnrollmentResponse,
    LearningModuleResponse,
    LearningPathResponse,
    LinkedCourseResponse,
    ModuleGateResponse,
    ModuleProgressResponse,
    MyLearningStateResponse,
    ReorderPathModulesRequest,
    SetDeadlineRequest,
    SigningKeyResponse,
    TranslationResponse,
    TranslationUpsertRequest,
    UpdateModuleRequest,
    UpdatePathRequest,
    UpdateProgressRequest,
)
from cyberdyne_backend.adapters.inbound.api.locale import resolve_locale
from cyberdyne_backend.adapters.inbound.middleware.auth import (
    require_editor,
    require_principal,
)
from cyberdyne_backend.application.learning import (
    CertificateVerification,
    CheckEnrollmentEligibility,
    CreateModule,
    CreateModuleCommand,
    CreatePath,
    CreatePathCommand,
    DeleteModule,
    DeleteModuleTranslation,
    DeletePath,
    DeletePathTranslation,
    EligibilityResult,
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
    UpdateModuleCommand,
    UpdateModuleProgress,
    UpdatePath,
    UpdatePathCommand,
    UpsertModuleTranslation,
    UpsertPathTranslation,
    VerifyCertificate,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.learning import (
    Certificate,
    CertificateNotEligibleError,
    CertificateNotFoundError,
    Enrollment,
    EnrollmentDeadline,
    EnrollmentNotFoundError,
    LearningContentConflictError,
    LearningContentNotFoundError,
    LearningContentValidationError,
    LearningModule,
    LearningPath,
    LearningTranslation,
    ModuleGate,
    ModuleProgress,
    ProgressOutOfRangeError,
)

public_router = APIRouter(prefix="/api/v1/learning", tags=["learning"])
admin_router = APIRouter(prefix="/api/v1/admin/learning", tags=["learning-admin"])


# Dependency stubs — overridden in main.py.
async def get_list_modules_uc() -> ListModules:  # pragma: no cover - override target
    raise NotImplementedError


async def get_list_paths_uc() -> ListPaths:  # pragma: no cover - override target
    raise NotImplementedError


async def get_enroll_uc() -> EnrollInPath:  # pragma: no cover - override target
    raise NotImplementedError


async def get_update_progress_uc() -> UpdateModuleProgress:  # pragma: no cover - override target
    raise NotImplementedError


async def get_my_state_uc() -> GetMyLearningState:  # pragma: no cover - override target
    raise NotImplementedError


async def get_issue_certificate_uc() -> IssueCertificate:  # pragma: no cover - override target
    raise NotImplementedError


async def get_verify_certificate_uc() -> VerifyCertificate:  # pragma: no cover - override target
    raise NotImplementedError


async def get_signing_key_info() -> SigningKeyResponse:  # pragma: no cover - override target
    raise NotImplementedError


async def get_render_pdf_uc() -> RenderCertificatePdf:  # pragma: no cover - override target
    raise NotImplementedError


async def get_my_deadlines_uc() -> GetMyDeadlines:  # pragma: no cover - override target
    raise NotImplementedError


async def get_set_deadline_uc() -> SetEnrollmentDeadline:  # pragma: no cover - override target
    raise NotImplementedError


async def get_path_gating_uc() -> GetPathGating:  # pragma: no cover - override target
    raise NotImplementedError


async def get_eligibility_uc() -> CheckEnrollmentEligibility:  # pragma: no cover - override target
    raise NotImplementedError


async def get_create_module_uc() -> CreateModule:  # pragma: no cover - override target
    raise NotImplementedError


async def get_update_module_uc() -> UpdateModule:  # pragma: no cover - override target
    raise NotImplementedError


async def get_delete_module_uc() -> DeleteModule:  # pragma: no cover - override target
    raise NotImplementedError


async def get_create_path_uc() -> CreatePath:  # pragma: no cover - override target
    raise NotImplementedError


async def get_update_path_uc() -> UpdatePath:  # pragma: no cover - override target
    raise NotImplementedError


async def get_delete_path_uc() -> DeletePath:  # pragma: no cover - override target
    raise NotImplementedError


async def get_reorder_path_modules_uc() -> ReorderPathModules:  # pragma: no cover - override target
    raise NotImplementedError


async def get_list_module_tr_uc() -> ListModuleTranslations:  # pragma: no cover - override target
    raise NotImplementedError


async def get_upsert_module_tr_uc() -> (
    UpsertModuleTranslation
):  # pragma: no cover - override target
    raise NotImplementedError


async def get_delete_module_tr_uc() -> (
    DeleteModuleTranslation
):  # pragma: no cover - override target
    raise NotImplementedError


async def get_list_path_tr_uc() -> ListPathTranslations:  # pragma: no cover - override target
    raise NotImplementedError


async def get_upsert_path_tr_uc() -> UpsertPathTranslation:  # pragma: no cover - override target
    raise NotImplementedError


async def get_delete_path_tr_uc() -> DeletePathTranslation:  # pragma: no cover - override target
    raise NotImplementedError


# ── Response builders ────────────────────────────────────────────────


def _module_response(m: LearningModule) -> LearningModuleResponse:
    return LearningModuleResponse(
        slug=m.slug,
        title=m.title,
        category=m.category,
        description=m.description,
        level=m.level,
        duration=m.duration,
        icon=m.icon,
        topics=list(m.topics),
        course_slugs=list(m.course_slugs),
        courses=[
            LinkedCourseResponse(slug=c.slug, title=c.title, level=c.level) for c in m.courses
        ],
    )


def _path_response(p: LearningPath) -> LearningPathResponse:
    return LearningPathResponse(
        slug=p.slug,
        title=p.title,
        description=p.description,
        module_slugs=list(p.module_slugs),
        estimated_time=p.estimated_time,
        icon=p.icon,
    )


def _enrollment_response(e: Enrollment) -> EnrollmentResponse:
    return EnrollmentResponse(
        id=e.id,
        user_id=e.user_id,
        path_slug=e.path_slug,
        started_at=e.started_at,
        status=e.status.value,
        due_at=e.due_at,
    )


def _deadline_response(d: EnrollmentDeadline) -> EnrollmentDeadlineResponse:
    return EnrollmentDeadlineResponse(
        path_slug=d.path_slug,
        due_at=d.due_at,
        status=d.status.value,
        days_remaining=d.days_remaining,
    )


def _progress_response(p: ModuleProgress) -> ModuleProgressResponse:
    return ModuleProgressResponse(
        module_slug=p.module_slug,
        percent=p.percent,
        started_at=p.started_at,
        completed_at=p.completed_at,
    )


def _certificate_response(c: Certificate) -> CertificateResponse:
    return CertificateResponse(
        id=c.id,
        user_id=c.user_id,
        path_slug=c.path_slug,
        issued_at=c.issued_at,
        verification_hash=c.verification_hash,
        signed_payload=c.signed_payload,
    )


def _verification_response(v: CertificateVerification) -> CertificateVerificationResponse:
    return CertificateVerificationResponse(
        valid=v.valid,
        certificate=_certificate_response(v.certificate) if v.certificate else None,
    )


# ── Public catalogue ─────────────────────────────────────────────────


@public_router.get(
    "/modules",
    response_model=list[LearningModuleResponse],
    response_model_by_alias=True,
)
async def list_modules(
    use_case: Annotated[ListModules, Depends(get_list_modules_uc)],
    locale: Annotated[str, Depends(resolve_locale)],
) -> list[LearningModuleResponse]:
    modules = await use_case.execute(locale=locale)
    return [_module_response(m) for m in modules]


@public_router.get(
    "/paths",
    response_model=list[LearningPathResponse],
    response_model_by_alias=True,
)
async def list_paths(
    use_case: Annotated[ListPaths, Depends(get_list_paths_uc)],
    locale: Annotated[str, Depends(resolve_locale)],
) -> list[LearningPathResponse]:
    paths = await use_case.execute(locale=locale)
    return [_path_response(p) for p in paths]


@public_router.get(
    "/certificates/{certificate_id}/verify",
    response_model=CertificateVerificationResponse,
    response_model_by_alias=True,
)
async def verify_certificate(
    certificate_id: UUID,
    use_case: Annotated[VerifyCertificate, Depends(get_verify_certificate_uc)],
) -> CertificateVerificationResponse:
    # Public: anyone with the certificate id can check authenticity.
    result = await use_case.execute(certificate_id)
    return _verification_response(result)


@public_router.get(
    "/certificates/signing-key",
    response_model=SigningKeyResponse,
    response_model_by_alias=True,
)
async def certificate_signing_key(
    info: Annotated[SigningKeyResponse, Depends(get_signing_key_info)],
) -> SigningKeyResponse:
    """Publish the certificate verification key. For the Ed25519 scheme
    this returns the base64url public key so external verifiers (partner
    LMS, NFT minting) can check signatures without our secret; for HMAC it
    reports the algorithm with a null key (the secret is not publishable)."""
    return info


@public_router.get(
    "/certificates/{certificate_id}/pdf",
    response_class=Response,
    responses={200: {"content": {"application/pdf": {}}}},
)
async def download_certificate_pdf(
    certificate_id: UUID,
    use_case: Annotated[RenderCertificatePdf, Depends(get_render_pdf_uc)],
) -> Response:
    # Public download — the certificate id is the bearer token, same as verify.
    try:
        pdf = await use_case.execute(certificate_id)
    except CertificateNotFoundError as exc:
        raise HTTPException(status_code=404, detail="certificate not found") from exc
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="certificate-{certificate_id}.pdf"'},
    )


# ── Authenticated user state ─────────────────────────────────────────


@public_router.get(
    "/me",
    response_model=MyLearningStateResponse,
    response_model_by_alias=True,
)
async def get_my_state(
    use_case: Annotated[GetMyLearningState, Depends(get_my_state_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> MyLearningStateResponse:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    state = await use_case.execute(principal.user_id)
    return MyLearningStateResponse(
        enrollments=[_enrollment_response(e) for e in state.enrollments],
        progress=[_progress_response(p) for p in state.progress_by_module.values()],
        certificates=[_certificate_response(c) for c in state.certificates],
    )


@public_router.post(
    "/paths/{slug}/enroll",
    response_model=EnrollmentResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def enroll_in_path(
    slug: str,
    use_case: Annotated[EnrollInPath, Depends(get_enroll_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> EnrollmentResponse:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    try:
        enrollment = await use_case.execute(user_id=principal.user_id, path_slug=slug)
    except LearningContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _enrollment_response(enrollment)


@public_router.patch(
    "/modules/{slug}/progress",
    response_model=ModuleProgressResponse,
    response_model_by_alias=True,
)
async def update_module_progress(
    slug: str,
    body: UpdateProgressRequest,
    use_case: Annotated[UpdateModuleProgress, Depends(get_update_progress_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> ModuleProgressResponse:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    try:
        progress = await use_case.execute(
            user_id=principal.user_id,
            module_slug=slug,
            percent=body.percent,
        )
    except ProgressOutOfRangeError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _progress_response(progress)


# ── Deadlines ────────────────────────────────────────────────────────


@public_router.get(
    "/deadlines",
    response_model=list[EnrollmentDeadlineResponse],
    response_model_by_alias=True,
)
async def my_deadlines(
    use_case: Annotated[GetMyDeadlines, Depends(get_my_deadlines_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> list[EnrollmentDeadlineResponse]:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    deadlines = await use_case.execute(principal.user_id)
    return [_deadline_response(d) for d in deadlines]


# ── Prerequisites & gating ───────────────────────────────────────────


def _gate_response(gate: ModuleGate) -> ModuleGateResponse:
    return ModuleGateResponse(
        module_slug=gate.module_slug,
        level=gate.level,
        position=gate.position,
        unlocked=gate.unlocked,
        completed=gate.completed,
        blocked_by=gate.blocked_by,
        reason=gate.reason,
    )


def _eligibility_response(result: EligibilityResult) -> EligibilityResponse:
    return EligibilityResponse(
        eligible=result.eligible,
        already_enrolled=result.already_enrolled,
        next_module=result.next_module,
        reason=result.reason,
    )


@public_router.get(
    "/paths/{slug}/gating",
    response_model=list[ModuleGateResponse],
    response_model_by_alias=True,
)
async def get_path_gating(
    slug: str,
    use_case: Annotated[GetPathGating, Depends(get_path_gating_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> list[ModuleGateResponse]:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    try:
        gates = await use_case.execute(user_id=principal.user_id, path_slug=slug)
    except LearningContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return [_gate_response(g) for g in gates]


@public_router.get(
    "/paths/{slug}/eligibility",
    response_model=EligibilityResponse,
    response_model_by_alias=True,
)
async def check_path_eligibility(
    slug: str,
    use_case: Annotated[CheckEnrollmentEligibility, Depends(get_eligibility_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> EligibilityResponse:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    try:
        result = await use_case.execute(user_id=principal.user_id, path_slug=slug)
    except LearningContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _eligibility_response(result)


# ── Admin — issue certificate ────────────────────────────────────────


@admin_router.post(
    "/paths/{slug}/certificate/issue/{user_id}",
    response_model=CertificateResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def issue_certificate(
    slug: str,
    user_id: UUID,
    use_case: Annotated[IssueCertificate, Depends(get_issue_certificate_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> CertificateResponse:
    try:
        cert = await use_case.execute(user_id=user_id, path_slug=slug)
    except LearningContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except CertificateNotEligibleError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return _certificate_response(cert)


@admin_router.patch(
    "/enrollments/{user_id}/{slug}/deadline",
    response_model=EnrollmentResponse,
    response_model_by_alias=True,
)
async def set_enrollment_deadline(
    user_id: UUID,
    slug: str,
    body: SetDeadlineRequest,
    use_case: Annotated[SetEnrollmentDeadline, Depends(get_set_deadline_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> EnrollmentResponse:
    try:
        enrollment = await use_case.execute(user_id=user_id, path_slug=slug, due_at=body.due_at)
    except EnrollmentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _enrollment_response(enrollment)


# ── Admin catalogue CRUD: modules ────────────────────────────────────


@admin_router.get(
    "/modules",
    response_model=list[LearningModuleResponse],
    response_model_by_alias=True,
)
async def admin_list_modules(
    use_case: Annotated[ListModules, Depends(get_list_modules_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> list[LearningModuleResponse]:
    return [_module_response(m) for m in await use_case.execute()]


@admin_router.post(
    "/modules",
    response_model=LearningModuleResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def admin_create_module(
    body: CreateModuleRequest,
    use_case: Annotated[CreateModule, Depends(get_create_module_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> LearningModuleResponse:
    try:
        module = await use_case.execute(
            CreateModuleCommand(
                title=body.title,
                category=body.category,
                description=body.description,
                level=body.level,
                duration=body.duration,
                icon=body.icon,
                topics=tuple(body.topics),
                course_slugs=tuple(body.course_slugs),
                slug=body.slug,
            )
        )
    except LearningContentConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except LearningContentValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _module_response(module)


@admin_router.patch(
    "/modules/{slug}",
    response_model=LearningModuleResponse,
    response_model_by_alias=True,
)
async def admin_update_module(
    slug: str,
    body: UpdateModuleRequest,
    use_case: Annotated[UpdateModule, Depends(get_update_module_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> LearningModuleResponse:
    try:
        module = await use_case.execute(
            UpdateModuleCommand(
                slug=slug,
                title=body.title,
                category=body.category,
                description=body.description,
                level=body.level,
                duration=body.duration,
                icon=body.icon,
                topics=tuple(body.topics) if body.topics is not None else None,
                course_slugs=(tuple(body.course_slugs) if body.course_slugs is not None else None),
            )
        )
    except LearningContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except LearningContentValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _module_response(module)


@admin_router.delete("/modules/{slug}", status_code=204)
async def admin_delete_module(
    slug: str,
    use_case: Annotated[DeleteModule, Depends(get_delete_module_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> Response:
    try:
        await use_case.execute(slug)
    except LearningContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Response(status_code=204)


# ── Admin catalogue CRUD: paths ──────────────────────────────────────


@admin_router.get(
    "/paths",
    response_model=list[LearningPathResponse],
    response_model_by_alias=True,
)
async def admin_list_paths(
    use_case: Annotated[ListPaths, Depends(get_list_paths_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> list[LearningPathResponse]:
    return [_path_response(p) for p in await use_case.execute()]


@admin_router.post(
    "/paths",
    response_model=LearningPathResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def admin_create_path(
    body: CreatePathRequest,
    use_case: Annotated[CreatePath, Depends(get_create_path_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> LearningPathResponse:
    try:
        path = await use_case.execute(
            CreatePathCommand(
                title=body.title,
                description=body.description,
                module_slugs=tuple(body.module_slugs),
                estimated_time=body.estimated_time,
                icon=body.icon,
                slug=body.slug,
            )
        )
    except LearningContentConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except LearningContentValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _path_response(path)


@admin_router.patch(
    "/paths/{slug}",
    response_model=LearningPathResponse,
    response_model_by_alias=True,
)
async def admin_update_path(
    slug: str,
    body: UpdatePathRequest,
    use_case: Annotated[UpdatePath, Depends(get_update_path_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> LearningPathResponse:
    try:
        path = await use_case.execute(
            UpdatePathCommand(
                slug=slug,
                title=body.title,
                description=body.description,
                module_slugs=(tuple(body.module_slugs) if body.module_slugs is not None else None),
                estimated_time=body.estimated_time,
                icon=body.icon,
            )
        )
    except LearningContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except LearningContentValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _path_response(path)


@admin_router.delete("/paths/{slug}", status_code=204)
async def admin_delete_path(
    slug: str,
    use_case: Annotated[DeletePath, Depends(get_delete_path_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> Response:
    try:
        await use_case.execute(slug)
    except LearningContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Response(status_code=204)


@admin_router.post(
    "/paths/{slug}/modules/reorder",
    response_model=LearningPathResponse,
    response_model_by_alias=True,
)
async def admin_reorder_path_modules(
    slug: str,
    body: ReorderPathModulesRequest,
    use_case: Annotated[ReorderPathModules, Depends(get_reorder_path_modules_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> LearningPathResponse:
    try:
        path = await use_case.execute(slug=slug, module_slugs=tuple(body.module_slugs))
    except LearningContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except LearningContentValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _path_response(path)


# ── Admin translations (modules + paths) ─────────────────────────────


def _tr_response(t: LearningTranslation) -> TranslationResponse:
    return TranslationResponse(language=t.language, title=t.title, description=t.description)


@admin_router.get(
    "/modules/{slug}/translations",
    response_model=list[TranslationResponse],
    response_model_by_alias=True,
)
async def admin_list_module_translations(
    slug: str,
    use_case: Annotated[ListModuleTranslations, Depends(get_list_module_tr_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> list[TranslationResponse]:
    try:
        return [_tr_response(t) for t in await use_case.execute(slug)]
    except LearningContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@admin_router.put(
    "/modules/{slug}/translations/{language}",
    response_model=TranslationResponse,
    response_model_by_alias=True,
)
async def admin_upsert_module_translation(
    slug: str,
    language: str,
    body: TranslationUpsertRequest,
    use_case: Annotated[UpsertModuleTranslation, Depends(get_upsert_module_tr_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> TranslationResponse:
    try:
        tr = await use_case.execute(
            slug=slug, language=language, title=body.title, description=body.description
        )
    except LearningContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except LearningContentValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _tr_response(tr)


@admin_router.delete("/modules/{slug}/translations/{language}", status_code=204)
async def admin_delete_module_translation(
    slug: str,
    language: str,
    use_case: Annotated[DeleteModuleTranslation, Depends(get_delete_module_tr_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> Response:
    try:
        await use_case.execute(slug=slug, language=language)
    except LearningContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except LearningContentValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return Response(status_code=204)


@admin_router.get(
    "/paths/{slug}/translations",
    response_model=list[TranslationResponse],
    response_model_by_alias=True,
)
async def admin_list_path_translations(
    slug: str,
    use_case: Annotated[ListPathTranslations, Depends(get_list_path_tr_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> list[TranslationResponse]:
    try:
        return [_tr_response(t) for t in await use_case.execute(slug)]
    except LearningContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@admin_router.put(
    "/paths/{slug}/translations/{language}",
    response_model=TranslationResponse,
    response_model_by_alias=True,
)
async def admin_upsert_path_translation(
    slug: str,
    language: str,
    body: TranslationUpsertRequest,
    use_case: Annotated[UpsertPathTranslation, Depends(get_upsert_path_tr_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> TranslationResponse:
    try:
        tr = await use_case.execute(
            slug=slug, language=language, title=body.title, description=body.description
        )
    except LearningContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except LearningContentValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _tr_response(tr)


@admin_router.delete("/paths/{slug}/translations/{language}", status_code=204)
async def admin_delete_path_translation(
    slug: str,
    language: str,
    use_case: Annotated[DeletePathTranslation, Depends(get_delete_path_tr_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> Response:
    try:
        await use_case.execute(slug=slug, language=language)
    except LearningContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except LearningContentValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return Response(status_code=204)


__all__ = ["admin_router", "public_router"]
