"""YouTube content endpoints — transcript + playlist reads.

Source-material fetchers for the chat agents (and any authenticated
client): given a public video, return its transcript as plain text;
given a public playlist, return its ordered video URLs. Authentication
is required so the API cannot be used as an anonymous YouTube proxy.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from cyberdyne_backend.adapters.inbound.api.youtube.schemas import (
    PlaylistResponse,
    PlaylistVideoResponse,
    TranscriptResponse,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.application.youtube import GetVideoTranscript, ListPlaylistVideos
from cyberdyne_backend.domain.auth_identity import Principal
from cyberdyne_backend.domain.youtube import (
    InvalidYouTubeReferenceError,
    Playlist,
    PlaylistNotFoundError,
    TranscriptUnavailableError,
    VideoNotFoundError,
    VideoTranscript,
    YouTubeUnavailableError,
)

router = APIRouter(prefix="/api/v1/youtube", tags=["youtube"])


async def get_video_transcript_uc() -> GetVideoTranscript:  # pragma: no cover - override target
    raise NotImplementedError


async def get_list_playlist_videos_uc() -> ListPlaylistVideos:  # pragma: no cover - override
    raise NotImplementedError


def _transcript_response(transcript: VideoTranscript) -> TranscriptResponse:
    return TranscriptResponse(
        video_id=transcript.video_id,
        url=transcript.url,
        language=transcript.language,
        text=transcript.text,
    )


def _playlist_response(playlist: Playlist) -> PlaylistResponse:
    return PlaylistResponse(
        playlist_id=playlist.playlist_id,
        url=playlist.url,
        title=playlist.title,
        channel=playlist.channel,
        videos=[
            PlaylistVideoResponse(
                video_id=video.video_id,
                url=video.url,
                title=video.title,
                duration_s=video.duration_s,
            )
            for video in playlist.videos
        ],
    )


@router.get("/transcript", response_model=TranscriptResponse, response_model_by_alias=True)
async def get_transcript(
    video: Annotated[str, Query(min_length=1, description="Video URL or 11-char id")],
    use_case: Annotated[GetVideoTranscript, Depends(get_video_transcript_uc)],
    _principal: Annotated[Principal, Depends(require_principal)],
    lang: Annotated[str, Query(max_length=8, description="Preferred BCP-47 language")] = "en",
) -> TranscriptResponse:
    try:
        transcript = await use_case.execute(video, language=lang)
    except InvalidYouTubeReferenceError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except (VideoNotFoundError, TranscriptUnavailableError) as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except YouTubeUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return _transcript_response(transcript)


@router.get("/playlist", response_model=PlaylistResponse, response_model_by_alias=True)
async def get_playlist(
    playlist: Annotated[str, Query(min_length=1, description="Playlist URL or id")],
    use_case: Annotated[ListPlaylistVideos, Depends(get_list_playlist_videos_uc)],
    _principal: Annotated[Principal, Depends(require_principal)],
) -> PlaylistResponse:
    try:
        listing = await use_case.execute(playlist)
    except InvalidYouTubeReferenceError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except PlaylistNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except YouTubeUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return _playlist_response(listing)
