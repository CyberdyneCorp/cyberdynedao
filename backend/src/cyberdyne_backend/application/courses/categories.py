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

# Built-in leaf categories: (slug, name, icon, sort_order). sort_order places a
# leaf among its siblings (within its parent group); mathematics is top-level so
# its sort_order orders it among the groups. Values reproduce the exact order the
# frontend topicGroups/topicOrder used to hardcode.
BUILTIN_CATEGORIES: tuple[tuple[str, str, str, int], ...] = (
    # Programming
    ("foundations", "Foundations", "🎯", 0),
    ("languages", "Languages", "💻", 1),
    ("web-development", "Web Development", "🌍", 2),
    ("algorithms", "Algorithms", "🧮", 3),
    # Software & Systems
    ("software-engineering", "Software Engineering", "🧰", 0),
    ("devops", "DevOps", "⚙️", 1),
    ("databases", "Databases", "🗄️", 2),
    ("operating-systems", "Operating Systems", "🖥️", 3),
    ("networking", "Networking", "🌐", 4),
    ("system-design", "System Design", "🏗️", 5),
    ("distributed-systems", "Distributed Systems", "🕸️", 6),
    ("concurrency-parallelism", "Concurrency & Parallelism", "⚡", 7),
    ("cybersecurity", "Cybersecurity", "🔒", 8),
    # AI & Data
    ("ai-machine-learning", "AI / Machine Learning", "🧠", 0),
    ("data-engineering", "Data Engineering", "🏭", 1),
    # Mathematics — a standalone top-level category (sits 4th among top-level).
    ("mathematics", "Mathematics", "➗", 3),
    # Engineering & Robotics
    ("physics", "Physics", "⚛️", 0),
    ("computer-architecture", "Computer Architecture", "🏛️", 1),
    ("electronic-engineering", "Electronic Engineering", "🔌", 2),
    ("robotics", "Robotics", "🤖", 3),
    # Web3
    ("blockchain", "Blockchain", "⛓️", 0),
)

# Built-in parent groups (top-level categories): (slug, name, icon). Order is
# the display order. Mirrors the frontend topicGroups.
# Built-in parent groups: (slug, name, icon, sort_order). sort_order places the
# group among the top-level items (mathematics, a top-level leaf, sits at 3).
BUILTIN_GROUPS: tuple[tuple[str, str, str, int], ...] = (
    ("programming", "Programming", "🧑‍💻", 0),
    ("software-systems", "Software & Systems", "🧰", 1),
    ("ai-data", "AI & Data", "🧠", 2),
    ("engineering-robotics", "Engineering & Robotics", "🔬", 4),
    ("web3", "Web3", "⛓️", 5),
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
    # Foundational CS-theory course (computability/logic) — placed under
    # Foundations, ahead of the generic ``algorithms`` prefix match below.
    if slug == "algorithms-logic-computing":
        return "foundations"
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
    if slug.startswith("webdev-") or slug.startswith("django-") or slug.startswith("rails-"):
        return "web-development"
    if slug.startswith("dataeng-"):
        return "data-engineering"
    if slug.startswith("concurrency-"):
        return "concurrency-parallelism"
    if (
        slug.startswith("git-")
        or slug.startswith("testing-")
        or slug.startswith("software-quality-")
        or slug.startswith("software-architecture-")
    ):
        return "software-engineering"
    if slug.startswith("computational-thinking-"):
        return "foundations"
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
    if (
        slug.startswith("vectorcalc")
        or slug.startswith("statinf")
        or slug.startswith("math")
        or slug.startswith("prob-stats-python-")
        or slug.startswith("stochastic-processes-")
    ):
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
    if _EE_RE.match(slug) or slug.startswith(
        (
            "circuit-analysis-",
            "filter-design-",
            "data-converters-",
            "rfic-",
            "coding-theory-",
            "analog-comms-",
            "wireless-comms-",
            "fiber-optics-",
            "radar-",
            "image-processing-",
            "audio-processing-",
            "adaptive-dsp-",
        )
    ):
        return "electronic-engineering"
    if (
        slug in ("matlab-basics", "python-course")
        or slug.startswith("technical-english-")
        or slug.startswith("english-br-")
    ):
        return "foundations"
    return None


async def seed_categories(repo: CategoryRepository) -> dict[str, Category]:
    """Idempotently upsert the built-in parent groups + leaf categories and
    return them all by slug. Existing categories (matched by slug) are reused so
    an editor's renamed icon/name and custom categories survive a reseed. A
    built-in leaf's parent is set only when currently unset, so a manual
    reparent is not clobbered."""
    by_slug: dict[str, Category] = {}
    # Parent groups first, so leaves can reference them. sort_order is kept
    # canonical for built-ins (there's no admin reorder), but an edited
    # name/icon is preserved.
    for slug, name, icon, order in BUILTIN_GROUPS:
        existing = await repo.get_by_slug(slug)
        if existing is not None:
            if existing.sort_order != order:
                existing.sort_order = order
                await repo.save(existing)
            by_slug[slug] = existing
            continue
        group = new_category(name=name, slug=slug, icon=icon, sort_order=order)
        await repo.save(group)
        by_slug[slug] = group
    # Leaf categories, parented to their group. Parent is filled only when unset
    # (so a manual reparent survives); sort_order is kept canonical.
    for slug, name, icon, order in BUILTIN_CATEGORIES:
        parent_slug = CATEGORY_PARENT.get(slug)
        parent = by_slug.get(parent_slug) if parent_slug else None
        existing = await repo.get_by_slug(slug)
        if existing is not None:
            changed = False
            if existing.parent_id is None and parent is not None:
                existing.parent_id = parent.id
                changed = True
            if existing.sort_order != order:
                existing.sort_order = order
                changed = True
            if changed:
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
