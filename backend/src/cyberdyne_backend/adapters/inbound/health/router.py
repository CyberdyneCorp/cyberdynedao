"""Health / readiness endpoints.

`/healthz` is for liveness probes (Coolify, Kubernetes). It must stay
trivially cheap — no DB call, no upstream check — so a hung dependency
never causes the container to be killed.

`/readyz` is for readiness probes. Once Phase 1.5 lands real
dependencies (Postgres, CyberdyneAuth), this is where their probes go.
"""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from cyberdyne_backend import __version__

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: str
    version: str


@router.get("/healthz", response_model=HealthResponse)
async def liveness() -> HealthResponse:
    return HealthResponse(status="ok", version=__version__)


@router.get("/readyz", response_model=HealthResponse)
async def readiness() -> HealthResponse:
    # Phase 1.5: extend with Postgres + CyberdyneAuth introspection probes.
    return HealthResponse(status="ready", version=__version__)
