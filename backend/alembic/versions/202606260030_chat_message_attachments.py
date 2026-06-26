"""attachments column on chat_messages for AI tutor file attachments (issue #220)

Revision ID: 202606260030
Revises: 202606260029
Create Date: 2026-06-26

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "202606260030"
down_revision: str | Sequence[str] | None = "202606260029"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("chat_messages", sa.Column("attachments", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("chat_messages", "attachments")
