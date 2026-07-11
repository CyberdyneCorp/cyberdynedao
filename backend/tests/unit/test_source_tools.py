"""Tests for the external source tools (web search + YouTube) shared by
both chat agents: the handlers, and that each agent's dispatcher routes
the three tool names to them."""

from __future__ import annotations

import json

import pytest

from cyberdyne_backend.application.ai_chat.source_tools import (
    EXTERNAL_SOURCE_TOOLS,
    run_web_search,
    run_youtube_playlist,
    run_youtube_transcript,
)
from cyberdyne_backend.application.websearch import SearchWeb
from cyberdyne_backend.application.youtube import GetVideoTranscript, ListPlaylistVideos
from cyberdyne_backend.domain.websearch import (
    SearchProviderError,
    SearchResponse,
    SearchResult,
)
from cyberdyne_backend.domain.youtube import (
    Playlist,
    PlaylistNotFoundError,
    PlaylistVideo,
    TranscriptUnavailableError,
    VideoTranscript,
)


class _SearchPort:
    def __init__(self, error: Exception | None = None) -> None:
        self._error = error

    async def search(self, query: str, *, num_results: int) -> SearchResponse:
        if self._error is not None:
            raise self._error
        return SearchResponse(
            query=query,
            answer="the answer",
            results=tuple(
                SearchResult(position=i, title=f"T{i}", url=f"https://{i}", snippet="s")
                for i in range(1, num_results + 1)
            ),
        )


class _YtPort:
    def __init__(self, error: Exception | None = None, text: str = "hello world") -> None:
        self._error = error
        self._text = text

    async def fetch_transcript(self, video_id: str, language: str) -> VideoTranscript:
        if self._error is not None:
            raise self._error
        return VideoTranscript(video_id=video_id, language=language, text=self._text)

    async def fetch_playlist(self, playlist_id: str) -> Playlist:
        if self._error is not None:
            raise self._error
        return Playlist(
            playlist_id=playlist_id,
            title="PL",
            channel="C",
            videos=tuple(PlaylistVideo(video_id=f"v{i:09d}", title=f"vid {i}") for i in range(150)),
        )


class TestWebSearchHandler:
    async def test_success(self) -> None:
        out = json.loads(await run_web_search(SearchWeb(provider=_SearchPort()), {"query": "hi"}))
        assert out["query"] == "hi"
        assert out["answer"] == "the answer"
        assert out["results"][0] == {"title": "T1", "url": "https://1", "snippet": "s"}

    async def test_none_use_case(self) -> None:
        out = json.loads(await run_web_search(None, {"query": "hi"}))
        assert "error" in out

    async def test_unconfigured(self) -> None:
        out = json.loads(await run_web_search(SearchWeb(provider=None), {"query": "hi"}))
        assert out["error"] == "web search is not configured"

    async def test_provider_error(self) -> None:
        uc = SearchWeb(provider=_SearchPort(error=SearchProviderError("quota")))
        out = json.loads(await run_web_search(uc, {"query": "hi"}))
        assert "search engine error" in out["error"]

    async def test_num_results_string_parsed(self) -> None:
        out = json.loads(
            await run_web_search(
                SearchWeb(provider=_SearchPort()), {"query": "hi", "num_results": "3"}
            )
        )
        assert len(out["results"]) == 3


class TestYoutubeTranscriptHandler:
    async def test_success(self) -> None:
        uc = GetVideoTranscript(content=_YtPort())
        out = json.loads(
            await run_youtube_transcript(uc, {"video": "https://youtu.be/abcdefghijk"})
        )
        assert out["videoId"] == "abcdefghijk"
        assert out["text"] == "hello world"
        assert out["truncated"] is False

    async def test_truncated(self) -> None:
        uc = GetVideoTranscript(content=_YtPort(text="x" * 20000))
        out = json.loads(await run_youtube_transcript(uc, {"video": "abcdefghijk"}))
        assert out["truncated"] is True
        assert len(out["text"]) == 8000

    async def test_no_transcript(self) -> None:
        uc = GetVideoTranscript(content=_YtPort(error=TranscriptUnavailableError("x")))
        out = json.loads(await run_youtube_transcript(uc, {"video": "abcdefghijk"}))
        assert "no transcript" in out["error"]

    async def test_invalid_reference(self) -> None:
        uc = GetVideoTranscript(content=_YtPort())
        out = json.loads(await run_youtube_transcript(uc, {"video": "https://vimeo.com/1"}))
        assert "not a valid" in out["error"]


class TestYoutubePlaylistHandler:
    async def test_success_and_cap(self) -> None:
        uc = ListPlaylistVideos(content=_YtPort())
        out = json.loads(
            await run_youtube_playlist(
                uc, {"playlist": "https://www.youtube.com/playlist?list=PL0123456789ab"}
            )
        )
        assert out["title"] == "PL"
        assert out["videoCount"] == 150  # true total reported
        assert len(out["videos"]) == 100  # payload capped

    async def test_not_found(self) -> None:
        uc = ListPlaylistVideos(content=_YtPort(error=PlaylistNotFoundError("x")))
        out = json.loads(await run_youtube_playlist(uc, {"playlist": "PL0123456789ab"}))
        assert "not found" in out["error"]


