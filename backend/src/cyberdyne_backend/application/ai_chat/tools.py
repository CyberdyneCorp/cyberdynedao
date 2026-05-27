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
import re
from dataclasses import dataclass
from decimal import Decimal
from typing import cast
from uuid import UUID

from cyberdyne_backend.application.blog.use_cases import (
    GetBlogPost,
    ListBlogPosts,
    ListBlogPostsQuery,
)
from cyberdyne_backend.application.content.use_cases import ListProjects
from cyberdyne_backend.application.dao_treasury.use_cases import GetDaoOverview
from cyberdyne_backend.application.learning import (
    EnrollInPath,
    GetMyLearningState,
    ListPaths,
    UpdateModuleProgress,
)
from cyberdyne_backend.application.marketplace import GetProduct
from cyberdyne_backend.domain.ai_chat import (
    KnowledgeSearchPort,
    MatlabDiagnostic,
    MatlabPort,
    ToolCall,
)
from cyberdyne_backend.domain.ai_chat.ports import ToolSchema
from cyberdyne_backend.domain.auth_identity import UserProfile
from cyberdyne_backend.domain.blog import BlogPostNotFoundError
from cyberdyne_backend.domain.leads import (
    AskChannel,
    AskRepository,
    CaptchaPort,
    EmailNotifierPort,
    new_ask,
)
from cyberdyne_backend.domain.learning import (
    LearningContentNotFoundError,
    LearningRepository,
    ProgressOutOfRangeError,
)
from cyberdyne_backend.domain.marketplace import ProductNotFoundError

logger = logging.getLogger("cyberdyne_backend.ai_chat.tools")

# Plotting verbs — if matlab_repl source draws, we route it through
# /v1/plot so a figure is actually captured (plain /v1/repl doesn't
# auto-save figures). Mirrors the frontend's looksLikePlot heuristic.
_PLOT_VERB = re.compile(
    r"(^|[\s;])(plot3?|figure|imshow|imagesc|surf|mesh|contourf?|histogram|barh?|"
    r"scatter3?|stem|stairs|loglog|semilog[xy]|polar(plot)?|pie|area|heatmap|"
    r"fplot|fsurf|fmesh|quiver3?|geoplot|geoscatter|plotmatrix|spy)\s*\(",
    re.IGNORECASE,
)


