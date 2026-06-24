"""Course-backed learning modules.

Adds ``course_slugs`` (JSON list) to ``learning_modules`` so a module
(stage) can bundle one or more real courses. Existing rows backfill to an
empty list — they keep the legacy self-reported progress behaviour.

Revision ID: 202606170025
Revises: 202606170024
Create Date: 2026-06-24 12:00:00
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202606170025"
down_revision: str | Sequence[str] | None = "202606170024"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "learning_modules",
        sa.Column(
            "course_slugs",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'[]'"),
        ),
    )


def downgrade() -> None:
    op.drop_column("learning_modules", "course_slugs")
