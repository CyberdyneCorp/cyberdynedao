"""Tool surface available to the chat agent.

Tools are pure data (``ToolSchema``) on the way out to the LLM, and
dispatched in-process here when the LLM calls them back. The
dispatcher resolves each tool through the existing application
use cases — no shadow data path.

Tools defined in v1:
- ``list_projects`` — Cyberdyne's projects (from the content context).
- ``lookup_module`` — a single learning module by slug.
- ``list_paths`` — learning paths.
- ``lookup_product`` — marketplace product by slug.
- ``search_cyberdyne_knowledge`` — CyberRAG semantic search (stub in v1).
- ``create_ask_for_handoff`` — opens a lead (Ask) so a human follows up.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import cast

from cyberdyne_backend.application.content.use_cases import ListProjects
from cyberdyne_backend.application.learning import ListPaths
from cyberdyne_backend.application.marketplace import GetProduct
from cyberdyne_backend.domain.ai_chat import KnowledgeSearchPort, ToolCall
from cyberdyne_backend.domain.ai_chat.ports import ToolSchema
from cyberdyne_backend.domain.leads import (
    AskChannel,
    AskRepository,
    CaptchaPort,
    EmailNotifierPort,
    new_ask,
)
from cyberdyne_backend.domain.learning import LearningContentNotFoundError, LearningRepository
from cyberdyne_backend.domain.marketplace import ProductNotFoundError

logger = logging.getLogger("cyberdyne_backend.ai_chat.tools")


CYBERDYNE_TOOLS: list[ToolSchema] = [
    ToolSchema(
        name="list_projects",
        description="List Cyberdyne's projects and products. Use this to answer questions about what Cyberdyne builds.",
        parameters={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    ToolSchema(
        name="lookup_module",
        description="Look up a single learning module by its slug. Useful when the user asks about a specific course.",
        parameters={
            "type": "object",
            "properties": {
                "slug": {"type": "string", "description": "Module slug, e.g. 'mcp-servers'"},
            },
            "required": ["slug"],
        },
    ),
    ToolSchema(
        name="list_paths",
        description="List the learning paths Cyberdyne Academy offers. Use this to answer 'what training do you offer?'.",
        parameters={"type": "object", "properties": {}, "required": []},
    ),
    ToolSchema(
        name="lookup_product",
        description="Look up a single marketplace product (service, training, or license) by slug.",
        parameters={
            "type": "object",
            "properties": {
                "slug": {"type": "string"},
            },
            "required": ["slug"],
        },
    ),
    ToolSchema(
        name="search_cyberdyne_knowledge",
        description=(
            "Semantic search across Cyberdyne's documentation, blog, and project descriptions. "
            "Use when the user asks something open-ended that isn't a slug-keyed lookup."
        ),
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
            },
            "required": ["query"],
        },
    ),
    ToolSchema(
        name="create_ask_for_handoff",
        description=(
            "Open a lead so a human follows up. Only call this when the user has explicitly "
            "asked to be contacted. Always confirm the email address with the user before calling."
        ),
        parameters={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"},
                "body": {"type": "string"},
                "product_slug": {"type": "string"},
            },
            "required": ["name", "email", "body"],
        },
    ),
]


@dataclass(slots=True)
class ToolContext:
    """All the use cases / repos a tool might need. The dispatcher
    only reads from them — it never holds state."""

    list_projects: ListProjects
    list_paths: ListPaths
    get_product: GetProduct
    learning_repo: LearningRepository
    knowledge: KnowledgeSearchPort
    ask_repo: AskRepository
    captcha: CaptchaPort
    ask_notifier: EmailNotifierPort


class ToolDispatcher:
    """Runs a tool call to completion and returns a string the LLM can
    consume on its next turn. Every tool result is JSON-stringified so
    the LLM gets a stable surface."""

    def __init__(self, ctx: ToolContext) -> None:
        self._ctx = ctx

    async def dispatch(self, call: ToolCall) -> str:
        try:
            args = cast(dict[str, object], json.loads(call.arguments_json or "{}"))
        except json.JSONDecodeError:
            return json.dumps({"error": "invalid_arguments_json"})
        try:
            if call.name == "list_projects":
                return await self._list_projects()
            if call.name == "lookup_module":
                return await self._lookup_module(cast(str, args.get("slug", "")))
            if call.name == "list_paths":
                return await self._list_paths()
            if call.name == "lookup_product":
                return await self._lookup_product(cast(str, args.get("slug", "")))
            if call.name == "search_cyberdyne_knowledge":
                return await self._search(cast(str, args.get("query", "")))
            if call.name == "create_ask_for_handoff":
                return await self._create_ask(args)
        except Exception as exc:
            logger.exception("tool %s failed", call.name)
            return json.dumps({"error": "tool_failed", "detail": str(exc)})
        return json.dumps({"error": "unknown_tool", "tool": call.name})

    async def _list_projects(self) -> str:
        projects = await self._ctx.list_projects.execute()
        return json.dumps(
            [
                {
                    "id": p.id,
                    "name": p.name,
                    "description": p.description,
                    "status": p.status,
                }
                for p in projects
            ]
        )

    async def _lookup_module(self, slug: str) -> str:
        modules = await self._ctx.learning_repo.list_modules()
        for m in modules:
            if m.slug == slug:
                return json.dumps(
                    {
                        "slug": m.slug,
                        "title": m.title,
                        "category": m.category,
                        "level": m.level,
                        "duration": m.duration,
                        "description": m.description,
                        "topics": list(m.topics),
                    }
                )
        return json.dumps({"error": "not_found", "slug": slug})

    async def _list_paths(self) -> str:
        try:
            paths = await self._ctx.list_paths.execute()
        except LearningContentNotFoundError:
            return json.dumps([])
        return json.dumps(
            [
                {
                    "slug": p.slug,
                    "title": p.title,
                    "description": p.description,
                    "estimated_time": p.estimated_time,
                    "module_slugs": list(p.module_slugs),
                }
                for p in paths
            ]
        )

    async def _lookup_product(self, slug: str) -> str:
        try:
            product = await self._ctx.get_product.execute(slug)
        except ProductNotFoundError:
            return json.dumps({"error": "not_found", "slug": slug})
        return json.dumps(
            {
                "slug": product.slug,
                "type": product.type.value,
                "title": product.title,
                "price_cents": product.price_cents,
                "currency": product.currency,
                "duration_label": product.duration_label,
                "features": list(product.features),
                "is_purchasable": product.is_purchasable,
            }
        )

    async def _search(self, query: str) -> str:
        if not query.strip():
            return json.dumps({"error": "empty_query"})
        result = await self._ctx.knowledge.search(query)
        return json.dumps({"summary": result})

    async def _create_ask(self, args: dict[str, object]) -> str:
        name = cast(str, args.get("name", "")).strip()
        email = cast(str, args.get("email", "")).strip()
        body = cast(str, args.get("body", "")).strip()
        product_slug = cast(str | None, args.get("product_slug"))
        if not (name and email and body):
            return json.dumps({"error": "missing_required_fields"})
        # Chat handoffs bypass captcha — we trust the LLM only as far as
        # rate-limited inference, but they're entering through a
        # different surface than the contact form.
        ask = new_ask(
            channel=AskChannel.CHAT_AGENT_HANDOFF,
            name=name,
            email=email,
            body=body,
            product_slug=product_slug,
            source_url=None,
        )
        await self._ctx.ask_repo.save(ask)
        await self._ctx.ask_notifier.send_new_ask_notification(ask)
        return json.dumps({"ok": True, "ask_id": str(ask.id)})
