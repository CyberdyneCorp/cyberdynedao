"""phase20 lesson notes — per-user lesson annotations (issue #188)

Revision ID: 202606170024
Revises: 202606170023
Create Date: 2026-06-17

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "202606170024"
down_revision: str | Sequence[str] | None = "202606170023"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "lesson_notes",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("course_slug", sa.String(length=128), nullable=False),
        sa.Column("lesson_id", sa.String(length=128), nullable=False),
        sa.Column("quote", sa.Text(), nullable=True),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_lesson_notes_user_id", "lesson_notes", ["user_id"])
    op.create_index(
        "ix_lesson_notes_user_lesson", "lesson_notes", ["user_id", "lesson_id"]
    )
    op.create_index(
        "ix_lesson_notes_user_course_created",
        "lesson_notes",
        ["user_id", "course_slug", "created_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_lesson_notes_user_course_created", table_name="lesson_notes")
    op.drop_index("ix_lesson_notes_user_lesson", table_name="lesson_notes")
    op.drop_index("ix_lesson_notes_user_id", table_name="lesson_notes")
    op.drop_table("lesson_notes")
