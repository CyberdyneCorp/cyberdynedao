"""Phase 8 — uploads (stored-media metadata).

Adds the ``uploads`` table tracking admin-uploaded course/lesson media.
The bytes live on disk (local volume / persistent mount); this table is
the queryable record + public URL.

Revision ID: 202605270006u
Revises: 202605270005
Create Date: 2026-06-01 00:45:00
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202605270006u"
down_revision: str | Sequence[str] | None = "202605270005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "uploads",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("original_filename", sa.String(length=256), nullable=False),
        sa.Column("stored_filename", sa.String(length=128), nullable=False, unique=True),
        sa.Column("category", sa.String(length=32), nullable=False),
        sa.Column("content_type", sa.String(length=128), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
        sa.Column("relative_path", sa.Text(), nullable=False),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("uploaded_by", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_uploads_category", "uploads", ["category"])
    op.create_index("ix_uploads_uploaded_by", "uploads", ["uploaded_by"])


def downgrade() -> None:
    op.drop_index("ix_uploads_uploaded_by", table_name="uploads")
    op.drop_index("ix_uploads_category", table_name="uploads")
    op.drop_table("uploads")
