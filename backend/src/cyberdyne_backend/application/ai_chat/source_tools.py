"""External source tools shared by both chat agents (the AI Tutor and the
answer agent): open-web search and YouTube (transcript + playlist).

The tool *schemas* (what the LLM sees) and the *handlers* (which run a
use case and JSON-stringify the result for the model's next turn) live
here once so both agents expose an identical surface. The handlers cap
their payloads — a transcript or a big playlist must not blow the prompt.
"""

from __future__ import annotations

import json
from typing import Any

from cyberdyne_backend.application.websearch import SearchWeb
from cyberdyne_backend.application.youtube import GetVideoTranscript, ListPlaylistVideos
from cyberdyne_backend.domain.ai_chat.ports import ToolSchema
from cyberdyne_backend.domain.websearch import (
    InvalidQueryError,
    SearchProviderError,
    SearchUnavailableError,
)
from cyberdyne_backend.domain.youtube import (
    InvalidYouTubeReferenceError,
    PlaylistNotFoundError,
    TranscriptUnavailableError,
    VideoNotFoundError,
    YouTubeUnavailableError,
)

# Payload caps so a tool result never blows the prompt budget.
_MAX_TRANSCRIPT_CHARS = 8000
_MAX_PLAYLIST_VIDEOS = 100
_MAX_SEARCH_RESULTS = 10


WEB_SEARCH_TOOL = ToolSchema(
    name="web_search",
    description=(
        "Search the public web (Google) for current, real-world, or open-ended information "
        "that is NOT part of Cyberdyne's own courses/docs/projects. Use for recent events, "
        "external facts, people, definitions, or anything beyond this platform. Returns result "
        "titles, URLs and snippets, plus a direct answer when available. For Cyberdyne's OWN "
        "content use search_cyberdyne_knowledge instead."
    ),
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The search query."},
            "num_results": {
                "type": "integer",
                "description": "How many results to return (1-20, default 10).",
            },
        },
        "required": ["query"],
    },
)

YOUTUBE_TRANSCRIPT_TOOL = ToolSchema(
    name="youtube_transcript",
    description=(
        "Fetch the transcript (captions) of a public YouTube video as plain text. Use when the "
        "user shares a YouTube link or asks about the content of a specific video. Long "
        "transcripts are truncated."
    ),
    parameters={
        "type": "object",
        "properties": {
            "video": {
                "type": "string",
                "description": "YouTube video URL (watch/share/embed/youtu.be) or the 11-char id.",
            },
            "lang": {
                "type": "string",
                "description": "Preferred transcript language (BCP-47, e.g. 'en', 'pt'). Default en.",
            },
        },
        "required": ["video"],
    },
)

YOUTUBE_PLAYLIST_TOOL = ToolSchema(
    name="youtube_playlist",
    description=(
        "List the videos in a public YouTube playlist (title, channel, and each video's title + "
        "URL, in order). Use when the user shares a playlist link or asks what a playlist "
        "contains."
    ),
    parameters={
        "type": "object",
        "properties": {
            "playlist": {
                "type": "string",
                "description": "YouTube playlist URL (anything with list=) or the bare playlist id.",
            },
        },
        "required": ["playlist"],
    },
)

# Both agents append this to their tool set.
EXTERNAL_SOURCE_TOOLS: list[ToolSchema] = [
    WEB_SEARCH_TOOL,
    YOUTUBE_TRANSCRIPT_TOOL,
    YOUTUBE_PLAYLIST_TOOL,
]

EXTERNAL_SOURCE_TOOL_NAMES = frozenset(t.name for t in EXTERNAL_SOURCE_TOOLS)


def _err(message: str) -> str:
    return json.dumps({"error": message})


async def run_web_search(uc: SearchWeb | None, args: dict[str, Any]) -> str:
    if uc is None:
        return _err("web search is not available")
    query = str(args.get("query") or "")
    raw_num = args.get("num_results")
    num = int(raw_num) if isinstance(raw_num, int | float | str) and str(raw_num).isdigit() else 10
    try:
        result = await uc.execute(query, num_results=num)
    except InvalidQueryError:
        return _err("empty query")
    except SearchUnavailableError:
        return _err("web search is not configured")
    except SearchProviderError as exc:
        return _err(f"search engine error: {exc}")
    return json.dumps(
        {
            "query": result.query,
            "answer": result.answer,
            "results": [
                {"title": r.title, "url": r.url, "snippet": r.snippet}
                for r in result.results[:_MAX_SEARCH_RESULTS]
            ],
        }
    )


async def run_youtube_transcript(uc: GetVideoTranscript | None, args: dict[str, Any]) -> str:
    if uc is None:
        return _err("youtube transcript is not available")
    video = str(args.get("video") or "")
    lang = str(args.get("lang") or "en")
    try:
        transcript = await uc.execute(video, language=lang)
    except InvalidYouTubeReferenceError:
        return _err("not a valid YouTube video URL or id")
    except (VideoNotFoundError, TranscriptUnavailableError):
        return _err("no transcript available for that video")
    except YouTubeUnavailableError:
        return _err("could not reach YouTube (try again later)")
    text = transcript.text
    truncated = len(text) > _MAX_TRANSCRIPT_CHARS
    return json.dumps(
        {
            "videoId": transcript.video_id,
            "url": transcript.url,
            "language": transcript.language,
            "text": text[:_MAX_TRANSCRIPT_CHARS],
            "truncated": truncated,
        }
    )


async def run_youtube_playlist(uc: ListPlaylistVideos | None, args: dict[str, Any]) -> str:
    if uc is None:
        return _err("youtube playlist is not available")
    playlist = str(args.get("playlist") or "")
    try:
        listing = await uc.execute(playlist)
    except InvalidYouTubeReferenceError:
        return _err("not a valid YouTube playlist URL or id")
    except PlaylistNotFoundError:
        return _err("playlist not found or private")
    except YouTubeUnavailableError:
        return _err("could not reach YouTube (try again later)")
    return json.dumps(
        {
            "playlistId": listing.playlist_id,
            "url": listing.url,
            "title": listing.title,
            "channel": listing.channel,
            "videoCount": len(listing.videos),
            "videos": [
                {"title": v.title, "url": v.url} for v in listing.videos[:_MAX_PLAYLIST_VIDEOS]
            ],
        }
    )
