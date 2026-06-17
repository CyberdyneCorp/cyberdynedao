"""phase19 notebook ai_summary (issue #187)

Revision ID: 202606170023
Revises: 202606170022
Create Date: 2026-06-17

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "202606170023"
down_revision: str | Sequence[str] | None = "202606170022"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "notebook_notes",
        sa.Column("ai_summary", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("notebook_notes", "ai_summary")
