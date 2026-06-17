# configuration Specification

## Purpose

Centralized application settings (`infrastructure/settings.py`) plus the
production guardrails that stop a shared deployment from silently running
the dev-default mock adapters. (src: src/cyberdyne_backend/infrastructure/settings.py)

## Requirements

### Requirement: Mock adapters are rejected in shared environments

The system SHALL refuse to start when `environment` is `staging` or
`production` and any dev-default mock adapter is active: `chain_reader_provider
== "fake"`, `captcha_provider == "mock"`, an unset `STRIPE_SECRET_KEY`, an
unset `STRIPE_WEBHOOK_SECRET`, or an unset `OPENAI_API_KEY`. Startup SHALL
fail with an error that lists every offending setting (not just the first).
In `local` and `ci` environments the mock defaults SHALL remain active so the
test suite stays hermetic.

#### Scenario: Production with dev defaults refuses to start

- GIVEN `environment = "production"`
- AND `chain_reader_provider = "fake"`, `captcha_provider = "mock"`, and the Stripe/OpenAI secrets unset
- WHEN settings are constructed at startup
- THEN an `InsecureProductionConfigError` is raised listing all five offending settings

#### Scenario: Local keeps the mocks

- GIVEN `environment = "local"` (or `"ci"`)
- WHEN settings are constructed with the default mock adapters
- THEN startup succeeds

#### Scenario: Fully configured production starts

- GIVEN `environment = "production"`
- AND `chain_reader_provider = "web3py"`, `captcha_provider = "turnstile"`, and the Stripe + OpenAI secrets set
- WHEN settings are constructed
- THEN startup succeeds
