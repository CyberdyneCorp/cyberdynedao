"""SQLAlchemy ORM models for the leads context."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import JSON, DateTime, ForeignKey, Index, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from cyberdyne_backend.infrastructure.database.base import Base


class AskRow(Base):
    __tablename__ = "asks"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True)
    channel: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(256), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    product_slug: Mapped[str | None] = mapped_column(String(64), nullable=True)
    source_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    owner_user_id: Mapped[UUID | None] = mapped_column(Uuid(), nullable=True)
    notes_md: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        Index("ix_asks_status", "status"),
        Index("ix_asks_channel", "channel"),
        Index("ix_asks_created_at", "created_at"),
    )


class AskEventRow(Base):
    __tablename__ = "ask_events"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True)
    ask_id: Mapped[UUID] = mapped_column(
        Uuid(),
        ForeignKey("asks.id", ondelete="CASCADE"),
        nullable=False,
    )
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    by_user_id: Mapped[UUID | None] = mapped_column(Uuid(), nullable=True)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (Index("ix_ask_events_ask_id", "ask_id"),)
