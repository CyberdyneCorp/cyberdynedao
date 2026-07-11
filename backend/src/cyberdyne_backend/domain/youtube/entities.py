"""YouTube domain entities + URL parsing.

The youtube context wraps read-only access to public YouTube content:
a video's transcript (closed captions) and a playlist's video listing.
It exists to feed the chat agents grounded source material - it stores
nothing and owns no persistence.

URL parsing lives in the domain because "what counts as a video/playlist
reference" is a business rule shared by every adapter and caller: full
watch URLs, short youtu.be links, embed URLs, share URLs with extra query
parameters, and bare ids are all accepted.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from cyberdyne_backend.domain.youtube.errors import InvalidYouTubeReferenceError

# Video ids are exactly 11 URL-safe base64 characters. Playlist ids are
# longer ("PL...", "UU...", "OL...", etc.) — accept the documented charset
# with a sane length range instead of enumerating prefixes.
_VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
_PLAYLIST_ID_RE = re.compile(r"^[A-Za-z0-9_-]{12,64}$")

_VIDEO_URL_RE = re.compile(
    r"(?:youtube\.com/(?:watch\?(?:.*&)?v=|embed/|shorts/|live/)|youtu\.be/)"
    r"([A-Za-z0-9_-]{11})"
)
_PLAYLIST_URL_RE = re.compile(r"[?&]list=([A-Za-z0-9_-]{12,64})")


def parse_video_id(reference: str) -> str:
    """Extract the 11-character video id from a URL or bare id."""
    ref = reference.strip()
    if not ref:
        raise InvalidYouTubeReferenceError("empty video reference")
    match = _VIDEO_URL_RE.search(ref)
    if match:
        return match.group(1)
    if _VIDEO_ID_RE.match(ref):
        return ref
    raise InvalidYouTubeReferenceError(f"not a YouTube video URL or id: {reference!r}")


def parse_playlist_id(reference: str) -> str:
    """Extract the playlist id from a URL or bare id."""
    ref = reference.strip()
    if not ref:
        raise InvalidYouTubeReferenceError("empty playlist reference")
    match = _PLAYLIST_URL_RE.search(ref)
    if match:
        return match.group(1)
    # A bare video id is 11 chars; playlist ids are longer, so the two
    # bare-id forms cannot collide.
    if _PLAYLIST_ID_RE.match(ref) and not _VIDEO_ID_RE.match(ref):
        return ref
    raise InvalidYouTubeReferenceError(f"not a YouTube playlist URL or id: {reference!r}")


def video_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"


def playlist_url(playlist_id: str) -> str:
    return f"https://www.youtube.com/playlist?list={playlist_id}"


@dataclass(frozen=True, slots=True)
class VideoTranscript:
    """A video's closed-caption transcript as plain text."""

    video_id: str
    language: str  # BCP-47 code of the transcript actually fetched
    text: str

    @property
    def url(self) -> str:
        return video_url(self.video_id)


@dataclass(frozen=True, slots=True)
class PlaylistVideo:
    """One entry of a playlist listing."""

    video_id: str
    title: str
    duration_s: int | None = None

    @property
    def url(self) -> str:
        return video_url(self.video_id)


@dataclass(frozen=True, slots=True)
class Playlist:
    """A playlist's metadata and ordered video listing."""

    playlist_id: str
    title: str
    channel: str | None = None
    videos: tuple[PlaylistVideo, ...] = field(default_factory=tuple)

    @property
    def url(self) -> str:
        return playlist_url(self.playlist_id)
