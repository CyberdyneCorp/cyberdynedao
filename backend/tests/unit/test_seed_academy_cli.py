"""Boot-path gating for the seed_academy CLI (--on-boot / SEED_ACADEMY_ON_BOOT).

Regression coverage for issue #259: the full-catalog seed must be skippable on
the blocking boot path (so ops can move it to a release step) while a manual
invocation always seeds. Pure, no DB — exercises ``_should_run_seed`` and the
``--on-boot`` argument parsing.
"""

from __future__ import annotations

import pytest

from cyberdyne_backend.cli.seed_academy import _parse_args, _should_run_seed
from cyberdyne_backend.infrastructure.settings import Settings

pytestmark = pytest.mark.unit


def _settings(*, on_boot_flag: bool) -> Settings:
    return Settings(seed_academy_on_boot=on_boot_flag)


def test_on_boot_with_flag_disabled_skips() -> None:
    # The one case that skips: booting AND ops moved the seed to a release step.
    assert _should_run_seed(True, _settings(on_boot_flag=False)) is False


def test_on_boot_with_flag_enabled_runs() -> None:
    assert _should_run_seed(True, _settings(on_boot_flag=True)) is True


def test_manual_invocation_runs_regardless_of_flag() -> None:
    # A no-flag (release-step) invocation always seeds, whatever the env says.
    assert _should_run_seed(False, _settings(on_boot_flag=False)) is True
    assert _should_run_seed(False, _settings(on_boot_flag=True)) is True


def test_default_flag_is_true_so_boot_seeds() -> None:
    # Backward-compat: unset SEED_ACADEMY_ON_BOOT keeps the boot seed on.
    assert Settings().seed_academy_on_boot is True
    assert _should_run_seed(True, Settings()) is True


def test_parse_args_defaults_off_boot_false() -> None:
    assert _parse_args([]).on_boot is False


def test_parse_args_on_boot_flag() -> None:
    assert _parse_args(["--on-boot"]).on_boot is True
