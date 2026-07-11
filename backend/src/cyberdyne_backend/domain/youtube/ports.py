"""Ports for the youtube context."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from cyberdyne_backend.domain.youtube.entities import Playlist, VideoTranscript


@runtime_checkable
class YouTubeContentPort(Protocol):
    """Reads public YouTube content (transcripts, playlist listings).

    Implementations talk to YouTube over HTTP and may be throttled by
    it; callers should expect ``YouTubeUnavailableError`` and treat the
    data as a best-effort snapshot of public content.
    """

    async def fetch_transcript(self, video_id: str, language: str) -> VideoTranscript: ...

    async def fetch_playlist(self, playlist_id: str) -> Playlist: ...
