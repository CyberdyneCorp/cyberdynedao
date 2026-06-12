"""Scoping logic for the translate_academy CLI (--slug / --limit)."""

from __future__ import annotations

import pytest

from cyberdyne_backend.cli.translate_academy import _parse_args, select_courses
from cyberdyne_backend.domain.courses import new_course

pytestmark = pytest.mark.unit


def _courses() -> list:
    return [
        new_course(title="A", description="d", level="Beginner", slug="a"),
        new_course(title="B", description="d", level="Beginner", slug="b"),
        new_course(title="C", description="d", level="Beginner", slug="c"),
    ]


def test_no_scope_returns_all() -> None:
    courses = _courses()
    assert select_courses(courses) == courses


def test_slug_filters_to_one() -> None:
    picked = select_courses(_courses(), slug="b")
    assert [c.slug for c in picked] == ["b"]


def test_unknown_slug_returns_empty() -> None:
    assert select_courses(_courses(), slug="zzz") == []


def test_limit_takes_first_n_in_order() -> None:
    picked = select_courses(_courses(), limit=2)
    assert [c.slug for c in picked] == ["a", "b"]


def test_slug_wins_over_limit() -> None:
    picked = select_courses(_courses(), slug="c", limit=1)
    assert [c.slug for c in picked] == ["c"]


def test_args_slug_and_limit_are_mutually_exclusive() -> None:
    assert _parse_args(["--slug", "a"]).slug == "a"
    assert _parse_args(["--limit", "3"]).limit == 3
    with pytest.raises(SystemExit):
        _parse_args(["--slug", "a", "--limit", "2"])
