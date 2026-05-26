"""Declarative base for SQLAlchemy ORM models.

Per-request sessions read/write rows from tables defined against this
base. Tables themselves live alongside their bounded context's adapter
(``adapters/outbound/persistence/<context>/models.py``).
"""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Project-wide declarative base."""
