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

COPY pyproject.toml uv.lock* alembic.ini ./
COPY src/ src/
COPY alembic/ alembic/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Non-root runtime user. Pre-create the media dir owned by appuser so the
# uploads_data named volume (mounted at /data/uploads) initialises with
# appuser ownership and is writable by the non-root process.
RUN adduser --disabled-password --gecos '' appuser && \
    mkdir -p /data/uploads && \
    chown -R appuser:appuser /app /data
USER appuser

EXPOSE 8000

# Coolify trap: `wget -qO-` and `localhost` (DNS) both fail silently inside
# slim Alpine/Debian — use a Python one-liner against 127.0.0.1 instead.
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=5).status == 200 else 1)"

# On container start: apply migrations, provision the version-controlled
# Academy catalogue, then exec uvicorn so SIGTERM reaches it for graceful
# shutdown. The seed (application.courses.seed) is idempotent and
# non-destructive, so running it every boot just reconciles content; it's
# wrapped so a seed failure logs and still lets the API come up. The wider
# `start-period=40s` gives Alembic + the seed room before Traefik probes us.
CMD ["sh", "-c", "alembic upgrade head && (python -m cyberdyne_backend.cli.seed_academy || echo 'academy seed failed; continuing boot') && exec uvicorn cyberdyne_backend.main:app --host 0.0.0.0 --port 8000"]
