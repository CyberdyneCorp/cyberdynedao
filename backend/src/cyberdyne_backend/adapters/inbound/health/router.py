"""Health / readiness endpoints.

`/healthz` is for liveness probes (Coolify, Kubernetes). It stays
trivially cheap — no DB call, no upstream check — so a hung dependency
never causes the container to be killed.

`/readyz` is for readiness probes. It probes the local Postgres with
``SELECT 1``; if that fails the container reports 503 and Traefik
routes around it until the DB is reachable.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import text

from cyberdyne_backend import __version__
from cyberdyne_backend.infrastructure.database.engine import session_scope

logger = logging.getLogger("cyberdyne_backend.health")

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: str
    version: str


@router.get("/healthz", response_model=HealthResponse)
async def liveness() -> HealthResponse:
    return HealthResponse(status="ok", version=__version__)


@router.get(
    "/readyz",
    response_model=HealthResponse,
    responses={503: {"model": HealthResponse}},
)
async def readiness() -> JSONResponse:
    try:
        async with session_scope() as session:
            await session.execute(text("SELECT 1"))
    except Exception as exc:
        logger.warning("readiness DB probe failed: %s", exc)
        return JSONResponse(
            status_code=503,
            content=HealthResponse(status="degraded:db", version=__version__).model_dump(),
        )
    return JSONResponse(
        status_code=200,
        content=HealthResponse(status="ready", version=__version__).model_dump(),
    )
