"""API tests for the youtube endpoints: auth gating, response shape, and
error mapping. The YouTube port is faked — no network."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.api.youtube.router import (
    get_list_playlist_videos_uc,
    get_video_transcript_uc,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.application.youtube import GetVideoTranscript, ListPlaylistVideos
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.youtube import (
    Playlist,
    PlaylistNotFoundError,
    PlaylistVideo,
    TranscriptUnavailableError,
    VideoTranscript,
    YouTubeUnavailableError,
)

pytestmark = pytest.mark.integration

_VID = "yhGzXULZkEw"
_PLID = "PLQ-uHSnFig5M9fW16o2l35jrfdsxGknNB"


def _learner() -> UserPrincipal:
    return UserPrincipal(
        user_id=uuid.uuid4(),
        username="l",
        scopes=frozenset(),
        audience=None,
        expires_at=datetime(2026, 7, 1, tzinfo=UTC),
    )


class _Port:
    def __init__(
        self, transcript_error: Exception | None = None, playlist_error: Exception | None = None
    ) -> None:
        self._transcript_error = transcript_error
        self._playlist_error = playlist_error

    async def fetch_transcript(self, video_id: str, language: str) -> VideoTranscript:
        if self._transcript_error is not None:
            raise self._transcript_error
        return VideoTranscript(video_id=video_id, language=language, text="hello world")

    async def fetch_playlist(self, playlist_id: str) -> Playlist:
        if self._playlist_error is not None:
            raise self._playlist_error
        return Playlist(
            playlist_id=playlist_id,
            title="Startup School",
            channel="Y Combinator",
            videos=(PlaylistVideo(video_id=_VID, title="Talk", duration_s=1099),),
        )


def _client(app: FastAPI, port: _Port) -> TestClient:
    app.dependency_overrides[require_principal] = _learner
    app.dependency_overrides[get_video_transcript_uc] = lambda: GetVideoTranscript(content=port)
    app.dependency_overrides[get_list_playlist_videos_uc] = lambda: ListPlaylistVideos(content=port)
    return TestClient(app)


class TestTranscriptEndpoint:
    def test_requires_authentication(self, app: FastAPI) -> None:
        client = TestClient(app)
        response = client.get("/api/v1/youtube/transcript", params={"video": _VID})
        assert response.status_code == 401

    def test_returns_transcript(self, app: FastAPI) -> None:
        client = _client(app, _Port())
        response = client.get(
            "/api/v1/youtube/transcript",
            params={"video": f"https://youtu.be/{_VID}", "lang": "pt-BR"},
        )
        assert response.status_code == 200
        body = response.json()
        assert body == {
            "videoId": _VID,
            "url": f"https://www.youtube.com/watch?v={_VID}",
            "language": "pt-BR",
            "text": "hello world",
        }

    def test_invalid_reference_is_422(self, app: FastAPI) -> None:
        # NB: any 11 chars of [A-Za-z0-9_-] IS a valid video id (so a string
        # like "not-a-video" would parse); use an unmistakably foreign URL.
        client = _client(app, _Port())
        response = client.get(
            "/api/v1/youtube/transcript", params={"video": "https://vimeo.com/12345"}
        )
        assert response.status_code == 422

    def test_unavailable_transcript_is_404(self, app: FastAPI) -> None:
        client = _client(app, _Port(transcript_error=TranscriptUnavailableError("none")))
        response = client.get("/api/v1/youtube/transcript", params={"video": _VID})
        assert response.status_code == 404

    def test_youtube_down_is_503(self, app: FastAPI) -> None:
        client = _client(app, _Port(transcript_error=YouTubeUnavailableError("blocked")))
        response = client.get("/api/v1/youtube/transcript", params={"video": _VID})
        assert response.status_code == 503


class TestPlaylistEndpoint:
    def test_requires_authentication(self, app: FastAPI) -> None:
        client = TestClient(app)
        response = client.get("/api/v1/youtube/playlist", params={"playlist": _PLID})
        assert response.status_code == 401

    def test_returns_listing(self, app: FastAPI) -> None:
        client = _client(app, _Port())
        response = client.get(
            "/api/v1/youtube/playlist",
            params={"playlist": f"https://www.youtube.com/playlist?list={_PLID}"},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["playlistId"] == _PLID
        assert body["url"] == f"https://www.youtube.com/playlist?list={_PLID}"
        assert body["title"] == "Startup School"
        assert body["channel"] == "Y Combinator"
        assert body["videos"] == [
            {
                "videoId": _VID,
                "url": f"https://www.youtube.com/watch?v={_VID}",
                "title": "Talk",
                "durationS": 1099,
            }
        ]

    def test_invalid_reference_is_422(self, app: FastAPI) -> None:
        client = _client(app, _Port())
        response = client.get("/api/v1/youtube/playlist", params={"playlist": "nope"})
        assert response.status_code == 422

    def test_missing_playlist_is_404(self, app: FastAPI) -> None:
        client = _client(app, _Port(playlist_error=PlaylistNotFoundError("gone")))
        response = client.get("/api/v1/youtube/playlist", params={"playlist": _PLID})
        assert response.status_code == 404
