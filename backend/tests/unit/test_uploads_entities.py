"""Domain tests for the uploads context — policy + filename safety."""

from __future__ import annotations

import pytest

from cyberdyne_backend.domain.uploads import (
    MAX_UPLOAD_BYTES,
    FileTooLargeError,
    UnsafeFilenameError,
    UnsupportedMediaTypeError,
    UploadCategory,
    build_stored_filename,
    classify,
    safe_display_name,
    validate_size,
)


class TestClassify:
    @pytest.mark.parametrize(
        ("mime", "category", "ext"),
        [
            ("image/png", UploadCategory.IMAGE, ".png"),
            ("image/jpeg", UploadCategory.IMAGE, ".jpg"),
            ("application/pdf", UploadCategory.DOCUMENT, ".pdf"),
            (
                "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                UploadCategory.PRESENTATION,
                ".pptx",
            ),
            ("video/mp4", UploadCategory.VIDEO, ".mp4"),
            ("video/webm", UploadCategory.VIDEO, ".webm"),
        ],
    )
    def test_known_types(self, mime: str, category: UploadCategory, ext: str) -> None:
        c = classify(mime)
        assert c.category is category
        assert c.extension == ext

    def test_strips_parameters(self) -> None:
        assert classify("image/png; charset=binary").category is UploadCategory.IMAGE

    def test_unknown_type_raises(self) -> None:
        with pytest.raises(UnsupportedMediaTypeError):
            classify("application/x-msdownload")

    def test_executable_disguised_is_rejected(self) -> None:
        with pytest.raises(UnsupportedMediaTypeError):
            classify("text/html")


class TestSize:
    def test_within_cap_ok(self) -> None:
        validate_size(classify("image/png"), 5 * 1024 * 1024)

    def test_over_cap_raises(self) -> None:
        # Image cap is 10MB.
        with pytest.raises(FileTooLargeError):
            validate_size(classify("image/png"), 11 * 1024 * 1024)

    def test_video_cap_is_largest(self) -> None:
        assert classify("video/mp4").max_bytes == MAX_UPLOAD_BYTES


class TestSafeFilename:
    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ("photo.png", "photo.png"),
            ("../../etc/passwd", "passwd"),
            ("/abs/path/report.pdf", "report.pdf"),
            ("..\\..\\windows\\system32\\evil.dll", "evil.dll"),
            ("my file (1).png", "my_file_1_.png"),
        ],
    )
    def test_sanitises(self, raw: str, expected: str) -> None:
        assert safe_display_name(raw) == expected

    def test_leading_dots_stripped(self) -> None:
        assert safe_display_name("...hidden") == "hidden"

    def test_unusable_raises(self) -> None:
        with pytest.raises(UnsafeFilenameError):
            safe_display_name("///")

    def test_empty_raises(self) -> None:
        with pytest.raises(UnsafeFilenameError):
            safe_display_name("   ")


class TestStoredFilename:
    def test_uuid_with_canonical_extension(self) -> None:
        name = build_stored_filename(classify("image/jpeg"))
        assert name.endswith(".jpg")
        # No path separators, no traversal.
        assert "/" not in name and "\\" not in name and ".." not in name
        assert len(name) > len(".jpg")
