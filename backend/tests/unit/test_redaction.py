"""Unit tests for PII log redaction (issue #7)."""

from __future__ import annotations

import pytest

from cyberdyne_backend.infrastructure.redaction import redact_email


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("alice@example.com", "a***@example.com"),
        ("bob.smith@cyberdyne.ai", "b***@cyberdyne.ai"),
        ("a@x.io", "*@x.io"),  # single-char local fully masked
        ("", ""),
        (None, ""),
        ("not-an-email", "n***"),  # no @ → masked token
        ("x", "*"),
    ],
)
def test_redact_email(raw: str | None, expected: str) -> None:
    assert redact_email(raw) == expected


def test_redact_email_hides_the_local_part() -> None:
    out = redact_email("verysecretlocal@example.com")
    assert "verysecretlocal" not in out
    assert out.endswith("@example.com")
