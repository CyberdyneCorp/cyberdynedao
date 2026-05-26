"""Pydantic response models for the content endpoints.

These pin the API contract — the OpenAPI schema and the frontend's
fetcher both depend on them being stable. Field names are Python
snake_case internally, but every model serialises to **camelCase** on
the wire via ``alias_generator=to_camel``. The router uses
``response_model_by_alias=True`` to enforce that.

Why bother: the existing Svelte components consume camelCase (e.g.
``member.imageUrl``). Pushing the case-conversion to the API boundary
keeps the frontend types untouched as we migrate from static data to
live fetches.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    """Project-wide response base. Emits camelCase, accepts either."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


# ── Shared palette enum ──────────────────────────────────────────────

Palette = Literal["blue", "green", "purple", "orange", "red"]


# ── Team ─────────────────────────────────────────────────────────────


class TeamMemberResponse(_CamelModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )

    id: str
    name: str
    title: str
    image_url: str
    bio: str
    tags: list[str]
    palette: Palette


# ── Cyberdyne page ───────────────────────────────────────────────────
#
# The frontend currently reads about-a-dozen named exports from
# cyberdyne.ts; we return them in a single response so the page can
# render in one round-trip.


class DomainResponse(_CamelModel):
    id: str
    name: str
    icon: str
    palette: Palette
    tagline: str
    projects: list[str]
    status: Literal["live", "shipping", "active", "planned"]


class BeliefResponse(_CamelModel):
    title: str
    description: str


class TargetUserResponse(_CamelModel):
    name: str
    description: str


class TokenomicsRowResponse(_CamelModel):
    allocation: str
    percentage: str
    vesting: str


class ExampleEconomicsRowResponse(_CamelModel):
    label: str
    value: str


class RoadmapItemResponse(_CamelModel):
    icon: str
    text: str


class RoadmapPhaseResponse(_CamelModel):
    id: str
    title: str
    subtitle: str
    status: Literal["shipped", "shipping", "active", "planned"]
    color: Palette
    items: list[RoadmapItemResponse]


class CyberdynePageResponse(_CamelModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )

    hero_tagline: str
    intro_lead: str
    intro_bullets: list[str]
    domains: list[DomainResponse]
    beliefs: list[BeliefResponse]
    target_users: list[TargetUserResponse]
    tokenomics_rows: list[TokenomicsRowResponse]
    token_utility_points: list[str]
    example_economics: list[ExampleEconomicsRowResponse]
    roadmap_phases: list[RoadmapPhaseResponse]
    closing_headline: str
    closing_body: str
