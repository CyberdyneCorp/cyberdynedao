"""Phase 13 — Academy content translations (i18n).

Adds per-language translation tables for course/lesson/quiz content so the
Academy can be served in multiple languages with English fallback. The base
``courses``/``lessons``/``quiz_questions``/``quiz_options`` rows remain the
English source of truth; a translation row carries the localized fields for
one ``(entity, language)`` pair plus a ``source_hash`` of the English source
captured at translation time (lets the seeder skip unchanged content).

Revision ID: 202606120011
Revises: 202605270010
Create Date: 2026-06-12 09:00:00
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202606120011"
down_revision: str | Sequence[str] | None = "202605270010"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "course_translations",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "course_id",
            sa.Uuid(),
            sa.ForeignKey("courses.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("language", sa.String(length=8), nullable=False),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("source_hash", sa.String(length=64), nullable=False),
        sa.UniqueConstraint("course_id", "language", name="uq_course_tr_course_lang"),
    )
    op.create_index(
        "ix_course_translations_course_lang", "course_translations", ["course_id", "language"]
    )

    op.create_table(
        "lesson_translations",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "lesson_id",
            sa.Uuid(),
            sa.ForeignKey("lessons.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("language", sa.String(length=8), nullable=False),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column("text_body", sa.Text(), nullable=True),
        sa.Column("source_hash", sa.String(length=64), nullable=False),
        sa.UniqueConstraint("lesson_id", "language", name="uq_lesson_tr_lesson_lang"),
    )
    op.create_index(
        "ix_lesson_translations_lesson_lang", "lesson_translations", ["lesson_id", "language"]
    )

    op.create_table(
        "quiz_question_translations",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "question_id",
            sa.Uuid(),
            sa.ForeignKey("quiz_questions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("language", sa.String(length=8), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False, server_default=""),
        sa.Column("source_hash", sa.String(length=64), nullable=False),
        sa.UniqueConstraint(
            "question_id", "language", name="uq_quiz_question_tr_question_lang"
        ),
    )
    op.create_index(
        "ix_quiz_question_tr_question_lang",
        "quiz_question_translations",
        ["question_id", "language"],
    )

    op.create_table(
        "quiz_option_translations",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "option_id",
            sa.Uuid(),
            sa.ForeignKey("quiz_options.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("language", sa.String(length=8), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("source_hash", sa.String(length=64), nullable=False),
        sa.UniqueConstraint("option_id", "language", name="uq_quiz_option_tr_option_lang"),
    )
    op.create_index(
        "ix_quiz_option_tr_option_lang",
        "quiz_option_translations",
        ["option_id", "language"],
    )


def downgrade() -> None:
    op.drop_index("ix_quiz_option_tr_option_lang", table_name="quiz_option_translations")
    op.drop_table("quiz_option_translations")
    op.drop_index("ix_quiz_question_tr_question_lang", table_name="quiz_question_translations")
    op.drop_table("quiz_question_translations")
    op.drop_index("ix_lesson_translations_lesson_lang", table_name="lesson_translations")
    op.drop_table("lesson_translations")
    op.drop_index("ix_course_translations_course_lang", table_name="course_translations")
    op.drop_table("course_translations")
