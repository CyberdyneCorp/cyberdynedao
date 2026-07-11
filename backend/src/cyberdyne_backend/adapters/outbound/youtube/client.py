"""YouTube content client — transcripts via youtube-transcript-api,
playlist listings via yt-dlp (flat extraction, no media download).

Both libraries are synchronous; calls are pushed to a worker thread so
the event loop never blocks on YouTube's latency. YouTube throttles
datacenter IPs aggressively at times — network/parse failures map to
``YouTubeUnavailableError`` so callers can distinguish "retry later"
from "this video has no captions".
"""

from __future__ import annotations

import asyncio
import logging

import yt_dlp
from youtube_transcript_api import (
    CouldNotRetrieveTranscript,
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
    YouTubeTranscriptApi,
)

from cyberdyne_backend.domain.youtube import (
    Playlist,
    PlaylistNotFoundError,
    PlaylistVideo,
    TranscriptUnavailableError,
    VideoNotFoundError,
    VideoTranscript,
    YouTubeUnavailableError,
    playlist_url,
)

logger = logging.getLogger(__name__)

_YDL_OPTS = {
    "quiet": True,
    "no_warnings": True,
    "skip_download": True,
    "extract_flat": "in_playlist",  # listing only — never resolve each video
}

# yt-dlp reports every failure as DownloadError; these fragments tell a
# missing/private playlist apart from YouTube being unreachable.
_NOT_FOUND_FRAGMENTS = ("does not exist", "not exist", "private", "unavailable", "removed")


class YouTubeContentClient:
    """``YouTubeContentPort`` implementation over public YouTube."""

    async def fetch_transcript(self, video_id: str, language: str) -> VideoTranscript:
        return await asyncio.to_thread(self._fetch_transcript_sync, video_id, language)

    async def fetch_playlist(self, playlist_id: str) -> Playlist:
        return await asyncio.to_thread(self._fetch_playlist_sync, playlist_id)

    def _fetch_transcript_sync(self, video_id: str, language: str) -> VideoTranscript:
        # Prefer the requested language, fall back to English; the result
        # reports which one was actually found.
        languages = [language] if language == "en" else [language, "en"]
        try:
            fetched = YouTubeTranscriptApi().fetch(video_id, languages=languages)
        except (TranscriptsDisabled, NoTranscriptFound) as exc:
            raise TranscriptUnavailableError(
                f"no transcript available for video {video_id} in {languages}"
            ) from exc
        except VideoUnavailable as exc:
            raise VideoNotFoundError(f"video {video_id} does not exist or is private") from exc
        except CouldNotRetrieveTranscript as exc:
            # Base class of the library's failures — anything else (IP block,
            # request failure) is YouTube's side, not the caller's.
            raise YouTubeUnavailableError(f"could not reach YouTube: {exc}") from exc
        text = " ".join(
            snippet.text.strip() for snippet in fetched.snippets if snippet.text.strip()
        )
        return VideoTranscript(video_id=video_id, language=fetched.language_code, text=text)

    def _fetch_playlist_sync(self, playlist_id: str) -> Playlist:
        try:
            with yt_dlp.YoutubeDL(_YDL_OPTS) as ydl:
                info = ydl.extract_info(playlist_url(playlist_id), download=False)
        except yt_dlp.utils.DownloadError as exc:
            message = str(exc).lower()
            if any(fragment in message for fragment in _NOT_FOUND_FRAGMENTS):
                raise PlaylistNotFoundError(
                    f"playlist {playlist_id} does not exist or is private"
                ) from exc
            raise YouTubeUnavailableError(f"could not reach YouTube: {exc}") from exc
        if not info:
            raise PlaylistNotFoundError(f"playlist {playlist_id} returned no data")
        videos = tuple(
            PlaylistVideo(
                video_id=entry["id"],
                title=entry.get("title") or "",
                duration_s=int(entry["duration"]) if entry.get("duration") else None,
            )
            for entry in (info.get("entries") or [])
            if entry and entry.get("id")
        )
        return Playlist(
            playlist_id=playlist_id,
            title=info.get("title") or playlist_id,
            channel=info.get("channel") or info.get("uploader"),
            videos=videos,
        )
