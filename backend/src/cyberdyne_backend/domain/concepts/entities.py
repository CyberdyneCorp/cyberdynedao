"""Entities for the concepts context — standalone concept cards (#168).

A *concept card* is a short, browsable idea (title + markdown summary +
optional formula) that lives independently of any single lesson, plus
back-links to the lessons/courses that teach it. Concepts used to exist
only embedded in lesson markdown; this context makes them a first-class,
searchable library (the Concepts nav).
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from cyberdyne_backend.domain.concepts.errors import InvalidConceptError

_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_MAX_TITLE = 160
_MAX_DOMAIN = 64


@dataclass(slots=True)
class Concept:
    id: UUID
    slug: str
    title: str
    domain: str
    summary: str  # markdown
    formula: str | None = None
    # Back-links to the lessons/courses that teach the concept.
    related_lesson_ids: tuple[UUID, ...] = ()
    related_course_slugs: tuple[str, ...] = ()
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
    updated_at: datetime | None = None

    def validate(self) -> None:
        if not _SLUG_RE.match(self.slug):
            raise InvalidConceptError(f"slug must be kebab-case ([a-z0-9-]), got {self.slug!r}")
        if not self.title.strip() or len(self.title) > _MAX_TITLE:
            raise InvalidConceptError(f"title must be 1..{_MAX_TITLE} chars")
        if not self.domain.strip() or len(self.domain) > _MAX_DOMAIN:
            raise InvalidConceptError(f"domain must be 1..{_MAX_DOMAIN} chars")
        if not self.summary.strip():
            raise InvalidConceptError("summary cannot be empty")


def new_concept(
    *,
    slug: str,
    title: str,
    domain: str,
    summary: str,
    formula: str | None = None,
    related_lesson_ids: tuple[UUID, ...] = (),
    related_course_slugs: tuple[str, ...] = (),
    now: datetime | None = None,
) -> Concept:
    moment = now or datetime.now(tz=UTC)
    concept = Concept(
        id=uuid.uuid4(),
        slug=slug.strip(),
        title=title.strip(),
        domain=domain.strip(),
        summary=summary.strip(),
        formula=formula.strip() if formula else None,
        related_lesson_ids=related_lesson_ids,
        related_course_slugs=related_course_slugs,
        created_at=moment,
        updated_at=moment,
    )
    concept.validate()
    return concept


@dataclass(slots=True)
class ConceptPage:
    """A page of browsable concepts plus an opaque forward cursor."""

    items: list[Concept] = field(default_factory=list)
    next_cursor: str | None = None
