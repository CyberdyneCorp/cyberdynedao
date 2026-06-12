"""Phase 14 — widen translated title columns to TEXT.

``course_translations.title`` / ``lesson_translations.title`` mirrored the
base ``VARCHAR(256)`` titles, but a translation is derived data and can be
longer than its English source (French/Spanish run longer; a model may also
return more than a bare title). An over-long value raised
``StringDataRightTruncationError`` and aborted the whole course's translation.
Translations don't need the length cap — store titles as TEXT.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202606120012"
down_revision: str | Sequence[str] | None = "202606120011"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # batch_alter_table so the type change also works on SQLite (recreates the
    # table); a plain ALTER COLUMN TYPE is fine on Postgres but SQLite can't.
    for table in ("course_translations", "lesson_translations"):
        with op.batch_alter_table(table) as batch_op:
            batch_op.alter_column("title", type_=sa.Text(), existing_nullable=False)


def downgrade() -> None:
    for table in ("course_translations", "lesson_translations"):
        with op.batch_alter_table(table) as batch_op:
            batch_op.alter_column(
                "title", type_=sa.String(length=256), existing_nullable=False
            )
