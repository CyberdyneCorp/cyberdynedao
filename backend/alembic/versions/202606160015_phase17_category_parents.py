"""Phase 17 — category sub-categories (self-referential parent).

Adds ``categories.parent_id`` (self-FK, ON DELETE SET NULL) so categories form
a one-level hierarchy: a top-level category is a *group* (e.g. "Programming")
and a child is a *sub-category* (e.g. "Languages"). Seeds the built-in parent
groups and parents each existing built-in leaf category, reproducing the
two-level grouping the frontend used to hardcode (topicGroups).

Revision ID: 202606160015
Revises: 202606150014
Create Date: 2026-06-16 09:00:00
"""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from datetime import UTC, datetime

import sqlalchemy as sa
from alembic import op

revision: str = "202606160015"
down_revision: str | Sequence[str] | None = "202606150014"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Parent groups: (slug, name, icon).
_GROUPS: tuple[tuple[str, str, str], ...] = (
    ("programming", "Programming", "🧑‍💻"),
    ("software-systems", "Software & Systems", "🧰"),
    ("ai-data", "AI & Data", "🧠"),
    ("engineering-robotics", "Engineering & Robotics", "🔬"),
    ("web3", "Web3", "⛓️"),
)

# leaf category slug -> parent group slug (leaves not listed stay top-level).
_PARENT: dict[str, str] = {
    "foundations": "programming",
    "languages": "programming",
    "web-development": "programming",
    "algorithms": "programming",
    "software-engineering": "software-systems",
    "devops": "software-systems",
    "databases": "software-systems",
    "operating-systems": "software-systems",
    "networking": "software-systems",
    "system-design": "software-systems",
    "distributed-systems": "software-systems",
    "concurrency-parallelism": "software-systems",
    "cybersecurity": "software-systems",
    "ai-machine-learning": "ai-data",
    "data-engineering": "ai-data",
    "physics": "engineering-robotics",
    "computer-architecture": "engineering-robotics",
    "electronic-engineering": "engineering-robotics",
    "robotics": "engineering-robotics",
    "blockchain": "web3",
}


def upgrade() -> None:
    op.add_column(
        "categories",
        sa.Column(
            "parent_id",
            sa.Uuid(),
            sa.ForeignKey("categories.id", ondelete="SET NULL", name="fk_categories_parent"),
            nullable=True,
        ),
    )
    op.create_index("ix_categories_parent_id", "categories", ["parent_id"])

    bind = op.get_bind()
    now = datetime.now(tz=UTC)
    # Seed parent groups (skip any that already exist by slug).
    group_ids: dict[str, uuid.UUID] = {}
    for order, (slug, name, icon) in enumerate(_GROUPS):
        existing = bind.execute(
            sa.text("SELECT id FROM categories WHERE slug = :slug"), {"slug": slug}
        ).scalar()
        if existing is not None:
            group_ids[slug] = existing
            continue
        gid = uuid.uuid4()
        group_ids[slug] = gid
        bind.execute(
            sa.text(
                "INSERT INTO categories (id, slug, name, icon, sort_order, created_at) "
                "VALUES (:id, :slug, :name, :icon, :sort_order, :created_at)"
            ),
            {
                "id": gid,
                "slug": slug,
                "name": name,
                "icon": icon,
                "sort_order": order,
                "created_at": now,
            },
        )
    # Parent each existing leaf that isn't already parented.
    for leaf_slug, parent_slug in _PARENT.items():
        bind.execute(
            sa.text(
                "UPDATE categories SET parent_id = :pid "
                "WHERE slug = :slug AND parent_id IS NULL"
            ),
            {"pid": group_ids[parent_slug], "slug": leaf_slug},
        )


def downgrade() -> None:
    # Remove the seeded parent groups (childless after the column drop anyway).
    bind = op.get_bind()
    bind.execute(
        sa.text("DELETE FROM categories WHERE slug = ANY(:slugs)"),
        {"slugs": [g[0] for g in _GROUPS]},
    )
    op.drop_index("ix_categories_parent_id", table_name="categories")
    op.drop_constraint("fk_categories_parent", "categories", type_="foreignkey")
    op.drop_column("categories", "parent_id")
