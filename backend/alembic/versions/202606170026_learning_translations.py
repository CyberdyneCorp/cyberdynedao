"""Learning path/module translations.

Adds ``learning_module_translations`` and ``learning_path_translations`` so a
module (stage) and a path can carry localized title/description per language,
mirroring ``course_translations``. English stays in the base rows.

Revision ID: 202606170026
Revises: 202606170025
Create Date: 2026-06-24 17:00:00
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202606170026"
down_revision: str | Sequence[str] | None = "202606170025"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "learning_module_translations",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "module_slug",
            sa.String(length=64),
            sa.ForeignKey("learning_modules.slug", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("language", sa.String(length=8), nullable=False),
        sa.Column("title", sa.Text(), nullable=False, server_default=""),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.UniqueConstraint("module_slug", "language", name="uq_learning_module_tr"),
    )
    op.create_table(
        "learning_path_translations",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "path_slug",
            sa.String(length=64),
            sa.ForeignKey("learning_paths.slug", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("language", sa.String(length=8), nullable=False),
        sa.Column("title", sa.Text(), nullable=False, server_default=""),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.UniqueConstraint("path_slug", "language", name="uq_learning_path_tr"),
    )


def downgrade() -> None:
    op.drop_table("learning_path_translations")
    op.drop_table("learning_module_translations")
