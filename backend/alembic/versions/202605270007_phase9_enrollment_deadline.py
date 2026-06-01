"""Phase 9 — enrollment deadlines.

Adds a nullable ``due_at`` to ``enrollments`` so an enrollment can carry
a deadline; status (overdue / urgent / upcoming) is computed in the
domain from ``due_at`` vs now.

Revision ID: 202605270007
Revises: 202605270006
Create Date: 2026-06-01 01:00:00
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202605270007"
down_revision: str | Sequence[str] | None = "202605270006"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "enrollments",
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("enrollments", "due_at")
