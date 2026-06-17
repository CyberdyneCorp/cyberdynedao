"""phase19 notebook flashcards (issue #161, part 2)

Revision ID: 202606170021
Revises: 202606170020
Create Date: 2026-06-17

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "202606170021"
down_revision: str | Sequence[str] | None = "202606170020"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "notebook_flashcards",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "note_id",
            sa.Uuid(),
            sa.ForeignKey("notebook_notes.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("answer", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_notebook_flashcards_note_id", "notebook_flashcards", ["note_id"]
    )


def downgrade() -> None:
    op.drop_index(
        "ix_notebook_flashcards_note_id", table_name="notebook_flashcards"
    )
    op.drop_table("notebook_flashcards")