def looks_like_plot(source: str) -> bool:
    return bool(_PLOT_VERB.search(source))


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
            "Open a generic lead so a human follows up. Use this for vague 'please contact me' "
            "requests where the user hasn't shared concrete project details. "
            "Always confirm the email address with the user before calling. "
            "If the user has shared project specifics (scope, budget, timeline), prefer "
            "``capture_project_idea`` instead."
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
    ToolSchema(
        name="capture_project_idea",
        description=(
            "Structured lead capture for project ideas. Use this when the user has shared "
            "any of: project title, scope (one-time / ongoing), budget range, timeline, "
            "domain (geospatial / AI / web3 / dev-tooling / identity). Confirm the email "
            "back to the user in plain text BEFORE calling. The result lands as an Ask "
            "with channel ``chat_agent_handoff`` and the structured details in the body."
        ),
        parameters={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"},
                "project_title": {
                    "type": "string",
                    "description": "Short title — e.g. 'Geospatial risk dashboard for orchards'",
                },
                "description": {
                    "type": "string",
                    "description": "What the project is. Plain language, 1-3 sentences.",
                },
                "scope": {
                    "type": "string",
                    "enum": ["one_time", "ongoing", "unknown"],
                    "description": "One-time engagement vs. ongoing retainer.",
                },
                "budget_range": {
                    "type": "string",
                    "description": "User-stated budget — free-form, e.g. '$5k-15k' or 'tbd'",
                },
                "timeline": {
                    "type": "string",
                    "description": "Desired start / completion timing — free-form.",
                },
                "domain": {
                    "type": "string",
                    "enum": [
                        "geospatial",
                        "ai_knowledge_graphs",
                        "web3_defi",
                        "developer_tooling",
                        "identity",
                        "other",
                    ],
                },
            },
            "required": ["name", "email", "project_title", "description"],
        },
    ),
    ToolSchema(
        name="matlab_repl",
        description=(
            "Execute MATLAB source on the live MATLAB-LLVM engine and return stdout/stderr. "
            "The session is stateful across calls in this conversation — variables defined in "
            "one call persist to the next. Use for computation, defining variables, inspecting "
            "results. If the code draws a figure, prefer ``matlab_plot`` so the image is captured."
        ),
        parameters={
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "MATLAB source to run."},
            },
            "required": ["source"],
        },
    ),
    ToolSchema(
        name="matlab_plot",
        description=(
            "Run MATLAB source that produces a figure and capture it as a PNG so it renders "
            "inline in the chat. Use whenever the user wants to see a plot/chart/figure. Shares "
            "the same stateful session as ``matlab_repl`` (variables carry over). You don't need "
            "to call saveas — the engine captures the current figure automatically."
        ),
        parameters={
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": 'MATLAB plotting source, e.g. "x = linspace(0,2*pi,200); plot(x, sin(x))".',
                },
            },
            "required": ["source"],
        },
    ),
    ToolSchema(
        name="matlab_check",
        description=(
            "Lint / type-check MATLAB source without running it. Returns diagnostics "
            "(errors/warnings with line numbers). Use when the user asks what's wrong with "
            "some MATLAB code or to validate before running."
        ),
        parameters={
            "type": "object",
            "properties": {"source": {"type": "string"}},
            "required": ["source"],
        },
    ),
    ToolSchema(
        name="matlab_codegen",
        description=(
            "Compile MATLAB source to a target language (e.g. 'c' or 'hdl') and return the "
            "generated code. Use when the user wants C / HDL / Verilog generated from MATLAB. "
            "Present the returned code in a fenced code block tagged with the language."
        ),
        parameters={
            "type": "object",
            "properties": {
                "source": {"type": "string"},
                "target": {
                    "type": "string",
                    "description": "Codegen target, e.g. 'c' or 'hdl'. Defaults to 'c'.",
                },
            },
            "required": ["source"],
        },
    ),
    ToolSchema(
        name="get_dao_treasury",
        description=(
            "Fetch the Cyberdyne DAO treasury snapshot on Base: token balances, AAVE v3 "
            "supply/borrow positions and APYs, Uniswap v4 LP positions, total USD value, and "
            "holder count. Use for any question about the treasury, yields, or LP positions."
        ),
        parameters={"type": "object", "properties": {}, "required": []},
    ),
    ToolSchema(
        name="list_blog_posts",
        description="List recent published Cyberdyne blog posts. Optionally filter by category or tag.",
        parameters={
            "type": "object",
            "properties": {
                "category": {"type": "string"},
                "tag": {"type": "string"},
            },
            "required": [],
        },
    ),
    ToolSchema(
        name="lookup_blog_post",
        description="Fetch a single blog post by slug, including its full body, so you can summarize it.",
        parameters={
            "type": "object",
            "properties": {"slug": {"type": "string"}},
            "required": ["slug"],
        },
    ),
    ToolSchema(
        name="enroll_in_path",
        description=(
            "Enroll the SIGNED-IN user in a learning path (idempotent). Requires authentication. "
            "Use `list_paths` first to get the path slug."
        ),
        parameters={
            "type": "object",
            "properties": {"path_slug": {"type": "string"}},
            "required": ["path_slug"],
        },
    ),
    ToolSchema(
        name="get_my_learning",
        description=(
            "Get the signed-in user's learning state: enrolled paths, per-module progress, and "
            "earned certificates. Requires authentication."
        ),
        parameters={"type": "object", "properties": {}, "required": []},
    ),
    ToolSchema(
        name="set_module_progress",
        description=(
            "Set the signed-in user's progress on a module to an absolute percent (0-100). "
            "Pass 100 to mark a module complete. Requires authentication."
        ),
        parameters={
            "type": "object",
            "properties": {
                "module_slug": {"type": "string"},
                "percent": {"type": "integer", "minimum": 0, "maximum": 100},
            },
            "required": ["module_slug", "percent"],
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
    # The signed-in user (if any). Lead-capture tools fall back to this
    # email/handle when the LLM omits it, so an authenticated user never
    # has to re-type contact details we already hold.
    user: UserProfile | None = None
    # MATLAB-LLVM engine for the matlab_* tools, plus the user's bearer
    # (forwarded so figures land in their workspace).
    matlab: MatlabPort | None = None
    bearer: str | None = None
    # DAO treasury + blog (read-only); learning actions run as the
    # signed-in user (user_id from the profile).
    dao_overview: GetDaoOverview | None = None
    list_blog_posts: ListBlogPosts | None = None
    get_blog_post: GetBlogPost | None = None
    enroll_in_path: EnrollInPath | None = None
    get_my_learning: GetMyLearningState | None = None
    update_progress: UpdateModuleProgress | None = None
    user_id: UUID | None = None


class ToolDispatcher:
    """Runs a tool call to completion and returns a string the LLM can
    consume on its next turn. Every tool result is JSON-stringified so
    the LLM gets a stable surface."""

    def __init__(self, ctx: ToolContext) -> None:
        self._ctx = ctx

    async def dispatch(self, call: ToolCall, *, chat_session_id: str = "") -> str:
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
            if call.name == "capture_project_idea":
                return await self._capture_project_idea(args)
            if call.name == "matlab_repl":
                return await self._matlab_run(
                    cast(str, args.get("source", "")), chat_session_id, plot=False
                )
            if call.name == "matlab_plot":
                return await self._matlab_run(
                    cast(str, args.get("source", "")), chat_session_id, plot=True
                )
            if call.name == "matlab_check":
                return await self._matlab_check(cast(str, args.get("source", "")), chat_session_id)
            if call.name == "matlab_codegen":
                return await self._matlab_codegen(
                    cast(str, args.get("source", "")),
                    cast(str, args.get("target", "c") or "c"),
                    chat_session_id,
                )
            if call.name == "get_dao_treasury":
                return await self._get_dao_treasury()
            if call.name == "list_blog_posts":
                return await self._list_blog_posts(
                    cast("str | None", args.get("category")), cast("str | None", args.get("tag"))
                )
            if call.name == "lookup_blog_post":
                return await self._lookup_blog_post(cast(str, args.get("slug", "")))
            if call.name == "enroll_in_path":
                return await self._enroll_in_path(cast(str, args.get("path_slug", "")))
            if call.name == "get_my_learning":
                return await self._get_my_learning()
            if call.name == "set_module_progress":
                return await self._set_module_progress(
                    cast(str, args.get("module_slug", "")), args.get("percent")
                )
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

    async def _matlab_run(self, source: str, chat_session_id: str, *, plot: bool) -> str:
        if not source.strip():
            return json.dumps({"error": "empty_source"})
        if self._ctx.matlab is None:
            return json.dumps({"error": "matlab_unavailable"})
        # One stable workspace per conversation so variables persist
        # across tool calls in the same chat.
        session_id = f"agent-{chat_session_id}" if chat_session_id else "agent-default"
        # Route through /v1/plot when the agent explicitly plots, OR when
        # it used matlab_repl on drawing code — /v1/repl alone doesn't
        # capture a figure, so the user would get "no plot". This way a
        # figure is captured regardless of which tool the model picked.
        use_plot = plot or looks_like_plot(source)
        if use_plot:
            res = await self._ctx.matlab.run_plot(
                source=source, session_id=session_id, bearer=self._ctx.bearer
            )
        else:
            res = await self._ctx.matlab.run_repl(
                source=source, session_id=session_id, bearer=self._ctx.bearer
            )
        # Reference the figure by artifact path + session id only — the
        # frontend downloads it through the authed proxy. Inlining the
        # PNG would feed it back into the next LLM round (big prompt,
        # transport errors). ``has_figure`` is the only signal the LLM
        # needs to know a plot was produced.
        image_exts = (".png", ".jpg", ".jpeg", ".svg")
        figures = [a for a in res.artifacts if a.lower().endswith(image_exts)]
        return json.dumps(
            {
                "ok": res.ok,
                "stdout": res.stdout,
                "stderr": res.stderr,
                "timed_out": res.timed_out,
                "artifacts": list(res.artifacts),
                "figures": figures,
                "session_id": res.session_id,
                "has_figure": len(figures) > 0,
            }
        )

    def _matlab_session(self, chat_session_id: str) -> str:
        return f"agent-{chat_session_id}" if chat_session_id else "agent-default"

    @staticmethod
    def _diag_dicts(diagnostics: tuple[MatlabDiagnostic, ...]) -> list[dict[str, object]]:
        return [
            {"severity": d.severity, "message": d.message, "line": d.line, "col": d.col}
            for d in diagnostics
        ]

    async def _matlab_check(self, source: str, chat_session_id: str) -> str:
        if not source.strip():
            return json.dumps({"error": "empty_source"})
        if self._ctx.matlab is None:
            return json.dumps({"error": "matlab_unavailable"})
        res = await self._ctx.matlab.check(
            source=source, session_id=self._matlab_session(chat_session_id), bearer=self._ctx.bearer
        )
        return json.dumps(
            {
                "ok": res.ok,
                "diagnostics": self._diag_dicts(res.diagnostics),
                "stdout": res.stdout,
                "stderr": res.stderr,
            }
        )

    async def _matlab_codegen(self, source: str, target: str, chat_session_id: str) -> str:
        if not source.strip():
            return json.dumps({"error": "empty_source"})
        if self._ctx.matlab is None:
            return json.dumps({"error": "matlab_unavailable"})
        res = await self._ctx.matlab.codegen(
            source=source,
            target=target,
            session_id=self._matlab_session(chat_session_id),
            bearer=self._ctx.bearer,
        )
        return json.dumps(
            {
                "ok": res.ok,
                "language": res.language,
                "code": res.code,
                "diagnostics": self._diag_dicts(res.diagnostics),
                "stderr": res.stderr,
            }
        )

    async def _get_dao_treasury(self) -> str:
        if self._ctx.dao_overview is None:
            return json.dumps({"error": "dao_unavailable"})
        overview = await self._ctx.dao_overview.execute()
        snap = overview.snapshot

        def f(x: object) -> float:
            return float(cast(Decimal, x))

        return json.dumps(
            {
                "treasury_address": snap.treasury_address,
                "chain_id": snap.chain_id,
                "total_usd_value": f(snap.total_usd_value),
                "holders": overview.holders,
                "token_balances": [
                    {
                        "symbol": b.symbol,
                        "balance": f(b.balance),
                        "usd_value": f(b.usd_value),
                        "change_24h_pct": f(b.change_24h_pct),
                    }
                    for b in snap.token_balances
                ],
                "aave_positions": [
                    {
                        "symbol": p.symbol,
                        "supply_apy": f(p.supply_apy),
                        "borrow_apy": f(p.borrow_apy),
                        "usd_value_supplied": f(p.usd_value_supplied),
                        "usd_value_borrowed": f(p.usd_value_borrowed),
                    }
                    for p in snap.aave_positions
                ],
                "uniswap_positions": [
                    {
                        "pair": f"{p.token0_symbol}/{p.token1_symbol}",
                        "fee_tier_bps": p.fee_tier_bps,
                        "in_range": p.in_range,
                        "usd_value": f(p.usd_value),
                        "uncollected_fees_usd": f(p.uncollected_fees_usd),
                    }
                    for p in snap.uniswap_positions
                ],
            }
        )

    async def _list_blog_posts(self, category: str | None, tag: str | None) -> str:
        if self._ctx.list_blog_posts is None:
            return json.dumps({"error": "blog_unavailable"})
        posts, total = await self._ctx.list_blog_posts.execute(
            ListBlogPostsQuery(category=category, tag=tag, page=1, page_size=10)
        )
        return json.dumps(
            {
                "total": total,
                "posts": [
                    {
                        "slug": p.slug,
                        "title": p.title,
                        "excerpt": p.excerpt,
                        "category": p.category_slug,
                        "tags": list(p.tags),
                        "published_at": p.published_at.isoformat() if p.published_at else None,
                    }
                    for p in posts
                ],
            }
        )

    async def _lookup_blog_post(self, slug: str) -> str:
        if self._ctx.get_blog_post is None:
            return json.dumps({"error": "blog_unavailable"})
        try:
            p = await self._ctx.get_blog_post.execute(slug)
        except BlogPostNotFoundError:
            return json.dumps({"error": "not_found", "slug": slug})
        return json.dumps(
            {
                "slug": p.slug,
                "title": p.title,
                "body_md": p.body_md,
                "category": p.category_slug,
                "tags": list(p.tags),
                "published_at": p.published_at.isoformat() if p.published_at else None,
            }
        )

    async def _enroll_in_path(self, path_slug: str) -> str:
        if self._ctx.enroll_in_path is None:
            return json.dumps({"error": "learning_unavailable"})
        if self._ctx.user_id is None:
            return json.dumps({"error": "sign_in_required"})
        if not path_slug.strip():
            return json.dumps({"error": "missing_path_slug"})
        try:
            enr = await self._ctx.enroll_in_path.execute(
                user_id=self._ctx.user_id, path_slug=path_slug
            )
        except LearningContentNotFoundError:
            return json.dumps({"error": "not_found", "path_slug": path_slug})
        return json.dumps({"ok": True, "path_slug": enr.path_slug, "status": enr.status.value})

    async def _get_my_learning(self) -> str:
        if self._ctx.get_my_learning is None:
            return json.dumps({"error": "learning_unavailable"})
        if self._ctx.user_id is None:
            return json.dumps({"error": "sign_in_required"})
        state = await self._ctx.get_my_learning.execute(self._ctx.user_id)
        return json.dumps(
            {
                "enrollments": [
                    {"path_slug": e.path_slug, "status": e.status.value} for e in state.enrollments
                ],
                "progress": [
                    {"module_slug": p.module_slug, "percent": p.percent}
                    for p in state.progress_by_module.values()
                ],
                "certificates": [
                    {"path_slug": c.path_slug, "verification_hash": c.verification_hash}
                    for c in state.certificates
                ],
            }
        )

    async def _set_module_progress(self, module_slug: str, percent: object) -> str:
        if self._ctx.update_progress is None:
            return json.dumps({"error": "learning_unavailable"})
        if self._ctx.user_id is None:
            return json.dumps({"error": "sign_in_required"})
        if not module_slug.strip():
            return json.dumps({"error": "missing_module_slug"})
        if not isinstance(percent, int):
            return json.dumps({"error": "percent_must_be_int"})
        try:
            prog = await self._ctx.update_progress.execute(
                user_id=self._ctx.user_id, module_slug=module_slug, percent=percent
            )
        except ProgressOutOfRangeError:
            return json.dumps({"error": "percent_out_of_range"})
        return json.dumps({"ok": True, "module_slug": prog.module_slug, "percent": prog.percent})

    def _fill_identity(self, name: str, email: str) -> tuple[str, str]:
        """Back-fill name/email from the signed-in profile when the LLM
        left them blank, so an authenticated user isn't asked for what
        we already have."""
        user = self._ctx.user
        if not email and user and user.email:
            email = user.email
        if not name and user:
            name = user.display_name or (user.email or "")
        return name.strip(), email.strip()

    async def _create_ask(self, args: dict[str, object]) -> str:
        name, email = self._fill_identity(
            cast(str, args.get("name", "")), cast(str, args.get("email", ""))
        )
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

    async def _capture_project_idea(self, args: dict[str, object]) -> str:
        """Structured lead capture. Bundles the structured fields into a
        deterministic markdown-ish body so the admin /asks list view
        renders it sensibly without a new column schema."""
        name, email = self._fill_identity(
            cast(str, args.get("name", "")), cast(str, args.get("email", ""))
        )
        title = cast(str, args.get("project_title", "")).strip()
        description = cast(str, args.get("description", "")).strip()
        if not (name and email and title and description):
            return json.dumps({"error": "missing_required_fields"})
        scope = cast(str, args.get("scope", "unknown") or "unknown")
        budget = cast(str, args.get("budget_range", "") or "").strip()
        timeline = cast(str, args.get("timeline", "") or "").strip()
        domain = cast(str, args.get("domain", "") or "").strip()
        # Compact, copy-paste-friendly body for the admin view.
        lines = [
            f"# {title}",
            "",
            description,
            "",
            f"- **Scope:** {scope}",
        ]
        if budget:
            lines.append(f"- **Budget:** {budget}")
        if timeline:
            lines.append(f"- **Timeline:** {timeline}")
        if domain:
            lines.append(f"- **Domain:** {domain}")
        body = "\n".join(lines)
        ask = new_ask(
            channel=AskChannel.CHAT_AGENT_HANDOFF,
            name=name,
            email=email,
            body=body,
            product_slug=None,
            source_url=None,
        )
        await self._ctx.ask_repo.save(ask)
        await self._ctx.ask_notifier.send_new_ask_notification(ask)
        return json.dumps(
            {
                "ok": True,
                "ask_id": str(ask.id),
                "captured": {
                    "project_title": title,
                    "scope": scope,
                    "budget_range": budget or None,
                    "timeline": timeline or None,
                    "domain": domain or None,
                },
            }
        )
