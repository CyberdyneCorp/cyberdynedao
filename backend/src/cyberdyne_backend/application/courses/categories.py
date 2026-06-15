"""Built-in course categories + slug-derived assignment.

Categories are stored data (an editor can create/rename/delete and reassign),
but the catalogue ships with a built-in set and every seeded course is given a
sensible default category derived from its slug — the same mapping the frontend
historically used (``courseTopic``). Assignment only fills *uncategorized*
courses, so a manual admin reassignment is never clobbered on the next reseed.
"""

from __future__ import annotations

import re

from cyberdyne_backend.domain.courses import (
    Category,
    CategoryRepository,
    CourseRepository,
    new_category,
)

# Built-in categories: (slug, name, icon). Order is the display order. Kept in
# sync with the frontend topicOrder/topicMeta; the migration seeds the same set.
BUILTIN_CATEGORIES: tuple[tuple[str, str, str], ...] = (
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

# Built-in parent groups (top-level categories): (slug, name, icon). Order is
# the display order. Mirrors the frontend topicGroups.
BUILTIN_GROUPS: tuple[tuple[str, str, str], ...] = (
    ("programming", "Programming", "🧑‍💻"),
    ("software-systems", "Software & Systems", "🧰"),
    ("ai-data", "AI & Data", "🧠"),
    ("engineering-robotics", "Engineering & Robotics", "🔬"),
    ("web3", "Web3", "⛓️"),
)

# Which parent group each built-in (leaf) category belongs to. A leaf not listed
# here stays top-level (e.g. Mathematics renders as its own row, as today).
CATEGORY_PARENT: dict[str, str] = {
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

_EE_RE = re.compile(
    r"^(electronics|analog-ic|antennas|power-electronics|pcb|semiconductor|embedded|signals|"
    r"signal-integrity|control|dsp|rf-comms|microwave|digital-comms|digital-logic|fpga|"
    r"electromagnetics|emc|test-measurement|hw-verification|vlsi|photonics|power-systems|"
    r"battery|sensors|machines)-"
)


def category_slug_for(slug: str) -> str | None:
    """The default category slug for a course slug (mirror of the frontend
    ``courseTopic``), or ``None`` for the 'Other' bucket."""
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


async def seed_categories(repo: CategoryRepository) -> dict[str, Category]:
    """Idempotently upsert the built-in parent groups + leaf categories and
    return them all by slug. Existing categories (matched by slug) are reused so
    an editor's renamed icon/name and custom categories survive a reseed. A
    built-in leaf's parent is set only when currently unset, so a manual
    reparent is not clobbered."""
    by_slug: dict[str, Category] = {}
    # Parent groups first, so leaves can reference them.
    for order, (slug, name, icon) in enumerate(BUILTIN_GROUPS):
        existing = await repo.get_by_slug(slug)
        if existing is not None:
            by_slug[slug] = existing
            continue
        group = new_category(name=name, slug=slug, icon=icon, sort_order=order)
        await repo.save(group)
        by_slug[slug] = group
    # Leaf categories, parented to their group.
    for order, (slug, name, icon) in enumerate(BUILTIN_CATEGORIES):
        parent_slug = CATEGORY_PARENT.get(slug)
        parent = by_slug.get(parent_slug) if parent_slug else None
        existing = await repo.get_by_slug(slug)
        if existing is not None:
            if existing.parent_id is None and parent is not None:
                existing.parent_id = parent.id
                await repo.save(existing)
            by_slug[slug] = existing
            continue
        category = new_category(
            name=name,
            slug=slug,
            icon=icon,
            sort_order=order,
            parent_id=parent.id if parent is not None else None,
        )
        await repo.save(category)
        by_slug[slug] = category
    return by_slug


async def assign_course_categories(
    course_repo: CourseRepository, categories: dict[str, Category]
) -> int:
    """Give every *uncategorized* course its slug-derived default category.
    Courses that already have a category (e.g. a manual admin assignment) are
    left untouched. Returns the number of courses newly assigned."""
    courses = await course_repo.list_courses(include_drafts=True)
    assigned = 0
    for course in courses:
        if course.category is not None:
            continue
        cat_slug = category_slug_for(course.slug)
        category = categories.get(cat_slug) if cat_slug else None
        if category is None:
            continue
        await course_repo.set_category(course.id, category.id)
        assigned += 1
    return assigned
