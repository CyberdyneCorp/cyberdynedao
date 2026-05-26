"""Domain entities for the content context."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class TeamMember:
    id: str
    name: str
    title: str
    image_url: str
    bio: str
    tags: tuple[str, ...]
    palette: str


@dataclass(frozen=True, slots=True)
class CyberdynePage:
    """The Cyberdyne about-us page payload.

    Held as an opaque ``dict[str, Any]`` — the shape is rich (domains,
    beliefs, tokenomics, roadmap, economics) and admin authoring (Phase
    3+) hasn't shipped, so normalising before there's an editor would
    invest in the wrong abstraction. The router pins a strict pydantic
    response schema so the OpenAPI surface stays typed.
    """

    slug: str
    payload: dict[str, Any]


# ── Phase 2 list entities ────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class Project:
    """One Cyberdyne project entry. Backs the Marketplace + Products views."""

    id: str
    name: str
    icon: str
    description: str
    features: tuple[str, ...]
    extra_features: tuple[str, ...] | None
    palette: str
    status: str
    full_width: bool


@dataclass(frozen=True, slots=True)
class ServiceBullet:
    title: str
    description: str


@dataclass(frozen=True, slots=True)
class ServiceSection:
    """One service-offering card on the Services view."""

    id: str
    icon: str
    title: str
    intro: str
    bullets: tuple[ServiceBullet, ...]
    palette: str
    full_width: bool


@dataclass(frozen=True, slots=True)
class ContactMethod:
    """One channel on the Contact Us view (WhatsApp / Discord / …)."""

    id: str
    name: str
    icon: str
    description: str
    action: str
    link: str
    brand_solid: str
    brand_hover: str
    brand_rgb: str
    tagline: str


@dataclass(frozen=True, slots=True)
class ResourceLink:
    label: str
    href: str
    disabled: bool = False


@dataclass(frozen=True, slots=True)
class ResourceGroup:
    """A labelled cluster of external resource links (Learn view)."""

    id: str
    icon: str
    title: str
    links: tuple[ResourceLink, ...]
