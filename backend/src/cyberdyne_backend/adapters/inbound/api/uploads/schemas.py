"""Pydantic schemas for upload endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


CategoryLiteral = Literal["image", "document", "presentation", "video"]


class UploadResponse(_CamelModel):
    id: UUID
    original_filename: str
    stored_filename: str
    category: CategoryLiteral
    content_type: str
    size_bytes: int
    url: str
    uploaded_by: UUID | None = None
    created_at: datetime
    # Always "stored" today — the upload is durably persisted before the
    # response is returned. Reserved for future async/virus-scan states.
    status: str = "stored"


class UploadListResponse(_CamelModel):
    items: list[UploadResponse]
