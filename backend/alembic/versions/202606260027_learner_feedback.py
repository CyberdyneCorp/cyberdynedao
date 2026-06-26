"""learner feedback channel — problem reports + feature requests (issue #233)

Revision ID: 202606260027
Revises: 202606170026
Create Date: 2026-06-26

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "202606260027"
down_revision: str | Sequence[str] | None = "202606170026"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "feedback",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("kind", sa.String(length=16), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("course_id", sa.String(length=128), nullable=True),
        sa.Column("lesson_id", sa.String(length=128), nullable=True),
        sa.Column("app_version", sa.String(length=64), nullable=True),
        sa.Column("platform", sa.String(length=32), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_feedback_user_id", "feedback", ["user_id"])
    op.create_index("ix_feedback_created_at", "feedback", ["created_at"])
    op.create_index("ix_feedback_kind_status", "feedback", ["kind", "status"])


def downgrade() -> None:
    op.drop_index("ix_feedback_kind_status", table_name="feedback")
    op.drop_index("ix_feedback_created_at", table_name="feedback")
    op.drop_index("ix_feedback_user_id", table_name="feedback")
    op.drop_table("feedback")
