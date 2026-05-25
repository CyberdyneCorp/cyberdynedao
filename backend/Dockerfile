# syntax=docker/dockerfile:1.4
#
# Multi-stage build for the Cyberdyne backend. Follows the proven
# pattern from geo_dashboard/backend — `uv` with --frozen, UV_LINK_MODE=copy
# (critical on Coolify, otherwise `ModuleNotFoundError` at runtime despite a
# green build), and a non-root runtime user.

# Stage 1: Base with uv
FROM python:3.12-slim AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Stage 2: Dependencies (cached layer; only re-runs when pyproject/uv.lock change)
FROM base AS deps

COPY pyproject.toml uv.lock* ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# Stage 3: Production
FROM base AS production

COPY --from=deps /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml uv.lock* ./
COPY src/ src/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Non-root runtime user
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Coolify trap: `wget -qO-` and `localhost` (DNS) both fail silently inside
# slim Alpine/Debian — use a Python one-liner against 127.0.0.1 instead.
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=5).status == 200 else 1)"

# `exec` form so SIGTERM reaches uvicorn for graceful shutdown
CMD ["uvicorn", "cyberdyne_backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
