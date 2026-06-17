"""Production guardrails: settings must refuse dev-default mocks in a
shared environment (issue #7, Operational)."""

from __future__ import annotations

import pytest

from cyberdyne_backend.infrastructure.settings import (
    InsecureProductionConfigError,
    Settings,
)

# A fully-real production config — passes the guardrail.
_REAL = {
    "chain_reader_provider": "web3py",
    "captcha_provider": "turnstile",
    "stripe_secret_key": "sk_live_x",
    "stripe_webhook_secret": "whsec_x",
    "openai_api_key": "sk-openai-x",
}


def test_local_allows_mock_defaults() -> None:
    # The default (all mocks) must keep working locally / in CI.
    Settings(environment="local")
    Settings(environment="ci")


def test_production_with_mock_defaults_refuses_to_start() -> None:
    with pytest.raises(InsecureProductionConfigError) as exc:
        Settings(
            environment="production",
            chain_reader_provider="fake",
            captcha_provider="mock",
            stripe_secret_key=None,
            stripe_webhook_secret=None,
            openai_api_key=None,
        )
    msg = str(exc.value)
    # Every offending default is listed, not just the first.
    for fragment in (
        "chain_reader_provider=fake",
        "captcha_provider=mock",
        "STRIPE_SECRET_KEY",
        "STRIPE_WEBHOOK_SECRET",
        "OPENAI_API_KEY",
    ):
        assert fragment in msg


def test_staging_is_guarded_too() -> None:
    with pytest.raises(InsecureProductionConfigError):
        Settings(environment="staging", **{**_REAL, "chain_reader_provider": "fake"})


def test_production_fully_configured_starts() -> None:
    # No exception when every adapter is real.
    Settings(environment="production", **_REAL)


def test_single_missing_secret_is_reported() -> None:
    with pytest.raises(InsecureProductionConfigError) as exc:
        Settings(environment="production", **{**_REAL, "openai_api_key": None})
    msg = str(exc.value)
    assert "OPENAI_API_KEY" in msg
    assert "chain_reader_provider=fake" not in msg  # the configured ones aren't flagged
