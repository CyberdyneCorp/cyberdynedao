"""Tests for the learning domain entities + factories."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest

from cyberdyne_backend.domain.learning import (
    CertificateNotEligibleError,
    LearningPath,
    ProgressOutOfRangeError,
    certificate_eligible,
    new_certificate,
    new_enrollment,
    new_progress,
)


class _StubSigner:
    """Deterministic signer for assertions."""

    def __init__(self, prefix: str = "sig:") -> None:
        self.prefix = prefix
        self.calls: list[str] = []

    def sign(self, message: str) -> str:
        self.calls.append(message)
        return f"{self.prefix}{message[:8]}"


def _path(slugs: tuple[str, ...] = ("m1", "m2")) -> LearningPath:
    return LearningPath(
        slug="p1",
        title="Path",
        description="desc",
        module_slugs=slugs,
        estimated_time="4 weeks",
        icon="x",
    )


class TestNewEnrollment:
    def test_status_defaults_to_active(self) -> None:
        e = new_enrollment(user_id=uuid.uuid4(), path_slug="p1")
        assert e.status.value == "active"
        assert e.started_at.tzinfo is not None

    def test_explicit_now_is_honoured(self) -> None:
        moment = datetime(2026, 1, 1, tzinfo=UTC)
        e = new_enrollment(user_id=uuid.uuid4(), path_slug="p1", now=moment)
        assert e.started_at == moment


class TestNewProgress:
    def test_zero_percent_has_no_completion_marker(self) -> None:
        p = new_progress(user_id=uuid.uuid4(), module_slug="m1")
        assert p.percent == 0
        assert p.completed_at is None

    def test_hundred_percent_sets_completion(self) -> None:
        p = new_progress(user_id=uuid.uuid4(), module_slug="m1", percent=100)
        assert p.is_completed
        assert p.completed_at is not None

    def test_out_of_range_raises(self) -> None:
        with pytest.raises(ProgressOutOfRangeError):
            new_progress(user_id=uuid.uuid4(), module_slug="m1", percent=101)
        with pytest.raises(ProgressOutOfRangeError):
            new_progress(user_id=uuid.uuid4(), module_slug="m1", percent=-1)


class TestModuleProgressUpdate:
    def test_completion_marker_set_at_100(self) -> None:
        p = new_progress(user_id=uuid.uuid4(), module_slug="m1")
        p.update(100)
        assert p.is_completed

    def test_reopen_clears_marker(self) -> None:
        p = new_progress(user_id=uuid.uuid4(), module_slug="m1", percent=100)
        assert p.completed_at is not None
        p.update(50)
        assert p.completed_at is None
        assert not p.is_completed

    def test_out_of_range_raises(self) -> None:
        p = new_progress(user_id=uuid.uuid4(), module_slug="m1")
        with pytest.raises(ProgressOutOfRangeError):
            p.update(200)


class TestCertificateEligible:
    def test_all_complete_is_eligible(self) -> None:
        user = uuid.uuid4()
        path = _path()
        progress = {
            "m1": new_progress(user_id=user, module_slug="m1", percent=100),
            "m2": new_progress(user_id=user, module_slug="m2", percent=100),
        }
        assert certificate_eligible(path, progress)

    def test_partial_progress_not_eligible(self) -> None:
        user = uuid.uuid4()
        path = _path()
        progress = {
            "m1": new_progress(user_id=user, module_slug="m1", percent=100),
            "m2": new_progress(user_id=user, module_slug="m2", percent=50),
        }
        assert not certificate_eligible(path, progress)

    def test_missing_module_not_eligible(self) -> None:
        user = uuid.uuid4()
        path = _path()
        progress = {"m1": new_progress(user_id=user, module_slug="m1", percent=100)}
        assert not certificate_eligible(path, progress)


class TestNewCertificate:
    def test_mints_with_deterministic_hash(self) -> None:
        user = uuid.uuid4()
        path = _path()
        signer = _StubSigner()
        progress = {
            slug: new_progress(user_id=user, module_slug=slug, percent=100)
            for slug in path.module_slugs
        }
        cert = new_certificate(
            user_id=user,
            path=path,
            progress_by_module=progress,
            signer=signer,
        )
        assert cert.user_id == user
        assert cert.path_slug == path.slug
        assert len(cert.verification_hash) == 64
        assert cert.signed_payload.startswith(signer.prefix)
        assert signer.calls == [cert.verification_hash]

    def test_not_eligible_raises(self) -> None:
        user = uuid.uuid4()
        path = _path()
        signer = _StubSigner()
        progress = {"m1": new_progress(user_id=user, module_slug="m1", percent=50)}
        with pytest.raises(CertificateNotEligibleError):
            new_certificate(
                user_id=user,
                path=path,
                progress_by_module=progress,
                signer=signer,
            )
