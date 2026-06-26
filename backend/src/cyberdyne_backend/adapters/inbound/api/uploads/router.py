"""Upload endpoints — admin write, public metadata read.

Files are streamed from the request in chunks and aborted the instant
they cross the hard global ceiling, so an oversized upload never buffers
fully in memory. The use case then applies the precise per-category cap.
"""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from cyberdyne_backend.adapters.inbound.api.uploads.schemas import (
    UploadListResponse,
    UploadResponse,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import require_editor, require_principal
from cyberdyne_backend.application.uploads import (
    GetUpload,
    SaveUpload,
    SaveUploads,
    UploadInput,
)
from cyberdyne_backend.domain.auth_identity import Principal, UserPrincipal
from cyberdyne_backend.domain.uploads import (
    MAX_UPLOAD_BYTES,
    FileTooLargeError,
    StoredFile,
    UnsafeFilenameError,
    UnsupportedMediaTypeError,
    UploadNotFoundError,
)

admin_router = APIRouter(prefix="/api/v1/admin/uploads", tags=["uploads-admin"])
public_router = APIRouter(prefix="/api/v1/uploads", tags=["uploads"])

_CHUNK = 1024 * 1024


# Dependency stubs — overridden in main.py.
async def get_save_upload_uc() -> SaveUpload:  # pragma: no cover - override target
    raise NotImplementedError


async def get_save_uploads_uc() -> SaveUploads:  # pragma: no cover - override target
    raise NotImplementedError


async def get_upload_uc() -> GetUpload:  # pragma: no cover - override target
    raise NotImplementedError


def _response(stored: StoredFile) -> UploadResponse:
    return UploadResponse(
        id=stored.id,
        original_filename=stored.original_filename,
        stored_filename=stored.stored_filename,
        category=stored.category.value,
        content_type=stored.content_type,
        size_bytes=stored.size_bytes,
        url=stored.url,
        uploaded_by=stored.uploaded_by,
        created_at=stored.created_at,
    )


async def _read_capped(upload: UploadFile, max_bytes: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = await upload.read(_CHUNK)
        if not chunk:
            break
        total += len(chunk)
        if total > max_bytes:
            raise HTTPException(status_code=413, detail="file exceeds maximum upload size")
        chunks.append(chunk)
    return b"".join(chunks)


async def _to_input(upload: UploadFile) -> UploadInput:
    data = await _read_capped(upload, MAX_UPLOAD_BYTES)
    return UploadInput(
        filename=upload.filename or "upload",
        content_type=upload.content_type or "application/octet-stream",
        data=data,
    )


def _map_domain_error(exc: Exception) -> HTTPException:
    if isinstance(exc, UnsupportedMediaTypeError):
        return HTTPException(status_code=415, detail=f"unsupported media type: {exc}")
    if isinstance(exc, FileTooLargeError):
        return HTTPException(status_code=413, detail=str(exc))
    if isinstance(exc, UnsafeFilenameError):
        return HTTPException(status_code=422, detail=f"unsafe filename: {exc}")
    raise exc


# ── Admin write ──────────────────────────────────────────────────────


@admin_router.post(
    "",
    response_model=UploadResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def upload_file(
    use_case: Annotated[SaveUpload, Depends(get_save_upload_uc)],
    principal: Annotated[UserPrincipal, Depends(require_editor)],
    file: Annotated[UploadFile, File()],
) -> UploadResponse:
    item = await _to_input(file)
    try:
        stored = await use_case.execute(item, uploaded_by=principal.user_id)
    except (UnsupportedMediaTypeError, FileTooLargeError, UnsafeFilenameError) as exc:
        raise _map_domain_error(exc) from exc
    return _response(stored)


@admin_router.post(
    "/batch",
    response_model=UploadListResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def upload_files(
    use_case: Annotated[SaveUploads, Depends(get_save_uploads_uc)],
    principal: Annotated[UserPrincipal, Depends(require_editor)],
    files: Annotated[list[UploadFile], File()],
) -> UploadListResponse:
    items = [await _to_input(f) for f in files]
    try:
        stored = await use_case.execute(items, uploaded_by=principal.user_id)
    except (UnsupportedMediaTypeError, FileTooLargeError, UnsafeFilenameError) as exc:
        raise _map_domain_error(exc) from exc
    return UploadListResponse(items=[_response(s) for s in stored])


# ── Learner write ────────────────────────────────────────────────────


@public_router.post(
    "",
    response_model=UploadResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def learner_upload_file(
    use_case: Annotated[SaveUpload, Depends(get_save_upload_uc)],
    principal: Annotated[Principal, Depends(require_principal)],
    file: Annotated[UploadFile, File()],
) -> UploadResponse:
    """A signed-in learner attaches a file (PDF/DOCX/CSV/XLSX/image) for the
    AI tutor to read. Reuses the same save-upload use case as the admin
    endpoint; only the allow-list + per-category caps gate the bytes."""
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    item = await _to_input(file)
    try:
        stored = await use_case.execute(item, uploaded_by=principal.user_id)
    except (UnsupportedMediaTypeError, FileTooLargeError, UnsafeFilenameError) as exc:
        raise _map_domain_error(exc) from exc
    return _response(stored)


# ── Public metadata read ─────────────────────────────────────────────


@public_router.get(
    "/{upload_id}",
    response_model=UploadResponse,
    response_model_by_alias=True,
)
async def get_upload(
    upload_id: UUID,
    use_case: Annotated[GetUpload, Depends(get_upload_uc)],
) -> UploadResponse:
    try:
        stored = await use_case.execute(upload_id)
    except UploadNotFoundError as exc:
        raise HTTPException(status_code=404, detail="upload not found") from exc
    return _response(stored)


__all__ = ["admin_router", "public_router"]
