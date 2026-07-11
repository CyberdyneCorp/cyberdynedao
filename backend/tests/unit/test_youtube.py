"""Unit tests for the youtube context: reference parsing, use cases, and
the outbound client's error mapping (third-party libs stubbed)."""

from __future__ import annotations

import pytest
import yt_dlp
from youtube_transcript_api import (
    CouldNotRetrieveTranscript,
    TranscriptsDisabled,
    VideoUnavailable,
)

from cyberdyne_backend.adapters.outbound.youtube import YouTubeContentClient
from cyberdyne_backend.application.youtube import GetVideoTranscript, ListPlaylistVideos
from cyberdyne_backend.domain.youtube import (
    InvalidYouTubeReferenceError,
    Playlist,
    PlaylistNotFoundError,
    PlaylistVideo,
    TranscriptUnavailableError,
    VideoNotFoundError,
    VideoTranscript,
    YouTubeUnavailableError,
    parse_playlist_id,
    parse_video_id,
)

_VID = "yhGzXULZkEw"
_PLID = "PLQ-uHSnFig5M9fW16o2l35jrfdsxGknNB"


class TestReferenceParsing:
    @pytest.mark.parametrize(
        "reference",
        [
            _VID,
            f"https://www.youtube.com/watch?v={_VID}",
            f"https://www.youtube.com/watch?feature=share&v={_VID}",
            f"https://youtu.be/{_VID}",
            f"https://youtu.be/{_VID}?t=42",
            f"https://www.youtube.com/embed/{_VID}",
            f"https://www.youtube.com/shorts/{_VID}",
            f"  https://www.youtube.com/watch?v={_VID}&list={_PLID}  ",
        ],
    )
    def test_video_references(self, reference: str) -> None:
        assert parse_video_id(reference) == _VID

    @pytest.mark.parametrize(
        "reference",
        ["", "not a url", "https://vimeo.com/12345", "shortid", _PLID],
    )
    def test_invalid_video_references(self, reference: str) -> None:
        with pytest.raises(InvalidYouTubeReferenceError):
            parse_video_id(reference)

    @pytest.mark.parametrize(
        "reference",
        [
            _PLID,
            f"https://www.youtube.com/playlist?list={_PLID}",
            f"https://www.youtube.com/watch?v={_VID}&list={_PLID}&index=3",
        ],
    )
    def test_playlist_references(self, reference: str) -> None:
        assert parse_playlist_id(reference) == _PLID

    @pytest.mark.parametrize(
        "reference",
        ["", "not a url", f"https://youtu.be/{_VID}", _VID],
    )
    def test_invalid_playlist_references(self, reference: str) -> None:
        with pytest.raises(InvalidYouTubeReferenceError):
            parse_playlist_id(reference)


class _FakePort:
    def __init__(self) -> None:
        self.transcript_calls: list[tuple[str, str]] = []
        self.playlist_calls: list[str] = []

    async def fetch_transcript(self, video_id: str, language: str) -> VideoTranscript:
        self.transcript_calls.append((video_id, language))
        return VideoTranscript(video_id=video_id, language=language, text="hello world")

    async def fetch_playlist(self, playlist_id: str) -> Playlist:
        self.playlist_calls.append(playlist_id)
        return Playlist(
            playlist_id=playlist_id,
            title="T",
            channel="C",
            videos=(PlaylistVideo(video_id=_VID, title="v", duration_s=60),),
        )


class TestUseCases:
    async def test_transcript_parses_reference_and_defaults_language(self) -> None:
        port = _FakePort()
        result = await GetVideoTranscript(content=port).execute(f"https://youtu.be/{_VID}")
        assert result.text == "hello world"
        assert result.url.endswith(_VID)
        assert port.transcript_calls == [(_VID, "en")]

    async def test_transcript_passes_language_and_rejects_blank(self) -> None:
        port = _FakePort()
        await GetVideoTranscript(content=port).execute(_VID, language="pt-BR")
        await GetVideoTranscript(content=port).execute(_VID, language="   ")
        assert port.transcript_calls == [(_VID, "pt-BR"), (_VID, "en")]

    async def test_playlist_parses_reference(self) -> None:
        port = _FakePort()
        result = await ListPlaylistVideos(content=port).execute(
            f"https://www.youtube.com/playlist?list={_PLID}"
        )
        assert port.playlist_calls == [_PLID]
        assert result.url.endswith(_PLID)
        assert result.videos[0].url == f"https://www.youtube.com/watch?v={_VID}"


