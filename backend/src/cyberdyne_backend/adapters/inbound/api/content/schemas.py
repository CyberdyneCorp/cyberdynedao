"""Pydantic response models for the content endpoints.

These pin the API contract — the OpenAPI schema and the frontend's
fetcher both depend on them being stable. They mirror the shapes the
existing Svelte components consume in
``frontend/src/lib/data/{team,cyberdyne}.ts``.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

# ── Shared palette enum ──────────────────────────────────────────────

Palette = Literal["blue", "green", "purple", "orange", "red"]


# ── Team ─────────────────────────────────────────────────────────────


class TeamMemberResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

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


class DomainResponse(BaseModel):
    id: str
    name: str
    icon: str
    palette: Palette
    tagline: str
    projects: list[str]
    status: Literal["live", "shipping", "active", "planned"]


class BeliefResponse(BaseModel):
    title: str
    description: str


class TargetUserResponse(BaseModel):
    name: str
    description: str


class TokenomicsRowResponse(BaseModel):
    allocation: str
    percentage: str
    vesting: str


class ExampleEconomicsRowResponse(BaseModel):
    label: str
    value: str


class RoadmapItemResponse(BaseModel):
    icon: str
    text: str


class RoadmapPhaseResponse(BaseModel):
    id: str
    title: str
    subtitle: str
    status: Literal["shipped", "shipping", "active", "planned"]
    color: Palette
    items: list[RoadmapItemResponse]


class CyberdynePageResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

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
