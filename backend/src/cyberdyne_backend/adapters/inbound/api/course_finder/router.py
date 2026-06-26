"""Scan-to-Learn endpoint (issue #231).

``POST /api/v1/learning/scan`` takes a photographed question, runs a vision step
to extract ``{question, subject, keywords}``, embeds the query, and matches it
(cosine) against the embedded course/lesson catalog. High-confidence hits return
ranked ``CourseMatch`` (with a deep-linkable lesson); a below-threshold scan
returns a no-match carrying the extracted query so the client can offer to
request the course. The scan counts toward the SCANS quota. The image is
analyzed only — never retained.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from cyberdyne_backend.adapters.inbound.api.course_finder.schemas import (
    CourseMatchSchema,
    ScanQuerySchema,
    ScanResponse,
)
from cyberdyne_backend.adapters.inbound.api.quota.dependencies import QuotaGuard
from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.application.course_finder import ScanResult, ScanToLearn
from cyberdyne_backend.domain.auth_identity import Principal
from cyberdyne_backend.domain.quota import QuotaMeter
from cyberdyne_backend.domain.uploads import UnsupportedMediaTypeError, UploadCategory, classify

public_router = APIRouter(prefix="/api/v1/learning", tags=["learning"])

_CHUNK = 1024 * 1024


async def get_scan_to_learn_uc() -> ScanToLearn:  # pragma: no cover - override target
    raise NotImplementedError


def _image_cap_bytes(content_type: str) -> int:
    """Validate the content type is a supported image and return its size cap.

    Reuses the uploads MIME allow-list + per-category caps. Non-image media
    (PDF, video, …) and unknown types are rejected with 415."""
    try:
        classification = classify(content_type)
    except UnsupportedMediaTypeError as exc:
        raise HTTPException(status_code=415, detail=f"unsupported media type: {exc}") from exc
    if classification.category is not UploadCategory.IMAGE:
        raise HTTPException(status_code=415, detail=f"scan requires an image, got {content_type}")
    return classification.max_bytes


async def _read_capped(upload: UploadFile, max_bytes: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = await upload.read(_CHUNK)
        if not chunk:
            break
        total += len(chunk)
        if total > max_bytes:
            raise HTTPException(status_code=413, detail="image exceeds maximum size")
        chunks.append(chunk)
    return b"".join(chunks)


def _response(result: ScanResult) -> ScanResponse:
    return ScanResponse(
        query=ScanQuerySchema(
            question=result.query.question,
            subject=result.query.subject,
            keywords=list(result.query.keywords),
        ),
        matches=[
            CourseMatchSchema(
                course_slug=m.course_slug,
                lesson_id=m.lesson_id,
                score=m.score,
                match_reason=m.match_reason,
            )
            for m in result.matches
        ],
        no_match=result.no_match,
    )


@public_router.post(
    "/scan",
    response_model=ScanResponse,
    response_model_by_alias=True,
    dependencies=[Depends(QuotaGuard(QuotaMeter.SCANS))],
)
async def scan_to_learn(
    file: Annotated[UploadFile, File()],
    use_case: Annotated[ScanToLearn, Depends(get_scan_to_learn_uc)],
    _principal: Annotated[Principal, Depends(require_principal)],
) -> ScanResponse:
    content_type = (file.content_type or "").strip()
    cap = _image_cap_bytes(content_type)
    image_bytes = await _read_capped(file, cap)
    result = await use_case.execute(image_bytes=image_bytes, content_type=content_type)
    return _response(result)