class _Snippet:
    def __init__(self, text: str) -> None:
        self.text = text


class _Fetched:
    language_code = "en"

    @property
    def snippets(self) -> list[_Snippet]:
        return [_Snippet("hello "), _Snippet("  "), _Snippet("world")]


class TestContentClientTranscripts:
    async def test_maps_snippets_to_plain_text(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            "cyberdyne_backend.adapters.outbound.youtube.client.YouTubeTranscriptApi",
            lambda: type("A", (), {"fetch": lambda self, vid, languages: _Fetched()})(),
        )
        result = await YouTubeContentClient().fetch_transcript(_VID, "en")
        assert result.text == "hello world"
        assert result.language == "en"

    @pytest.mark.parametrize(
        ("raised", "expected"),
        [
            (TranscriptsDisabled(_VID), TranscriptUnavailableError),
            (VideoUnavailable(_VID), VideoNotFoundError),
            (CouldNotRetrieveTranscript(_VID), YouTubeUnavailableError),
        ],
    )
    async def test_maps_library_errors_to_domain(
        self, monkeypatch: pytest.MonkeyPatch, raised: Exception, expected: type[Exception]
    ) -> None:
        def _raise(self: object, vid: str, languages: list[str]) -> None:
            raise raised

        monkeypatch.setattr(
            "cyberdyne_backend.adapters.outbound.youtube.client.YouTubeTranscriptApi",
            lambda: type("A", (), {"fetch": _raise})(),
        )
        with pytest.raises(expected):
            await YouTubeContentClient().fetch_transcript(_VID, "en")


class _FakeYDL:
    def __init__(self, info: dict | None = None, error: Exception | None = None) -> None:
        self._info = info
        self._error = error

    def __call__(self, opts: dict) -> _FakeYDL:
        return self

    def __enter__(self) -> _FakeYDL:
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def extract_info(self, url: str, download: bool = False) -> dict | None:
        if self._error is not None:
            raise self._error
        return self._info


class TestContentClientPlaylists:
    async def test_maps_flat_entries(self, monkeypatch: pytest.MonkeyPatch) -> None:
        info = {
            "title": "Startup School",
            "channel": "Y Combinator",
            "entries": [
                {"id": _VID, "title": "Talk", "duration": 1099.0},
                {"id": "AAAAAAAAAAA", "title": None, "duration": None},
                None,  # yt-dlp emits None for unavailable entries
            ],
        }
        monkeypatch.setattr(
            "cyberdyne_backend.adapters.outbound.youtube.client.yt_dlp.YoutubeDL",
            _FakeYDL(info=info),
        )
        playlist = await YouTubeContentClient().fetch_playlist(_PLID)
        assert playlist.title == "Startup School"
        assert playlist.channel == "Y Combinator"
        assert [v.video_id for v in playlist.videos] == [_VID, "AAAAAAAAAAA"]
        assert playlist.videos[0].duration_s == 1099
        assert playlist.videos[1].duration_s is None

    async def test_maps_not_found_and_unavailable(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            "cyberdyne_backend.adapters.outbound.youtube.client.yt_dlp.YoutubeDL",
            _FakeYDL(error=yt_dlp.utils.DownloadError("This playlist does not exist")),
        )
        with pytest.raises(PlaylistNotFoundError):
            await YouTubeContentClient().fetch_playlist(_PLID)

        monkeypatch.setattr(
            "cyberdyne_backend.adapters.outbound.youtube.client.yt_dlp.YoutubeDL",
            _FakeYDL(error=yt_dlp.utils.DownloadError("timed out")),
        )
        with pytest.raises(YouTubeUnavailableError):
            await YouTubeContentClient().fetch_playlist(_PLID)

    async def test_empty_info_is_not_found(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            "cyberdyne_backend.adapters.outbound.youtube.client.yt_dlp.YoutubeDL",
            _FakeYDL(info=None),
        )
        with pytest.raises(PlaylistNotFoundError):
            await YouTubeContentClient().fetch_playlist(_PLID)
