"""Interactive code-interpreter endpoint — runs a code lesson's source on
the MATLAB-LLVM engine as the signed-in learner."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request

from cyberdyne_backend.adapters.inbound.api.code.schemas import (
    CodeVariableView,
    RichOutputView,
    RunCodeRequest,
    RunCodeResponse,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import extract_token, require_principal
from cyberdyne_backend.application.code import RunLessonCode
from cyberdyne_backend.domain.auth_identity import UserPrincipal

player_router = APIRouter(prefix="/api/v1/lessons", tags=["code"])


# Dependency stub — overridden in main.py.
async def get_run_code_uc() -> RunLessonCode:  # pragma: no cover - override target
    raise NotImplementedError


@player_router.post(
    "/{lesson_id}/code/run",
    response_model=RunCodeResponse,
    response_model_by_alias=True,
)
async def run_lesson_code(
    lesson_id: UUID,
    body: RunCodeRequest,
    request: Request,
    use_case: Annotated[RunLessonCode, Depends(get_run_code_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> RunCodeResponse:
    # Signed-in learners only — execution runs in their per-(lesson,user)
    # MATLAB workspace, keyed off their bearer.
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    res = await use_case.execute(
        lesson_id=lesson_id,
        source=body.source,
        user_id=principal.user_id,
        bearer=extract_token(request),
        language=body.language,
    )
    return RunCodeResponse(
        ok=res.ok,
        stdout=res.stdout,
        stderr=res.stderr,
        artifacts=list(res.artifacts),
        session_id=res.session_id,
        timed_out=res.timed_out,
        variables=[
            CodeVariableView(name=v.name, type=v.type, repr=v.repr, size_bytes=v.size_bytes)
            for v in res.variables
        ],
        rich_outputs=[
            RichOutputView(mime_type=o.mime_type, artifact=o.artifact, text=o.text)
            for o in res.rich_outputs
        ],
    )


__all__ = ["player_router"]
