"""Errors for the youtube context."""

from __future__ import annotations


class YouTubeError(Exception):
    """Base class for youtube-context errors."""


class InvalidYouTubeReferenceError(YouTubeError):
    """The given string is not a recognizable YouTube video/playlist URL or id."""


class TranscriptUnavailableError(YouTubeError):
    """The video exists but has no transcript (captions disabled or none in
    the requested language)."""


class VideoNotFoundError(YouTubeError):
    """The video does not exist or is private/removed."""


class PlaylistNotFoundError(YouTubeError):
    """The playlist does not exist or is private/removed."""


class YouTubeUnavailableError(YouTubeError):
    """YouTube could not be reached or rejected the request (network error,
    throttling) — retryable, not the caller's fault."""
