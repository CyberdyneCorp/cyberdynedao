"""Tests for the learning use cases — use in-memory fakes for the repo."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest

from cyberdyne_backend.application.learning import (
    EnrollInPath,
    GetMyLearningState,
    IssueCertificate,
    ListModules,
    ListPaths,
    UpdateModuleProgress,
)
from cyberdyne_backend.domain.learning import (
    Certificate,
    CertificateNotEligibleError,
    Enrollment,
    LearningContentNotFoundError,
    LearningModule,
    LearningPath,
    ModuleProgress,
)


class _FakeRepo:
    def __init__(self) -> None:
        self.modules: list[LearningModule] = []
        self.paths: dict[str, LearningPath] = {}
        self.enrollments: list[Enrollment] = []
        self.progress: dict[tuple[uuid.UUID, str], ModuleProgress] = {}
        self.certs: dict[tuple[uuid.UUID, str], Certificate] = {}

    async def list_modules(self) -> list[LearningModule]:
        return list(self.modules)

    async def list_paths(self) -> list[LearningPath]:
        return list(self.paths.values())

    async def get_path(self, slug: str) -> LearningPath:
        if slug not in self.paths:
            raise LearningContentNotFoundError(slug)
        return self.paths[slug]

    async def upsert_enrollment(self, enrollment: Enrollment) -> Enrollment:
        for existing in self.enrollments:
            if (
                existing.user_id == enrollment.user_id
                and existing.path_slug == enrollment.path_slug
            ):
                return existing
        self.enrollments.append(enrollment)
        return enrollment

    async def list_enrollments_for_user(self, user_id: uuid.UUID) -> list[Enrollment]:
        return [e for e in self.enrollments if e.user_id == user_id]

    async def upsert_progress(self, progress: ModuleProgress) -> ModuleProgress:
        self.progress[(progress.user_id, progress.module_slug)] = progress
        return progress

    async def get_progress_map_for_user(self, user_id: uuid.UUID) -> dict[str, ModuleProgress]:
        return {slug: p for (uid, slug), p in self.progress.items() if uid == user_id}

    async def save_certificate(self, certificate: Certificate) -> None:
        self.certs[(certificate.user_id, certificate.path_slug)] = certificate

    async def get_certificate_for_user_and_path(
        self, user_id: uuid.UUID, path_slug: str
    ) -> Certificate | None:
        return self.certs.get((user_id, path_slug))


class _StubSigner:
    def sign(self, message: str) -> str:
        return f"sig:{message[:8]}"


def _path() -> LearningPath:
    return LearningPath(
        slug="p1",
        title="Path",
        description="d",
        module_slugs=("m1", "m2"),
        estimated_time="4w",
        icon="x",
    )


def _module(slug: str) -> LearningModule:
    return LearningModule(
        slug=slug,
        title=f"{slug} title",
        category="c",
        description="d",
        level="Beginner",
        duration="1h",
        icon="x",
        topics=(),
    )


class TestListEndpoints:
    async def test_list_modules(self) -> None:
        repo = _FakeRepo()
        repo.modules = [_module("m1"), _module("m2")]
        assert len(await ListModules(repo=repo).execute()) == 2

    async def test_list_paths(self) -> None:
        repo = _FakeRepo()
        repo.paths = {"p1": _path()}
        assert (await ListPaths(repo=repo).execute())[0].slug == "p1"


class TestEnrollInPath:
    async def test_creates_enrollment(self) -> None:
        repo = _FakeRepo()
        repo.paths = {"p1": _path()}
        user = uuid.uuid4()
        enrollment = await EnrollInPath(repo=repo).execute(user_id=user, path_slug="p1")
        assert enrollment.user_id == user
        assert enrollment.path_slug == "p1"

    async def test_idempotent_on_user_and_path(self) -> None:
        repo = _FakeRepo()
        repo.paths = {"p1": _path()}
        user = uuid.uuid4()
        uc = EnrollInPath(repo=repo)
        first = await uc.execute(user_id=user, path_slug="p1")
        second = await uc.execute(user_id=user, path_slug="p1")
        assert first.id == second.id
        assert len(repo.enrollments) == 1

    async def test_missing_path_raises(self) -> None:
        repo = _FakeRepo()
        with pytest.raises(LearningContentNotFoundError):
            await EnrollInPath(repo=repo).execute(user_id=uuid.uuid4(), path_slug="missing")


class TestUpdateModuleProgress:
    async def test_creates_then_updates_in_place(self) -> None:
        repo = _FakeRepo()
        user = uuid.uuid4()
        uc = UpdateModuleProgress(repo=repo)
        first = await uc.execute(user_id=user, module_slug="m1", percent=30)
        second = await uc.execute(user_id=user, module_slug="m1", percent=80)
        assert first.id == second.id
        assert second.percent == 80
        assert len(repo.progress) == 1

    async def test_hits_100_marks_complete(self) -> None:
        repo = _FakeRepo()
        user = uuid.uuid4()
        uc = UpdateModuleProgress(repo=repo)
        p = await uc.execute(user_id=user, module_slug="m1", percent=100)
        assert p.is_completed


class TestGetMyLearningState:
    async def test_bundles_enrollment_progress_certificates(self) -> None:
        repo = _FakeRepo()
        repo.paths = {"p1": _path()}
        user = uuid.uuid4()
        await EnrollInPath(repo=repo).execute(user_id=user, path_slug="p1")
        await UpdateModuleProgress(repo=repo).execute(user_id=user, module_slug="m1", percent=100)
        await UpdateModuleProgress(repo=repo).execute(user_id=user, module_slug="m2", percent=100)
        # No cert yet.
        state = await GetMyLearningState(repo=repo).execute(user)
        assert len(state.enrollments) == 1
        assert set(state.progress_by_module) == {"m1", "m2"}
        assert state.certificates == []


class TestIssueCertificate:
    async def test_eligible_user_gets_cert(self) -> None:
        repo = _FakeRepo()
        repo.paths = {"p1": _path()}
        user = uuid.uuid4()
        await UpdateModuleProgress(repo=repo).execute(user_id=user, module_slug="m1", percent=100)
        await UpdateModuleProgress(repo=repo).execute(user_id=user, module_slug="m2", percent=100)
        cert = await IssueCertificate(repo=repo, signer=_StubSigner()).execute(
            user_id=user, path_slug="p1"
        )
        assert cert.user_id == user
        assert (user, "p1") in repo.certs

    async def test_ineligible_user_raises(self) -> None:
        repo = _FakeRepo()
        repo.paths = {"p1": _path()}
        user = uuid.uuid4()
        await UpdateModuleProgress(repo=repo).execute(user_id=user, module_slug="m1", percent=50)
        with pytest.raises(CertificateNotEligibleError):
            await IssueCertificate(repo=repo, signer=_StubSigner()).execute(
                user_id=user, path_slug="p1"
            )

    async def test_missing_path_raises(self) -> None:
        repo = _FakeRepo()
        with pytest.raises(LearningContentNotFoundError):
            await IssueCertificate(repo=repo, signer=_StubSigner()).execute(
                user_id=uuid.uuid4(), path_slug="missing"
            )


# Suppress unused-import warning — datetime kept for future date-pinned tests.
_ = datetime(2026, 1, 1, tzinfo=UTC)
