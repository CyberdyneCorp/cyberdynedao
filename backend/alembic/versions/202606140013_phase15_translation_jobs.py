"""Phase 15 — durable translation job queue.

Adds the ``translation_jobs`` table backing a restart-safe translation
worker. The per-course translate endpoint used to run translation inside an
in-process FastAPI background task, which a container restart/redeploy would
kill mid-run — truncating a course's lesson translations. A durable queue
row survives the restart; the worker requeues any ``running`` job on startup
and resumes it (translation is idempotent by ``source_hash``, so a re-run
only fills gaps).

Revision ID: 202606140013
Revises: 202606120012
Create Date: 2026-06-14 09:00:00
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202606140013"
down_revision: str | Sequence[str] | None = "202606120012"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "translation_jobs",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("course_slug", sa.String(length=128), nullable=False),
        sa.Column("language", sa.String(length=8), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="pending"),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("course_slug", "language", name="uq_translation_jobs_slug_lang"),
    )
    op.create_index(
        "ix_translation_jobs_status_created",
        "translation_jobs",
        ["status", "created_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_translation_jobs_status_created", table_name="translation_jobs")
    op.drop_table("translation_jobs")
