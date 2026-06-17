"""Production guardrails: mock adapters are flagged in shared environments,
and (opt-in) can hard-fail app startup — but settings construction itself
never raises, so migrations/tooling are unaffected (issue #7, Operational)."""

from __future__ import annotations

import logging

import pytest

from cyberdyne_backend.infrastructure.settings import (
    InsecureProductionConfigError,
    Settings,
)

# A fully-real production config — no mock-adapter problems.
_REAL = {
    "chain_reader_provider": "web3py",
    "captcha_provider": "turnstile",
    "stripe_secret_key": "sk_live_x",
    "stripe_webhook_secret": "whsec_x",
    "openai_api_key": "sk-openai-x",
}


def test_construction_never_raises_even_in_production() -> None:
    # Critical: building Settings() must not raise — alembic env.py and other
    # tooling construct it just to read the DB URL. (Regression guard.)
    s = Settings(environment="production")  # all mocks active
    assert s.environment == "production"


def test_local_has_no_problems() -> None:
    assert Settings(environment="local").mock_adapter_problems() == []
    assert Settings(environment="ci").mock_adapter_problems() == []


def test_production_lists_every_active_mock() -> None:
    problems = Settings(
        environment="production",
        chain_reader_provider="fake",
        captcha_provider="mock",
        stripe_secret_key=None,
        stripe_webhook_secret=None,
        openai_api_key=None,
    ).mock_adapter_problems()
    joined = "\n".join(problems)
    for fragment in (
        "chain_reader_provider=fake",
        "captcha_provider=mock",
        "STRIPE_SECRET_KEY",
        "STRIPE_WEBHOOK_SECRET",
        "OPENAI_API_KEY",
    ):
        assert fragment in joined


def test_fully_configured_production_has_no_problems() -> None:
    assert Settings(environment="production", **_REAL).mock_adapter_problems() == []


def test_check_warns_by_default(caplog: pytest.LogCaptureFixture) -> None:
    log = logging.getLogger("test.guardrail")
    s = Settings(environment="production")  # mocks active, enforce off (default)
    with caplog.at_level(logging.WARNING):
        s.check_production_adapters(log)  # must NOT raise
    assert "dev-default mock adapters active" in caplog.text


def test_check_raises_when_enforced() -> None:
    s = Settings(
        environment="production",
        enforce_production_adapters=True,
        chain_reader_provider="fake",
    )
    with pytest.raises(InsecureProductionConfigError):
        s.check_production_adapters(logging.getLogger("test.guardrail"))


def test_enforced_but_fully_configured_is_fine() -> None:
    s = Settings(environment="production", enforce_production_adapters=True, **_REAL)
    s.check_production_adapters(logging.getLogger("test.guardrail"))  # no raise


def test_local_check_is_a_noop_even_when_enforced() -> None:
    s = Settings(environment="local", enforce_production_adapters=True)
    s.check_production_adapters(logging.getLogger("test.guardrail"))  # no raise
