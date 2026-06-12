"""Unit tests for request locale resolution."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from cyberdyne_backend.adapters.inbound.api.locale import (
    match_language,
    resolve_locale,
)

pytestmark = pytest.mark.unit


def _request(accept_language: str | None = None):
    headers = {"accept-language": accept_language} if accept_language is not None else {}
    return SimpleNamespace(headers=headers)


@pytest.mark.parametrize(
    ("tag", "expected"),
    [
        ("pt-BR", "pt-BR"),
        ("PT-br", "pt-BR"),  # case-insensitive
        ("pt-PT", "pt-BR"),  # primary-subtag match
        ("es", "es"),
        ("fr-CA", "fr"),
        ("en-US", "en"),
        ("de", None),  # unsupported
        ("", None),
        (None, None),
    ],
)
def test_match_language(tag, expected) -> None:
    assert match_language(tag) == expected


def test_query_param_wins_over_header() -> None:
    assert resolve_locale(_request("fr"), lang="es") == "es"


def test_falls_back_to_accept_language_header() -> None:
    assert resolve_locale(_request("pt-BR,pt;q=0.9,en;q=0.8"), lang=None) == "pt-BR"


def test_honours_accept_language_q_priority() -> None:
    # English higher priority than French → English.
    assert resolve_locale(_request("fr;q=0.4, en;q=0.9"), lang=None) == "en"


def test_defaults_to_english_when_nothing_matches() -> None:
    assert resolve_locale(_request("de-DE,de;q=0.9"), lang=None) == "en"
    assert resolve_locale(_request(None), lang=None) == "en"


def test_unsupported_query_param_falls_through_to_header() -> None:
    assert resolve_locale(_request("es"), lang="klingon") == "es"
