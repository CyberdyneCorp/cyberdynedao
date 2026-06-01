"""Learning endpoints — public catalogue + authenticated state + admin
certificate issuance."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from cyberdyne_backend.adapters.inbound.api.learning.schemas import (
    CertificateResponse,
    EligibilityResponse,
    EnrollmentResponse,
    LearningModuleResponse,
    LearningPathResponse,
    ModuleGateResponse,
    ModuleProgressResponse,
    MyLearningStateResponse,
    UpdateProgressRequest,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import (
    require_editor,
    require_principal,
)
from cyberdyne_backend.application.learning import (
    CheckEnrollmentEligibility,
    EligibilityResult,
    EnrollInPath,
    GetMyLearningState,
    GetPathGating,
    IssueCertificate,
    ListModules,
    ListPaths,
    UpdateModuleProgress,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.learning import (
    Certificate,
    CertificateNotEligibleError,
    Enrollment,
    LearningContentNotFoundError,
    LearningModule,
    LearningPath,
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


async def get_path_gating_uc() -> GetPathGating:  # pragma: no cover - override target
    raise NotImplementedError


async def get_eligibility_uc() -> CheckEnrollmentEligibility:  # pragma: no cover - override target
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


# ── Public catalogue ─────────────────────────────────────────────────


@public_router.get(
    "/modules",
    response_model=list[LearningModuleResponse],
    response_model_by_alias=True,
)
async def list_modules(
    use_case: Annotated[ListModules, Depends(get_list_modules_uc)],
) -> list[LearningModuleResponse]:
    modules = await use_case.execute()
    return [_module_response(m) for m in modules]


@public_router.get(
    "/paths",
    response_model=list[LearningPathResponse],
    response_model_by_alias=True,
)
async def list_paths(
    use_case: Annotated[ListPaths, Depends(get_list_paths_uc)],
) -> list[LearningPathResponse]:
    paths = await use_case.execute()
    return [_path_response(p) for p in paths]


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


__all__ = ["admin_router", "public_router"]