class TestBothAgentsExposeTools:
    def test_tutor_registers_all_three(self) -> None:
        from cyberdyne_backend.application.ai_chat.tools import CYBERDYNE_TOOLS

        names = {t.name for t in CYBERDYNE_TOOLS}
        assert {"web_search", "youtube_transcript", "youtube_playlist"} <= names

    def test_answer_agent_registers_all_three(self) -> None:
        from cyberdyne_backend.application.agent_chat.tools import AGENT_TOOLS

        names = {t.name for t in AGENT_TOOLS}
        assert {"web_search", "youtube_transcript", "youtube_playlist"} <= names

    def test_schema_count(self) -> None:
        assert {t.name for t in EXTERNAL_SOURCE_TOOLS} == {
            "web_search",
            "youtube_transcript",
            "youtube_playlist",
        }


class TestTutorDispatchRouting:
    async def test_web_search_routes(self) -> None:
        from cyberdyne_backend.application.ai_chat.tools import ToolContext, ToolDispatcher
        from cyberdyne_backend.domain.ai_chat import ToolCall

        # Minimal ctx: only the fields the web_search branch touches.
        ctx = ToolContext(
            list_projects=None,  # type: ignore[arg-type]
            list_paths=None,  # type: ignore[arg-type]
            get_product=None,  # type: ignore[arg-type]
            learning_repo=None,  # type: ignore[arg-type]
            knowledge=None,  # type: ignore[arg-type]
            ask_repo=None,  # type: ignore[arg-type]
            captcha=None,  # type: ignore[arg-type]
            ask_notifier=None,  # type: ignore[arg-type]
            search_web=SearchWeb(provider=_SearchPort()),
        )
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="c", name="web_search", arguments_json='{"query": "hi"}')
        )
        assert json.loads(result)["answer"] == "the answer"

    async def test_youtube_transcript_routes(self) -> None:
        from cyberdyne_backend.application.ai_chat.tools import ToolContext, ToolDispatcher
        from cyberdyne_backend.domain.ai_chat import ToolCall

        ctx = ToolContext(
            list_projects=None,  # type: ignore[arg-type]
            list_paths=None,  # type: ignore[arg-type]
            get_product=None,  # type: ignore[arg-type]
            learning_repo=None,  # type: ignore[arg-type]
            knowledge=None,  # type: ignore[arg-type]
            ask_repo=None,  # type: ignore[arg-type]
            captcha=None,  # type: ignore[arg-type]
            ask_notifier=None,  # type: ignore[arg-type]
            youtube_transcript=GetVideoTranscript(content=_YtPort()),
        )
        result = await ToolDispatcher(ctx).dispatch(
            ToolCall(id="c", name="youtube_transcript", arguments_json='{"video": "abcdefghijk"}')
        )
        assert json.loads(result)["text"] == "hello world"


class TestAnswerAgentDispatchRouting:
    @staticmethod
    def _toolset(**kw: object):  # type: ignore[no-untyped-def]
        import uuid

        from cyberdyne_backend.application.agent_chat.tools import (
            LearnerContextDispatcher,
            LearnerContextToolset,
        )

        return LearnerContextDispatcher(
            LearnerContextToolset(
                user_id=uuid.uuid4(),
                list_my_progress=None,  # type: ignore[arg-type]
                get_my_learning_state=None,  # type: ignore[arg-type]
                recommend_courses=None,  # type: ignore[arg-type]
                list_user_notes=None,  # type: ignore[arg-type]
                **kw,  # type: ignore[arg-type]
            )
        )

    async def test_web_search_routes(self) -> None:
        from cyberdyne_backend.domain.ai_chat import ToolCall

        dispatcher = self._toolset(search_web=SearchWeb(provider=_SearchPort()))
        result = await dispatcher.dispatch(
            ToolCall(id="c", name="web_search", arguments_json='{"query": "hi"}')
        )
        assert json.loads(result)["answer"] == "the answer"

    async def test_youtube_playlist_routes(self) -> None:
        from cyberdyne_backend.domain.ai_chat import ToolCall

        dispatcher = self._toolset(youtube_playlist=ListPlaylistVideos(content=_YtPort()))
        result = await dispatcher.dispatch(
            ToolCall(
                id="c", name="youtube_playlist", arguments_json='{"playlist": "PL0123456789ab"}'
            )
        )
        assert json.loads(result)["title"] == "PL"


@pytest.mark.parametrize(
    "handler",
    [run_web_search, run_youtube_transcript, run_youtube_playlist],
)
async def test_handlers_report_unavailable_when_none(handler: object) -> None:
    out = json.loads(await handler(None, {}))  # type: ignore[operator]
    assert "error" in out
