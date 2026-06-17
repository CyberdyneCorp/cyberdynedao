"""phase18 bookmarks — favorites + recently-viewed (issue #162)

Revision ID: 202606170016
Revises: 202606160015
Create Date: 2026-06-17

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "202606170016"
down_revision: str | Sequence[str] | None = "202606160015"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "favorites",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("type", sa.String(length=16), nullable=False),
        sa.Column("ref", sa.String(length=128), nullable=False),
        sa.Column("added_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "user_id", "type", "ref", name="uq_favorite_user_type_ref"
        ),
    )
    op.create_index("ix_favorites_user_id", "favorites", ["user_id"])

    op.create_table(
        "recent_views",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("type", sa.String(length=16), nullable=False),
        sa.Column("ref", sa.String(length=128), nullable=False),
        sa.Column("viewed_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "user_id", "type", "ref", name="uq_recent_user_type_ref"
        ),
    )
    op.create_index("ix_recent_views_user_id", "recent_views", ["user_id"])
    op.create_index("ix_recent_views_viewed_at", "recent_views", ["viewed_at"])


def downgrade() -> None:
    op.drop_index("ix_recent_views_viewed_at", table_name="recent_views")
    op.drop_index("ix_recent_views_user_id", table_name="recent_views")
    op.drop_table("recent_views")
    op.drop_index("ix_favorites_user_id", table_name="favorites")
    op.drop_table("favorites")
