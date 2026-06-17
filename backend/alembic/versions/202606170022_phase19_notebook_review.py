"""phase19 notebook spaced review (issue #161, part 3)

Revision ID: 202606170022
Revises: 202606170021
Create Date: 2026-06-17

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "202606170022"
down_revision: str | Sequence[str] | None = "202606170021"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "notebook_notes",
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "notebook_notes",
        sa.Column("next_review_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "notebook_notes",
        sa.Column(
            "review_interval_days",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )
    op.create_index(
        "ix_notebook_notes_user_next_review",
        "notebook_notes",
        ["user_id", "next_review_at"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_notebook_notes_user_next_review", table_name="notebook_notes"
    )
    op.drop_column("notebook_notes", "review_interval_days")
    op.drop_column("notebook_notes", "next_review_at")
    op.drop_column("notebook_notes", "reviewed_at")
