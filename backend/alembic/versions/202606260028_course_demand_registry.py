"""course/topic demand registry — captured learner course requests (issue #232)

Revision ID: 202606260028
Revises: 202606260027
Create Date: 2026-06-26

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "202606260028"
down_revision: str | Sequence[str] | None = "202606260027"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "course_requests",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("topic", sa.String(length=256), nullable=False),
        sa.Column("topic_key", sa.String(length=256), nullable=False),
        sa.Column("subject", sa.String(length=128), nullable=True),
        sa.Column("source", sa.String(length=16), nullable=False),
        sa.Column("source_question_text", sa.Text(), nullable=True),
        sa.Column("course_id", sa.String(length=128), nullable=True),
        sa.Column("lesson_id", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_course_requests_user_id", "course_requests", ["user_id"])
    op.create_index("ix_course_requests_topic_key", "course_requests", ["topic_key"])
    op.create_index("ix_course_requests_created_at", "course_requests", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_course_requests_created_at", table_name="course_requests")
    op.drop_index("ix_course_requests_topic_key", table_name="course_requests")
    op.drop_index("ix_course_requests_user_id", table_name="course_requests")
    op.drop_table("course_requests")
