"""per-user usage counters for quota / fair-use enforcement (issue #230)

Revision ID: 202606260029
Revises: 202606260028
Create Date: 2026-06-26

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "202606260029"
down_revision: str | Sequence[str] | None = "202606260028"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "usage_counters",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("meter", sa.String(length=32), nullable=False),
        sa.Column("period_key", sa.String(length=16), nullable=False),
        sa.Column("count", sa.Integer(), nullable=False, server_default="0"),
        sa.UniqueConstraint(
            "user_id", "meter", "period_key", name="uq_usage_user_meter_period"
        ),
    )
    op.create_index("ix_usage_counters_user_id", "usage_counters", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_usage_counters_user_id", table_name="usage_counters")
    op.drop_table("usage_counters")
