"""Wire schemas for the youtube endpoints."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class TranscriptResponse(_CamelModel):
    video_id: str
    url: str
    language: str
    text: str


class PlaylistVideoResponse(_CamelModel):
    video_id: str
    url: str
    title: str
    duration_s: int | None = None


class PlaylistResponse(_CamelModel):
    playlist_id: str
    url: str
    title: str
    channel: str | None = None
    videos: list[PlaylistVideoResponse]
