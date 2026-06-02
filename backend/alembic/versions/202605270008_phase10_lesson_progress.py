"""Phase 10 — per-lesson learner progress (courses context).

Adds the ``lesson_progress`` table: a learner's percent + completion per
lesson, keyed uniquely by ``(user_id, lesson_id)``. Per-course
completion is derived (complete iff every lesson is), so no course-level
progress column is needed. Distinct from the Phase 4 ``learning``
module progress, which tracks a separate slug-keyed catalogue.

Revision ID: 202605270008
Revises: 202605270007
Create Date: 2026-06-02 00:00:00
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202605270008"
down_revision: str | Sequence[str] | None = "202605270007"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "lesson_progress",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column(
            "course_id",
            sa.Uuid(),
            sa.ForeignKey("courses.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "lesson_id",
            sa.Uuid(),
            sa.ForeignKey("lessons.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("percent", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("user_id", "lesson_id", name="uq_lesson_progress_user_lesson"),
    )
    op.create_index(
        "ix_lesson_progress_user_course", "lesson_progress", ["user_id", "course_id"]
    )


def downgrade() -> None:
    op.drop_index("ix_lesson_progress_user_course", table_name="lesson_progress")
    op.drop_table("lesson_progress")
