"""Use-case tests for the uploads context, with fakes."""

from __future__ import annotations

import uuid
from uuid import UUID

import pytest

from cyberdyne_backend.application.uploads import (
    GetUpload,
    SaveUpload,
    SaveUploads,
    UploadInput,
)
from cyberdyne_backend.domain.uploads import (
    FileStorage,
    FileTooLargeError,
    StoredFile,
    UnsupportedMediaTypeError,
    UploadCategory,
    UploadNotFoundError,
    UploadRepository,
)


class FakeStorage:
    def __init__(self) -> None:
        self.saved: dict[str, bytes] = {}

    async def save(self, *, category: UploadCategory, stored_filename: str, data: bytes) -> str:
        rel = f"{category.value}/{stored_filename}"
        self.saved[rel] = data
        return rel

    async def delete(self, relative_path: str) -> None:
        self.saved.pop(relative_path, None)


class FakeUploadRepo:
    def __init__(self) -> None:
        self.by_id: dict[UUID, StoredFile] = {}

    async def save(self, stored: StoredFile) -> None:
        self.by_id[stored.id] = stored

    async def get(self, upload_id: UUID) -> StoredFile:
        stored = self.by_id.get(upload_id)
        if stored is None:
            raise UploadNotFoundError(str(upload_id))
        return stored


def test_fakes_match_ports() -> None:
    assert isinstance(FakeStorage(), FileStorage)
    assert isinstance(FakeUploadRepo(), UploadRepository)


def _uc(repo: FakeUploadRepo, storage: FakeStorage) -> SaveUpload:
    return SaveUpload(repo=repo, storage=storage, media_url_prefix="/media")


class TestSaveUpload:
    async def test_happy_path(self) -> None:
        repo, storage = FakeUploadRepo(), FakeStorage()
        stored = await _uc(repo, storage).execute(
            UploadInput(filename="hero.png", content_type="image/png", data=b"x" * 100),
            uploaded_by=uuid.uuid4(),
        )
        assert stored.category is UploadCategory.IMAGE
        assert stored.stored_filename.endswith(".png")
        assert stored.url == f"/media/image/{stored.stored_filename}"
        assert stored.size_bytes == 100
        # Persisted to both storage and repo.
        assert stored.relative_path in storage.saved
        assert repo.by_id[stored.id] is stored

    async def test_original_filename_sanitised(self) -> None:
        repo, storage = FakeUploadRepo(), FakeStorage()
        stored = await _uc(repo, storage).execute(
            UploadInput(
                filename="../../../etc/passwd.png",
                content_type="image/png",
                data=b"x",
            )
        )
        assert stored.original_filename == "passwd.png"

    async def test_unsupported_type_raises_and_writes_nothing(self) -> None:
        repo, storage = FakeUploadRepo(), FakeStorage()
        with pytest.raises(UnsupportedMediaTypeError):
            await _uc(repo, storage).execute(
                UploadInput(filename="x.exe", content_type="application/x-msdownload", data=b"x")
            )
        assert storage.saved == {}
        assert repo.by_id == {}

    async def test_oversize_raises_before_persist(self) -> None:
        repo, storage = FakeUploadRepo(), FakeStorage()
        with pytest.raises(FileTooLargeError):
            await _uc(repo, storage).execute(
                UploadInput(
                    filename="big.png",
                    content_type="image/png",
                    data=b"x" * (11 * 1024 * 1024),
                )
            )
        assert storage.saved == {}


class TestSaveUploads:
    async def test_batch(self) -> None:
        repo, storage = FakeUploadRepo(), FakeStorage()
        uc = SaveUploads(inner=_uc(repo, storage))
        results = await uc.execute(
            [
                UploadInput(filename="a.png", content_type="image/png", data=b"a"),
                UploadInput(filename="b.pdf", content_type="application/pdf", data=b"b"),
            ]
        )
        assert {r.category for r in results} == {UploadCategory.IMAGE, UploadCategory.DOCUMENT}
        assert len(storage.saved) == 2


class TestGetUpload:
    async def test_get(self) -> None:
        repo, storage = FakeUploadRepo(), FakeStorage()
        stored = await _uc(repo, storage).execute(
            UploadInput(filename="a.png", content_type="image/png", data=b"a")
        )
        fetched = await GetUpload(repo=repo).execute(stored.id)
        assert fetched.id == stored.id

    async def test_missing_raises(self) -> None:
        with pytest.raises(UploadNotFoundError):
            await GetUpload(repo=FakeUploadRepo()).execute(uuid.uuid4())
