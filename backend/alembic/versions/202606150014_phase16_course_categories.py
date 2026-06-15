"""Phase 16 — course categories (stored, not slug-derived).

Adds a ``categories`` table and a nullable ``courses.category_id`` (FK,
``ON DELETE SET NULL`` so removing a category never deletes its courses).

Categories used to exist only as a frontend convention derived from the course
slug prefix. This makes them real data an editor can create/rename/delete and
assign. To preserve the current public grouping exactly, the upgrade seeds the
built-in categories and backfills every existing course's ``category_id`` using
the same slug-prefix mapping the frontend used (``courseTopic``). Courses that
mapped to no topic (the "Other" bucket) stay NULL/uncategorized.

Revision ID: 202606150014
Revises: 202606140013
Create Date: 2026-06-15 09:00:00
"""

from __future__ import annotations

import re
import uuid
from collections.abc import Sequence
from datetime import UTC, datetime

import sqlalchemy as sa
from alembic import op

revision: str = "202606150014"
down_revision: str | Sequence[str] | None = "202606140013"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


# Built-in categories: (slug, name, icon). Order is the display order.
_CATEGORIES: tuple[tuple[str, str, str], ...] = (
    ("foundations", "Foundations", "🎯"),
    ("languages", "Languages", "💻"),
    ("databases", "Databases", "🗄️"),
    ("devops", "DevOps", "⚙️"),
    ("blockchain", "Blockchain", "⛓️"),
    ("physics", "Physics", "⚛️"),
    ("mathematics", "Mathematics", "➗"),
    ("ai-machine-learning", "AI / Machine Learning", "🧠"),
    ("robotics", "Robotics", "🤖"),
    ("algorithms", "Algorithms", "🧮"),
    ("software-engineering", "Software Engineering", "🧰"),
    ("web-development", "Web Development", "🌍"),
    ("system-design", "System Design", "🏗️"),
    ("distributed-systems", "Distributed Systems", "🕸️"),
    ("data-engineering", "Data Engineering", "🏭"),
    ("concurrency-parallelism", "Concurrency & Parallelism", "⚡"),
    ("operating-systems", "Operating Systems", "🖥️"),
    ("networking", "Networking", "🌐"),
    ("cybersecurity", "Cybersecurity", "🔒"),
    ("computer-architecture", "Computer Architecture", "🏛️"),
    ("electronic-engineering", "Electronic Engineering", "🔌"),
)

_EE_RE = re.compile(
    r"^(electronics|analog-ic|antennas|power-electronics|pcb|semiconductor|embedded|signals|"
    r"signal-integrity|control|dsp|rf-comms|microwave|digital-comms|digital-logic|fpga|"
    r"electromagnetics|emc|test-measurement|hw-verification|vlsi|photonics|power-systems|"
    r"battery|sensors|machines)-"
)


def _category_slug_for(slug: str) -> str | None:
    """Mirror of the frontend ``courseTopic(slug)`` mapping (returns the
    category slug, or None for the 'Other' bucket)."""
    if slug.startswith("comparch-") or slug.startswith("sysverilog-"):
        return "computer-architecture"
    if slug.startswith("ml-") or slug.startswith("transformers"):
        return "ai-machine-learning"
    if slug.startswith("security-"):
        return "cybersecurity"
    if slug.startswith("os-"):
        return "operating-systems"
    if slug.startswith("networking-"):
        return "networking"
    if slug.startswith("system-design-"):
        return "system-design"
    if slug.startswith("distributed-"):
        return "distributed-systems"
    if slug.startswith("webdev-"):
        return "web-development"
    if slug.startswith("dataeng-"):
        return "data-engineering"
    if slug.startswith("concurrency-"):
        return "concurrency-parallelism"
    if slug.startswith("git-") or slug.startswith("testing-"):
        return "software-engineering"
    if re.match(r"^(c|cpp|swift|go|rust|javascript|typescript)-", slug):
        return "languages"
    if slug in ("sql-basics", "sql-intermediate", "mongodb", "postgresql"):
        return "databases"
    if re.match(r"^(docker|kubernetes|terraform|ansible)-", slug):
        return "devops"
    if slug.startswith("blockchain"):
        return "blockchain"
    if slug.startswith("physics"):
        return "physics"
    if slug.startswith("vectorcalc") or slug.startswith("statinf") or slug.startswith("math"):
        return "mathematics"
    if (
        slug.startswith("robotics")
        or slug.startswith("aerial-")
        or slug.startswith("mobile-robotics-")
        or slug.startswith("estimation-")
    ):
        return "robotics"
    if slug.startswith("algorithms"):
        return "algorithms"
    if _EE_RE.match(slug):
        return "electronic-engineering"
    if slug in ("matlab-basics", "python-course"):
        return "foundations"
    return None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("slug", sa.String(length=64), nullable=False, unique=True),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("icon", sa.String(length=16), nullable=False, server_default=""),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_categories_slug", "categories", ["slug"], unique=True)
    op.add_column(
        "courses",
        sa.Column(
            "category_id",
            sa.Uuid(),
            sa.ForeignKey("categories.id", ondelete="SET NULL", name="fk_courses_category"),
            nullable=True,
        ),
    )
    op.create_index("ix_courses_category_id", "courses", ["category_id"])

    # ── Backfill ──────────────────────────────────────────────────────
    bind = op.get_bind()
    now = datetime.now(tz=UTC)
    slug_to_id: dict[str, uuid.UUID] = {}
    for order, (slug, name, icon) in enumerate(_CATEGORIES):
        cat_id = uuid.uuid4()
        slug_to_id[slug] = cat_id
        bind.execute(
            sa.text(
                "INSERT INTO categories (id, slug, name, icon, sort_order, created_at) "
                "VALUES (:id, :slug, :name, :icon, :sort_order, :created_at)"
            ),
            {
                "id": cat_id,
                "slug": slug,
                "name": name,
                "icon": icon,
                "sort_order": order,
                "created_at": now,
            },
        )

    courses = bind.execute(sa.text("SELECT id, slug FROM courses")).fetchall()
    for course_id, course_slug in courses:
        cat_slug = _category_slug_for(course_slug)
        if cat_slug is None:
            continue
        bind.execute(
            sa.text("UPDATE courses SET category_id = :cid WHERE id = :id"),
            {"cid": slug_to_id[cat_slug], "id": course_id},
        )


def downgrade() -> None:
    op.drop_index("ix_courses_category_id", table_name="courses")
    op.drop_constraint("fk_courses_category", "courses", type_="foreignkey")
    op.drop_column("courses", "category_id")
    op.drop_index("ix_categories_slug", table_name="categories")
    op.drop_table("categories")
