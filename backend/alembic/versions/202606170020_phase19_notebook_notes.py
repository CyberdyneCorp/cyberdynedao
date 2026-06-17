"""phase19 notebook notes — per-user living memory (issue #161, part 1)

Revision ID: 202606170020
Revises: 202606170019
Create Date: 2026-06-17

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "202606170020"
down_revision: str | Sequence[str] | None = "202606170019"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "notebook_notes",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("type", sa.String(length=16), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("course_slug", sa.String(length=128), nullable=True),
        sa.Column("lesson_id", sa.Uuid(), nullable=True),
        sa.Column("code", sa.Text(), nullable=True),
        sa.Column("language", sa.String(length=32), nullable=True),
        sa.Column("run_result", sa.JSON(), nullable=True),
        sa.Column("plot_refs", sa.JSON(), nullable=False),
        sa.Column("tags", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_notebook_notes_user_id", "notebook_notes", ["user_id"])
    op.create_index(
        "ix_notebook_notes_user_created", "notebook_notes", ["user_id", "created_at"]
    )


def downgrade() -> None:
    op.drop_index("ix_notebook_notes_user_created", table_name="notebook_notes")
    op.drop_index("ix_notebook_notes_user_id", table_name="notebook_notes")
    op.drop_table("notebook_notes")
