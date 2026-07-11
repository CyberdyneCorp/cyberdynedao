"""YouTube use cases — transcript + playlist reads for the chat agents."""

from __future__ import annotations

from dataclasses import dataclass

from cyberdyne_backend.domain.youtube import (
    Playlist,
    VideoTranscript,
    YouTubeContentPort,
    parse_playlist_id,
    parse_video_id,
)

DEFAULT_TRANSCRIPT_LANGUAGE = "en"


@dataclass(slots=True)
class GetVideoTranscript:
    """Returns a video's transcript as plain text.

    Accepts any recognizable video reference (watch/short/embed URL or a
    bare 11-character id) and a preferred language; the port may fall
    back to another available language and reports which one it used.
    """

    content: YouTubeContentPort

    async def execute(
        self, reference: str, language: str = DEFAULT_TRANSCRIPT_LANGUAGE
    ) -> VideoTranscript:
        video_id = parse_video_id(reference)
        return await self.content.fetch_transcript(video_id, language.strip() or "en")


@dataclass(slots=True)
class ListPlaylistVideos:
    """Returns a playlist's metadata and its ordered video URLs.

    Accepts a playlist URL (anything carrying ``list=``) or a bare
    playlist id.
    """

    content: YouTubeContentPort

    async def execute(self, reference: str) -> Playlist:
        playlist_id = parse_playlist_id(reference)
        return await self.content.fetch_playlist(playlist_id)
