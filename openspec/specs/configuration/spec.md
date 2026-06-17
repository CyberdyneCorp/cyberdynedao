# configuration Specification

## Purpose

Centralized application settings (`infrastructure/settings.py`) plus the
production guardrails that surface — and optionally block on — dev-default
mock adapters in a shared deployment. (src: src/cyberdyne_backend/infrastructure/settings.py)

## Requirements

### Requirement: Settings construction never blocks on mock adapters

Constructing `Settings` SHALL NOT raise on account of active mock adapters,
in any environment. The guardrail check is a separate, explicitly-invoked
step so that tooling which only needs configuration (e.g. `alembic upgrade`
reading the database URL) is never broken by it.

#### Scenario: Production settings construct cleanly

- GIVEN `environment = "production"` with dev-default mock adapters active
- WHEN `Settings()` is constructed (e.g. by the Alembic migration runner)
- THEN construction succeeds without raising

### Requirement: Mock adapters are surfaced in shared environments

The system SHALL identify dev-default mock adapters that should not run in
`staging`/`production`: `chain_reader_provider == "fake"`, `captcha_provider
== "mock"`, an unset `STRIPE_SECRET_KEY`, an unset `STRIPE_WEBHOOK_SECRET`,
and an unset `OPENAI_API_KEY`. In `local`/`ci` there SHALL be no such
problems (the mocks are the hermetic defaults).

#### Scenario: Every active mock is listed in production

- GIVEN `environment = "production"` with all mock defaults active
- WHEN the mock-adapter problems are computed
- THEN all five offending settings are reported

#### Scenario: Local reports nothing

- GIVEN `environment = "local"` (or `"ci"`)
- WHEN the mock-adapter problems are computed
- THEN the list is empty

### Requirement: App startup warns, or hard-fails when enforced

At app-serving startup the system SHALL log a warning for each active mock
adapter in `staging`/`production`, and SHALL boot anyway by default so a
partially-provisioned environment is not blocked. When
`enforce_production_adapters` is set, startup SHALL instead raise
`InsecureProductionConfigError` listing every offending setting.

#### Scenario: Partially-provisioned production boots with a warning

- GIVEN `environment = "production"`, some mocks active, and `enforce_production_adapters` unset
- WHEN the app factory runs its startup guardrail check
- THEN a warning is logged and the app starts

#### Scenario: Enforced production refuses to start

- GIVEN `environment = "production"`, a mock active, and `enforce_production_adapters = true`
- WHEN the app factory runs its startup guardrail check
- THEN an `InsecureProductionConfigError` is raised
