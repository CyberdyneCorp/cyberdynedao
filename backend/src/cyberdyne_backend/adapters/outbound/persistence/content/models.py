"""SQLAlchemy ORM models for the content context."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from cyberdyne_backend.infrastructure.database.base import Base


class TeamMemberRow(Base):
    """One row per teammate; ordered by ``sort_order`` then ``id``."""

    __tablename__ = "team_members"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    image_url: Mapped[str] = mapped_column(String(256), nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=False)
    palette: Mapped[str] = mapped_column(String(32), nullable=False)
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class ContentPageRow(Base):
    """Free-form content document keyed by slug.

    Phase 1 stores the cyberdyne page payload as one big JSON blob.
    Phase 2 reuses the same shape for the services-meta + contact-meta
    payloads (workflow steps, CTA, intro copy) — anything page-shaped
    that doesn't earn its own relational table yet.
    """

    __tablename__ = "content_pages"

    slug: Mapped[str] = mapped_column(String(64), primary_key=True)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(nullable=True)


# ── Phase 2 ──────────────────────────────────────────────────────────


class ProjectRow(Base):
    """One row per Cyberdyne project (Products / Marketplace views)."""

    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    icon: Mapped[str] = mapped_column(String(16), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    features: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    extra_features: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    palette: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    full_width: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class ServiceSectionRow(Base):
    """One row per service-offering card on the Services view.

    ``bullets`` is ``list[{title, description}]`` — held as JSON because
    the shape is fixed and we never query individual bullets.
    """

    __tablename__ = "service_sections"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    icon: Mapped[str] = mapped_column(String(16), nullable=False)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    intro: Mapped[str] = mapped_column(Text, nullable=False)
    bullets: Mapped[list[dict[str, str]]] = mapped_column(JSON, nullable=False, default=list)
    palette: Mapped[str] = mapped_column(String(32), nullable=False)
    full_width: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class ContactMethodRow(Base):
    """One row per contact channel (WhatsApp, Discord, GitHub, …)."""

    __tablename__ = "contact_methods"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    icon: Mapped[str] = mapped_column(String(16), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    action: Mapped[str] = mapped_column(String(64), nullable=False)
    link: Mapped[str] = mapped_column(String(512), nullable=False)
    brand_solid: Mapped[str] = mapped_column(String(16), nullable=False)
    brand_hover: Mapped[str] = mapped_column(String(16), nullable=False)
    brand_rgb: Mapped[str] = mapped_column(String(32), nullable=False)
    tagline: Mapped[str] = mapped_column(String(128), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class ResourceGroupRow(Base):
    """One row per resource-link cluster on the Learn view.

    Links are inlined as JSON (``[{label, href, disabled}]``) — they're
    display-only, never queried individually, and the parent group has
    no separate lifecycle. Splitting into a child table would add a
    join for nothing.
    """

    __tablename__ = "resource_groups"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    icon: Mapped[str] = mapped_column(String(16), nullable=False)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    links: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
