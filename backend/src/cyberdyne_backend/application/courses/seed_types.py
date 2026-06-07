"""Shared data types for the Academy course seed (kept here so the content
modules — ``seed`` and ``seed_languages`` — can import them without a cycle)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class SeedLesson:
    title: str
    lesson_type: str  # 'text' | 'code' | 'quiz' | …
    text_body: str | None = None
    duration: str | None = None


@dataclass(frozen=True, slots=True)
class SeedCourse:
    slug: str
    title: str
    description: str
    level: str
    lessons: tuple[SeedLesson, ...] = field(default_factory=tuple)


__all__ = ["SeedCourse", "SeedLesson"]
