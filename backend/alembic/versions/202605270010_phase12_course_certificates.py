"""Phase 12 — course completion certificates.

Adds the ``course_certificates`` table: one signed certificate per
(user, course), minted when the learner has completed every lesson.
Distinct from the path-keyed ``certificates`` table (learning context).

Revision ID: 202605270010
Revises: 202605270009
Create Date: 2026-06-02 03:00:00
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202605270010"
down_revision: str | Sequence[str] | None = "202605270009"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "course_certificates",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("course_slug", sa.String(length=128), nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("verification_hash", sa.String(length=128), nullable=False),
        sa.Column("signed_payload", sa.Text(), nullable=False),
        sa.UniqueConstraint("user_id", "course_slug", name="uq_course_cert_user_course"),
    )
    op.create_index(
        "ix_course_certificates_user_id", "course_certificates", ["user_id"]
    )


def downgrade() -> None:
    op.drop_index("ix_course_certificates_user_id", table_name="course_certificates")
    op.drop_table("course_certificates")
