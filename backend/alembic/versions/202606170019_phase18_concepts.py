"""phase18 concepts — standalone concept cards library (issue #168)

Revision ID: 202606170019
Revises: 202606160015
Create Date: 2026-06-17

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "202606170019"
down_revision: str | Sequence[str] | None = "202606160015"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "concepts",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("slug", sa.String(length=96), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("domain", sa.String(length=64), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("formula", sa.Text(), nullable=True),
        sa.Column("related_lesson_ids", sa.JSON(), nullable=False),
        sa.Column("related_course_slugs", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("slug", name="uq_concepts_slug"),
    )
    op.create_index("ix_concepts_slug", "concepts", ["slug"])
    op.create_index("ix_concepts_domain", "concepts", ["domain"])


def downgrade() -> None:
    op.drop_index("ix_concepts_domain", table_name="concepts")
    op.drop_index("ix_concepts_slug", table_name="concepts")
    op.drop_table("concepts")
