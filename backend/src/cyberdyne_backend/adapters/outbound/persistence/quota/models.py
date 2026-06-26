"""SQLAlchemy ORM model for per-user usage counters."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import Integer, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from cyberdyne_backend.infrastructure.database.base import Base


class UsageCounterRow(Base):
    __tablename__ = "usage_counters"
    __table_args__ = (
        UniqueConstraint("user_id", "meter", "period_key", name="uq_usage_user_meter_period"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(Uuid(), nullable=False, index=True)
    meter: Mapped[str] = mapped_column(String(32), nullable=False)
    # Period bucket: "YYYY-MM" (monthly) or "YYYY-MM-DD" (daily).
    period_key: Mapped[str] = mapped_column(String(16), nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
