"""Phase 11 — course-level deadline.

Adds a nullable ``due_at`` to ``courses`` so a course can carry a
completion deadline; the overdue / urgent / upcoming status is derived
in the read layer from ``due_at`` vs now (same semantics as enrollment
deadlines).

Revision ID: 202605270009
Revises: 202605270008
Create Date: 2026-06-02 02:00:00
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202605270009"
down_revision: str | Sequence[str] | None = "202605270008"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "courses",
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("courses", "due_at")
