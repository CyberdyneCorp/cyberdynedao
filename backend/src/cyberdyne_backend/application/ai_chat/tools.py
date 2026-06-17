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
from uuid import UUID, uuid4

from cyberdyne_backend.application.access import GetWalletAccess
from cyberdyne_backend.application.analytics import GetLearnerDashboard
from cyberdyne_backend.application.blog.use_cases import (
    GetBlogPost,
    ListBlogPosts,
    ListBlogPostsQuery,
)
from cyberdyne_backend.application.content.use_cases import ListProjects
from cyberdyne_backend.application.courses import GetCourse, GetMyCourseProgress, ListCourses
from cyberdyne_backend.application.dao_treasury.use_cases import GetDaoOverview
from cyberdyne_backend.application.learning import (
    EnrollInPath,
    GetMyDeadlines,
    GetMyLearningState,
    GetPathGating,
    ListPaths,
    UpdateModuleProgress,
)
from cyberdyne_backend.application.lesson_notes import ListUserNotes
from cyberdyne_backend.application.marketplace import GetProduct
from cyberdyne_backend.application.notebook import ListFlashcards, ListNotes
from cyberdyne_backend.application.quizzes import GetQuiz
from cyberdyne_backend.domain.access import InvalidWalletAddressError
from cyberdyne_backend.domain.ai_chat import (
    CyberfliesPort,
    DocumentRendererPort,
    KnowledgeSearchPort,
    MatlabDiagnostic,
    MatlabPort,
    PythonInterpreterPort,
    ToolCall,
)
from cyberdyne_backend.domain.ai_chat.ports import ToolSchema
from cyberdyne_backend.domain.auth_identity import UserProfile
from cyberdyne_backend.domain.blog import BlogPostNotFoundError
from cyberdyne_backend.domain.courses import (
    CourseLevel,
    CourseNotFoundError,
    InvalidCourseLevelError,
    parse_level,
)
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
from cyberdyne_backend.domain.notebook import Note, NoteType
from cyberdyne_backend.domain.quizzes import QuizNotFoundError

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


# matplotlib in the headless sandbox uses the Agg backend, so ``plt.show()``
# saves nothing — only ``plt.savefig`` produces a file the frontend can
# render. Rather than rely on the LLM to remember savefig, we auto-capture
# any open figures for plotting code (mirrors how ``matlab_plot`` captures a
# figure without the model writing ``saveas``).
_MATPLOTLIB_HINT = re.compile(
    r"\b(?:matplotlib|pyplot|pylab|seaborn)\b|\bplt\b|\bsns\b|\.plot\s*\(",
    re.IGNORECASE,
)

# Appended to plotting code before execution. Names are NOT underscore-prefixed
# because RestrictedPython rejects leading-underscore identifiers; ``cyb_`` keeps
# collision risk with user code low. ``{tag}`` is a per-call unique tag
# (dispatcher token + call seq) so figures never overwrite each other — within a
# turn OR across turns when the session is reused. The whole block is wrapped in
# try/except so it can never break the user's run.
_AUTO_CAPTURE_TEMPLATE = """

# --- auto-capture open matplotlib figures so they render inline ---
try:
    import matplotlib.pyplot as cyb_plt
    cyb_fignums = cyb_plt.get_fignums()
    for cyb_idx in range(len(cyb_fignums)):
        cyb_plt.figure(cyb_fignums[cyb_idx]).savefig("figure_{tag}_%d.png" % (cyb_idx + 1))
    cyb_plt.close("all")
except Exception:
    pass
"""


def wants_figure_capture(code: str) -> bool:
    """True when ``code`` looks like matplotlib plotting and doesn't already
    save figures itself. ``savefig`` present → trust the user's own save and
    skip auto-capture (avoids duplicate figures)."""
    if "savefig" in code:
        return False
    return bool(_MATPLOTLIB_HINT.search(code))


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
        name="python_exec",
        description=(
            "Execute Python source on the live interpreter sandbox and return stdout/stderr. "
            "Each call is an isolated execution: FILES written to the workspace persist and are "
            "visible to later calls, but VARIABLES, imports and definitions do NOT carry over — "
            "redefine what you need in every call, or persist intermediate state to a file and "
            "re-read it. Use for computation, data analysis, generating and running plots "
            "(matplotlib etc.), or any general Python the user asks for. Always show the Python "
            "source you ran in a fenced ```python block in your reply. Matplotlib figures are "
            "captured automatically and render inline — you do NOT need to call plt.savefig, and "
            "plt.show() alone is fine."
        ),
        parameters={
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Python source to run."},
            },
            "required": ["code"],
        },
    ),
    ToolSchema(
        name="render_manim",
        description=(
            "Render a mathematical animation with Manim (Community Edition) and show it "
            "inline in the chat. Use this WHENEVER the user asks you to explain, visualize, "
            "animate, or demonstrate a concept visually — math, physics, algorithms, "
            "geometry, data structures, transformations. Write a complete Manim `Scene` "
            "subclass in `code` (it MUST start with `from manim import *` and define one "
            "`class <Name>(Scene): def construct(self): ...`), and pass that class name as "
            "`scene`. Build the animation from `self.play(...)` calls (Create, Write, "
            "Transform, FadeIn, FadeOut, .animate, etc.). Keep scenes short and focused "
            "(a handful of plays) so they render quickly. The animation renders as a "
            "looping GIF that displays automatically below your message — do NOT embed a "
            "markdown image, a path, or a filename. ALWAYS also show the Manim source you "
            "wrote in a fenced ```python block, then describe what the animation shows in "
            "one or two sentences. Shares the same workspace as python_exec (rendered files "
            "persist between them), but like python_exec each call is an isolated execution — "
            "Python variables do not carry over.\n"
            "AUTHORING RULES (follow exactly — most render failures come from breaking "
            "these):\n"
            '• Use Text("...") for ALL words, labels, titles and sentences. Use '
            'MathTex(...) ONLY for real mathematical formulas (e.g. MathTex(r"F = ma")). '
            "NEVER put prose/sentences inside MathTex.\n"
            "• Inside MathTex never use \\text{}, \\textbf{}, \\textquotesingle, or \\\\ line "
            "breaks — those are the #1 cause of LaTeX render failures here. Keep formulas "
            "short.\n"
            '• ALWAYS write LaTeX as a raw string: MathTex(r"\\frac{1}{2} m v^2") — a plain '
            '"\\frac" string corrupts the LaTeX (\\f, \\t etc. become control chars).\n'
            "• Use Manim Community names: Create, Write, FadeIn, FadeOut, Transform, "
            "GrowArrow, and obj.animate.<method>() for moves/scales. Position with "
            ".shift(), .next_to(), .to_edge().\n"
            "• This is Manim Community Edition, NOT 3b1b/ManimGL — the APIs differ. "
            "Shade under a curve with axes.get_area(graph, x_range=[a, b], color=..., "
            "opacity=...); there is NO x_min/x_max kwarg (that's the old API and "
            "raises TypeError). Plot with axes.plot(func, x_range=[a, b]). `np` is "
            "available without importing numpy.\n"
            "• Keep it to ~6-8 self.play calls. If a render comes back failed, read the "
            "returned stdout/stderr (the Python traceback names the exact error), fix "
            "that line — or replace any MathTex prose with Text — and retry once."
        ),
        parameters={
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": (
                        "Full Manim scene source: `from manim import *` then a single "
                        "`class <Name>(Scene)` with a `construct(self)` method."
                    ),
                },
                "scene": {
                    "type": "string",
                    "description": "The Scene subclass name to render, e.g. 'PythagoreanProof'.",
                },
                "quality": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": (
                        "Render quality. Default 'low' (fast and reliable for chat); pass "
                        "'medium'/'high' only when the user wants a more polished clip."
                    ),
                },
            },
            "required": ["code", "scene"],
        },
    ),
    ToolSchema(
        name="ask_meetings",
        description=(
            "Answer a question about the signed-in user's recorded meetings (Cyberflies). "
            "Use for anything about what was said, decided, or discussed in their meetings — "
            "summaries, action items, 'what did we decide about X'. It searches the user's "
            "transcripts and returns an answer."
        ),
        parameters={
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The user's question about their meetings.",
                },
            },
            "required": ["question"],
        },
    ),
    ToolSchema(
        name="list_meetings",
        description=(
            "List the user's recent recorded meetings (id, headline, status, date). Use to "
            "enumerate meetings or before asking about a specific one."
        ),
        parameters={"type": "object", "properties": {}},
    ),
    ToolSchema(
        name="get_meeting",
        description=(
            "Fetch ONE meeting in full: its AI summary (headline, abstract, key points) AND "
            "the transcript text. Use this when the user wants to work WITH a specific meeting "
            "— summarize it, pull out action items / decisions, or draft a follow-up email — "
            "because you get the actual content to ground your answer. Get the meeting id from "
            "`list_meetings` first. For a cross-meeting or fuzzy question, prefer `ask_meetings`. "
            "To make the result downloadable, pass your summary to `create_document`; to hand "
            "action items to a human, use a lead tool."
        ),
        parameters={
            "type": "object",
            "properties": {
                "meeting_id": {
                    "type": "string",
                    "description": "Recording/meeting id from list_meetings.",
                }
            },
            "required": ["meeting_id"],
        },
    ),
    ToolSchema(
        name="create_document",
        description=(
            "Create a downloadable document for the user and return its filename. Use whenever "
            "the user asks to export, save, or download something (a summary, report, notes, "
            "diagram, mind map). Put the FULL document in `content`. Formats: 'markdown' (.md), "
            "'mermaid' (a Mermaid diagram definition, .mmd), 'xmind' (markdown headings/bullets "
            "for XMind import, .md), 'pdf' (rendered from markdown). After calling, tell the "
            "user the file is ready to download — do NOT paste the whole content again."
        ),
        parameters={
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Desired filename, e.g. 'meeting-summary'. Extension optional.",
                },
                "content": {
                    "type": "string",
                    "description": "Full document content (markdown, or a Mermaid definition).",
                },
                "format": {
                    "type": "string",
                    "enum": ["markdown", "mermaid", "xmind", "pdf"],
                },
            },
            "required": ["filename", "content", "format"],
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
    ToolSchema(
        name="list_courses",
        description=(
            "List the published courses in Cyberdyne Academy (title, level, lesson count). "
            "Use to answer 'what courses are there?' or to recommend a course."
        ),
        parameters={
            "type": "object",
            "properties": {
                "level": {
                    "type": "string",
                    "enum": ["Beginner", "Intermediate", "Advanced"],
                    "description": "Optional level filter.",
                }
            },
            "required": [],
        },
    ),
    ToolSchema(
        name="get_course",
        description=(
            "Get a single published course by slug with its ordered lessons (title + type). "
            "Use to discuss a course's contents or guide a learner through it. Lesson types "
            "include quiz lessons — use ``get_lesson_quiz`` for the questions."
        ),
        parameters={
            "type": "object",
            "properties": {"slug": {"type": "string"}},
            "required": ["slug"],
        },
    ),
    ToolSchema(
        name="get_my_deadlines",
        description=(
            "Get the signed-in user's enrollment deadlines with status "
            "(overdue / urgent / upcoming / none) and days remaining. Use to nudge the learner "
            "about what's due. Requires authentication."
        ),
        parameters={"type": "object", "properties": {}, "required": []},
    ),
    ToolSchema(
        name="get_path_gating",
        description=(
            "For the signed-in user, get per-module lock state in a learning path: which modules "
            "are unlocked vs locked, and why (level / sequential prerequisites). Use to explain "
            "what to do next or why something is locked. Requires authentication."
        ),
        parameters={
            "type": "object",
            "properties": {"path_slug": {"type": "string"}},
            "required": ["path_slug"],
        },
    ),
    ToolSchema(
        name="get_lesson_quiz",
        description=(
            "Get the quiz attached to a lesson, as the learner sees it BEFORE submitting: "
            "questions and option texts only. It deliberately does NOT include which option is "
            "correct or the explanations — so you can help a learner think through the questions "
            "without giving away answers. Get the lesson id from ``get_course``."
        ),
        parameters={
            "type": "object",
            "properties": {
                "lesson_id": {"type": "string", "description": "Lesson UUID from get_course."}
            },
            "required": ["lesson_id"],
        },
    ),
    ToolSchema(
        name="get_my_dashboard",
        description=(
            "Get the signed-in learner's analytics dashboard: enrolled / completed / active "
            "paths, completed + in-progress modules, completed + in-progress courses, average "
            "module percent, quizzes attempted/passed + pass rate + average score, and "
            "certificate count. Use to give a narrative progress summary or decide what to "
            "recommend next. Requires authentication."
        ),
        parameters={"type": "object", "properties": {}, "required": []},
    ),
    ToolSchema(
        name="get_my_course_progress",
        description=(
            "Get the signed-in learner's progress through a single course: per-lesson "
            "completion, completed-lesson count, overall percent, and whether the course is "
            "finished. Use when the learner asks how they're doing in a specific course. Get "
            "the course slug from ``get_course`` / ``list_courses``. Requires authentication."
        ),
        parameters={
            "type": "object",
            "properties": {
                "slug": {"type": "string", "description": "Course slug from get_course."}
            },
            "required": ["slug"],
        },
    ),
    ToolSchema(
        name="get_my_courses",
        description=(
            "The signed-in learner's progress across ALL published Cyberdyne Academy "
            "courses: each course's title, level, percent complete, and whether it's "
            "finished. This is the canonical answer to 'what am I studying?', 'what's my "
            "progress?', or 'which courses have I started?'. Prefer this over the legacy "
            "learning-paths tools. Requires authentication."
        ),
        parameters={"type": "object", "properties": {}},
    ),
    ToolSchema(
        name="get_my_notes",
        description=(
            "The signed-in learner's own course notes — the notes they wrote on course "
            "lessons. Each note has its course slug, lesson id, the note body, and any "
            "highlighted quote. Use this for 'what notes did I take?', 'show my notes', or "
            "'what did I write on <course>?'. Pass course_slug to filter to one course. "
            "Requires authentication."
        ),
        parameters={
            "type": "object",
            "properties": {
                "course_slug": {
                    "type": "string",
                    "description": "Optional: only return notes for this course slug.",
                }
            },
        },
    ),
    ToolSchema(
        name="get_my_notebook",
        description=(
            "The signed-in learner's Notebook — their standalone study notes (markdown "
            "title + body, a type, optional course/lesson link, and any saved-from-the-Lab "
            "code) together with the flashcards on each note. Use this for 'what's in my "
            "notebook?', 'show my flashcards', 'search my notes for X', or 'quiz me on "
            "what's due'. Optional filters: query (free-text search), due (only notes/cards "
            "due for spaced review), type (one of lesson/lab/code/simulation/theory/"
            "problem). Distinct from get_my_notes, which is the notes pinned to course "
            "lessons. Requires authentication."
        ),
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Optional free-text search."},
                "due": {
                    "type": "boolean",
                    "description": "Optional: only notes due for spaced review.",
                },
                "type": {
                    "type": "string",
                    "enum": ["lesson", "lab", "code", "simulation", "theory", "problem"],
                    "description": "Optional: filter by note type.",
                },
            },
        },
    ),
    ToolSchema(
        name="get_user_tier",
        description=(
            "The signed-in user's CyberdyneAccessNFT access tier — whether they hold an "
            "access NFT and which capabilities it grants (learning, frontend, backend, "
            "blog creator, admin, marketplace selling). Use this when the user asks what "
            "access / tier / permissions / NFT perks they have. Reads the wallet linked to "
            "their account; if no wallet is linked it returns no_wallet_linked — tell them "
            "to connect their wallet. Requires authentication."
        ),
        parameters={"type": "object", "properties": {}},
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
    # Python interpreter sandbox for the python_exec tool (same bearer
    # forwarding so files land in the user's workspace).
    python: PythonInterpreterPort | None = None
    # Cyberflies (meetings) backend for ask_meetings / list_meetings.
    cyberflies: CyberfliesPort | None = None
    # Renders document bytes (e.g. markdown → PDF) for create_document.
    documents: DocumentRendererPort | None = None
    bearer: str | None = None
    # DAO treasury + blog (read-only); learning actions run as the
    # signed-in user (user_id from the profile).
    dao_overview: GetDaoOverview | None = None
    list_blog_posts: ListBlogPosts | None = None
    get_blog_post: GetBlogPost | None = None
    enroll_in_path: EnrollInPath | None = None
    get_my_learning: GetMyLearningState | None = None
    update_progress: UpdateModuleProgress | None = None
    # New learning surface (courses + gating + deadlines) so the agent
    # can act as a learning companion / recommender.
    list_courses: ListCourses | None = None
    get_course: GetCourse | None = None
    get_my_course_progress: GetMyCourseProgress | None = None
    get_my_deadlines: GetMyDeadlines | None = None
    path_gating: GetPathGating | None = None
    get_quiz: GetQuiz | None = None
    learner_dashboard: GetLearnerDashboard | None = None
    # The learner's own course/lesson notes (read-only) for get_my_notes.
    list_user_notes: ListUserNotes | None = None
    # The learner's notebook (standalone notes + flashcards) for
    # get_my_notebook — both read-only.
    list_notebook_notes: ListNotes | None = None
    list_note_flashcards: ListFlashcards | None = None
    # Access-tier lookup for get_user_tier (reads the user's linked wallet).
    get_wallet_access: GetWalletAccess | None = None
    user_id: UUID | None = None


class ToolDispatcher:
    """Runs a tool call to completion and returns a string the LLM can
    consume on its next turn. Every tool result is JSON-stringified so
    the LLM gets a stable surface."""

    def __init__(self, ctx: ToolContext) -> None:
        self._ctx = ctx
        # Interpreter session for python_exec. Normally lazily created and
        # reused across calls within a single turn so variables/files persist.
        # It can also be pre-seeded via ``use_python_session`` when the user
        # uploaded files to a specific workspace (upload-and-analyze), in
        # which case that session may be shared across turns of a chat.
        self._py_session_id: str | None = None
        # Per-call counter so auto-captured figures from separate python_exec
        # calls get distinct filenames. Combined with a per-dispatcher token so
        # figures don't collide ACROSS turns when the session is reused
        # (figure_<token>_<seq>_<n>.png).
        self._py_fig_seq = 0
        self._fig_token = uuid4().hex[:8]

    def use_python_session(self, session_id: str) -> None:
        """Pre-seed the interpreter session (e.g. one the user uploaded files
        to) so python_exec runs in that workspace instead of creating a new
        one. Called once per turn, before dispatching, when the chat request
        carries an interpreter session id."""
        if session_id:
            self._py_session_id = session_id

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
            if call.name == "python_exec":
                return await self._python_exec(cast(str, args.get("code", "")), chat_session_id)
            if call.name == "render_manim":
                return await self._render_manim(
                    cast(str, args.get("code", "")),
                    cast(str, args.get("scene", "")),
                    cast(str, args.get("quality", "low") or "low"),
                )
            if call.name == "ask_meetings":
                return await self._ask_meetings(cast(str, args.get("question", "")))
            if call.name == "list_meetings":
                return await self._list_meetings()
            if call.name == "get_meeting":
                return await self._get_meeting(cast(str, args.get("meeting_id", "")))
            if call.name == "create_document":
                return await self._create_document(
                    cast(str, args.get("filename", "")),
                    cast(str, args.get("content", "")),
                    cast(str, args.get("format", "markdown")),
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
            if call.name == "list_courses":
                return await self._list_courses(cast("str | None", args.get("level")))
            if call.name == "get_course":
                return await self._get_course(cast(str, args.get("slug", "")))
            if call.name == "get_my_deadlines":
                return await self._get_my_deadlines()
            if call.name == "get_path_gating":
                return await self._get_path_gating(cast(str, args.get("path_slug", "")))
            if call.name == "get_lesson_quiz":
                return await self._get_lesson_quiz(cast(str, args.get("lesson_id", "")))
            if call.name == "get_my_dashboard":
                return await self._get_my_dashboard()
            if call.name == "get_my_course_progress":
                return await self._get_my_course_progress(cast(str, args.get("slug", "")))
            if call.name == "get_my_courses":
                return await self._get_my_courses()
            if call.name == "get_my_notes":
                return await self._get_my_notes(cast("str | None", args.get("course_slug")))
            if call.name == "get_my_notebook":
                return await self._get_my_notebook(
                    cast("str | None", args.get("query")),
                    bool(args.get("due", False)),
                    cast("str | None", args.get("type")),
                )
            if call.name == "get_user_tier":
                return await self._get_user_tier()
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

    async def _ensure_py_session(self) -> str:
        """The interpreter rejects client-invented session ids; create one
        server-side and reuse it for the rest of this turn so python_exec /
        create_document calls share a workspace."""
        if self._ctx.python is None:
            raise RuntimeError("python_unavailable")
        if self._py_session_id is None:
            self._py_session_id = await self._ctx.python.create_session(bearer=self._ctx.bearer)
        return self._py_session_id

    async def _python_exec(self, code: str, chat_session_id: str) -> str:
        if not code.strip():
            return json.dumps({"error": "empty_code"})
        if self._ctx.python is None:
            return json.dumps({"error": "python_unavailable"})
        session_id = await self._ensure_py_session()
        # For matplotlib code that doesn't save its own figures, append an
        # epilogue that captures any open figures — otherwise plt.show() in the
        # headless sandbox produces no file and the user sees no plot.
        exec_code = code
        if wants_figure_capture(code):
            tag = f"{self._fig_token}_{self._py_fig_seq}"
            exec_code = code + _AUTO_CAPTURE_TEMPLATE.format(tag=tag)
            self._py_fig_seq += 1
        res = await self._ctx.python.execute(
            code=exec_code, session_id=session_id, bearer=self._ctx.bearer
        )
        # Reference produced files by name + session id only — the frontend
        # downloads them through the authed /api/interpreter proxy. Image
        # artifacts surface ``has_figure`` like the MATLAB tool.
        #
        # Prefer the interpreter's auto-captured ``rich_outputs`` (explicit
        # image mime types) and union them with extension-sniffed artifacts —
        # rich_outputs catches figures the code never wrote to disk, while the
        # extension scan keeps working if a deployment omits rich_outputs.
        image_exts = (".png", ".jpg", ".jpeg", ".svg", ".gif")
        rich_figures = [o.artifact for o in res.rich_outputs if o.is_image and o.artifact]
        figures = list(rich_figures)
        for a in res.artifacts:
            if a.lower().endswith(image_exts) and a not in figures:
                figures.append(a)
        return json.dumps(
            {
                "ok": res.ok,
                "stdout": res.stdout,
                "stderr": res.stderr,
                "result": res.result,
                "error": res.error,
                "artifacts": list(res.artifacts),
                "figures": figures,
                "session_id": res.session_id,
                "has_figure": len(figures) > 0,
            }
        )

    async def _render_manim(self, code: str, scene: str, quality: str) -> str:
        if not code.strip():
            return json.dumps({"error": "empty_code"})
        if not scene.strip():
            return json.dumps({"error": "missing_scene"})
        if self._ctx.python is None:
            return json.dumps({"error": "python_unavailable"})
        if quality not in {"low", "medium", "high"}:
            quality = "low"
        session_id = await self._ensure_py_session()
        # Render to GIF so it rides the same inline-image path as python_exec
        # figures (the frontend renders a .gif as an animated <img>).
        res = await self._ctx.python.render_manim(
            code=code,
            scene=scene,
            session_id=session_id,
            bearer=self._ctx.bearer,
            quality=quality,
            output_format="gif",
        )
        # Surface the animation under ``figures`` (same contract the frontend
        # already uses for python_exec/matlab figures) so it displays inline.
        anim_exts = (".gif", ".mp4", ".png", ".webm")
        figures = [a for a in res.artifacts if a.lower().endswith(anim_exts)]
        return json.dumps(
            {
                "ok": res.ok,
                "status": res.status,
                "scene": res.scene,
                "error": res.error,
                # Renderer logs can be long; the tail is enough for the LLM to
                # debug a failed scene without bloating the next round. The
                # renderer merges stderr into stdout, so a failed scene's Python
                # traceback (e.g. a bad get_area kwarg) lands in stdout — forward
                # both so the model can see the real cause, not just `error`.
                "stdout": res.stdout[-1500:] if res.stdout else "",
                "stderr": res.stderr[-1500:] if res.stderr else "",
                "artifacts": list(res.artifacts),
                "figures": figures,
                "session_id": res.session_id,
                "has_figure": len(figures) > 0,
            }
        )

    async def _ask_meetings(self, question: str) -> str:
        if not question.strip():
            return json.dumps({"error": "empty_question"})
        if self._ctx.cyberflies is None:
            return json.dumps({"error": "cyberflies_unavailable"})
        reply = await self._ctx.cyberflies.ask_meetings(question=question, bearer=self._ctx.bearer)
        return json.dumps({"reply": reply})

    async def _create_document(self, filename: str, content: str, fmt: str) -> str:
        if not content.strip():
            return json.dumps({"error": "empty_content"})
        if self._ctx.python is None:
            return json.dumps({"error": "python_unavailable"})
        fmt = (fmt or "markdown").lower()
        ext_by_fmt = {"markdown": ".md", "mermaid": ".mmd", "xmind": ".md", "pdf": ".pdf"}
        if fmt not in ext_by_fmt:
            return json.dumps({"error": "unsupported_format", "format": fmt})

        if fmt == "pdf":
            if self._ctx.documents is None:
                return json.dumps({"error": "documents_unavailable"})
            data = self._ctx.documents.render_pdf(content=content)
            content_type = "application/pdf"
        else:
            data = content.encode("utf-8")
            content_type = "text/markdown" if ext_by_fmt[fmt] == ".md" else "text/plain"

        # Normalise the filename to the format's extension.
        base = (filename or "document").strip() or "document"
        base = base.rsplit("/", 1)[-1]
        ext = ext_by_fmt[fmt]
        if not base.lower().endswith(ext):
            base = f"{base.rsplit('.', 1)[0] if '.' in base else base}{ext}"

        session_id = await self._ensure_py_session()
        stored = await self._ctx.python.upload_file(
            session_id=session_id,
            filename=base,
            content=data,
            content_type=content_type,
            bearer=self._ctx.bearer,
        )
        return json.dumps(
            {
                "ok": True,
                "session_id": session_id,
                "filename": stored,
                "format": fmt,
                "size": len(data),
            }
        )

    async def _get_meeting(self, meeting_id: str) -> str:
        if not meeting_id.strip():
            return json.dumps({"error": "missing_meeting_id"})
        if self._ctx.cyberflies is None:
            return json.dumps({"error": "cyberflies_unavailable"})
        detail = await self._ctx.cyberflies.get_meeting(
            meeting_id=meeting_id, bearer=self._ctx.bearer
        )
        if detail is None:
            return json.dumps({"error": "not_found", "meeting_id": meeting_id})
        return json.dumps(
            {
                "id": detail.id,
                "headline": detail.headline,
                "abstract": detail.abstract,
                "bullets": list(detail.bullets),
                "transcript": detail.transcript,
                "status": detail.status,
                "created_at": detail.created_at,
                "word_count": detail.word_count,
                "duration_seconds": detail.duration_seconds,
            }
        )

    async def _list_meetings(self) -> str:
        if self._ctx.cyberflies is None:
            return json.dumps({"error": "cyberflies_unavailable"})
        meetings = await self._ctx.cyberflies.list_meetings(bearer=self._ctx.bearer)
        return json.dumps(
            {
                "meetings": [
                    {
                        "id": m.id,
                        "headline": m.headline,
                        "status": m.status,
                        "created_at": m.created_at,
                    }
                    for m in meetings
                ]
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

    async def _list_courses(self, level: str | None) -> str:
        if self._ctx.list_courses is None:
            return json.dumps({"error": "courses_unavailable"})
        parsed: CourseLevel | None = None
        if level:
            try:
                parsed = parse_level(level)
            except InvalidCourseLevelError:
                return json.dumps({"error": "invalid_level", "level": level})
        courses = await self._ctx.list_courses.execute(level=parsed, include_drafts=False)
        return json.dumps(
            [
                {
                    "slug": c.slug,
                    "title": c.title,
                    "level": c.level.value,
                    "description": c.description,
                    "mandatory": c.mandatory,
                    "lesson_count": len(c.lessons),
                }
                for c in courses
            ]
        )

    async def _get_course(self, slug: str) -> str:
        if self._ctx.get_course is None:
            return json.dumps({"error": "courses_unavailable"})
        if not slug.strip():
            return json.dumps({"error": "missing_slug"})
        try:
            course = await self._ctx.get_course.execute(slug, include_drafts=False)
        except CourseNotFoundError:
            return json.dumps({"error": "not_found", "slug": slug})
        return json.dumps(
            {
                "slug": course.slug,
                "title": course.title,
                "level": course.level.value,
                "description": course.description,
                "lessons": [
                    {
                        "id": str(les.id),
                        "title": les.title,
                        "type": les.lesson_type.value,
                        "duration": les.duration,
                    }
                    for les in course.lessons
                ],
            }
        )

    async def _get_my_deadlines(self) -> str:
        if self._ctx.get_my_deadlines is None:
            return json.dumps({"error": "learning_unavailable"})
        if self._ctx.user_id is None:
            return json.dumps({"error": "sign_in_required"})
        deadlines = await self._ctx.get_my_deadlines.execute(self._ctx.user_id)
        return json.dumps(
            [
                {
                    "path_slug": d.path_slug,
                    "due_at": d.due_at.isoformat() if d.due_at else None,
                    "status": d.status.value,
                    "days_remaining": d.days_remaining,
                }
                for d in deadlines
            ]
        )

    async def _get_path_gating(self, path_slug: str) -> str:
        if self._ctx.path_gating is None:
            return json.dumps({"error": "learning_unavailable"})
        if self._ctx.user_id is None:
            return json.dumps({"error": "sign_in_required"})
        if not path_slug.strip():
            return json.dumps({"error": "missing_path_slug"})
        try:
            gates = await self._ctx.path_gating.execute(
                user_id=self._ctx.user_id, path_slug=path_slug
            )
        except LearningContentNotFoundError:
            return json.dumps({"error": "not_found", "path_slug": path_slug})
        return json.dumps(
            [
                {
                    "module_slug": g.module_slug,
                    "level": g.level,
                    "unlocked": g.unlocked,
                    "completed": g.completed,
                    "blocked_by": g.blocked_by,
                    "reason": g.reason,
                }
                for g in gates
            ]
        )

    async def _get_lesson_quiz(self, lesson_id: str) -> str:
        if self._ctx.get_quiz is None:
            return json.dumps({"error": "quiz_unavailable"})
        try:
            lid = UUID(lesson_id)
        except (ValueError, TypeError, AttributeError):
            return json.dumps({"error": "invalid_lesson_id"})
        try:
            quiz = await self._ctx.get_quiz.execute(lid)
        except QuizNotFoundError:
            return json.dumps({"error": "not_found", "lesson_id": lesson_id})
        # PLAYER VIEW ONLY — deliberately omits is_correct + explanation so
        # the agent can never leak answers to a learner before submission.
        return json.dumps(
            {
                "lesson_id": str(quiz.lesson_id),
                "passing_score": quiz.passing_score,
                "questions": [
                    {
                        "id": str(q.id),
                        "prompt": q.prompt,
                        "options": [{"id": str(o.id), "text": o.text} for o in q.options],
                    }
                    for q in quiz.questions
                ],
            }
        )

    async def _get_my_dashboard(self) -> str:
        if self._ctx.learner_dashboard is None:
            return json.dumps({"error": "analytics_unavailable"})
        if self._ctx.user_id is None:
            return json.dumps({"error": "sign_in_required"})
        d = await self._ctx.learner_dashboard.execute(self._ctx.user_id)
        return json.dumps(
            {
                "enrolled_paths": d.enrolled_paths,
                "completed_paths": d.completed_paths,
                "active_paths": d.active_paths,
                "completed_modules": d.completed_modules,
                "in_progress_modules": d.in_progress_modules,
                "avg_module_percent": d.avg_module_percent,
                "quizzes_attempted": d.quizzes_attempted,
                "quizzes_passed": d.quizzes_passed,
                "quiz_pass_rate": d.quiz_pass_rate,
                "avg_quiz_score": d.avg_quiz_score,
                "total_quiz_attempts": d.total_quiz_attempts,
                "certificates": d.certificates,
                "completed_courses": d.completed_courses,
                "in_progress_courses": d.in_progress_courses,
            }
        )

    async def _get_my_course_progress(self, slug: str) -> str:
        if self._ctx.get_my_course_progress is None:
            return json.dumps({"error": "courses_unavailable"})
        if self._ctx.user_id is None:
            return json.dumps({"error": "sign_in_required"})
        if not slug.strip():
            return json.dumps({"error": "missing_slug"})
        try:
            progress = await self._ctx.get_my_course_progress.execute(
                user_id=self._ctx.user_id, slug=slug
            )
        except CourseNotFoundError:
            return json.dumps({"error": "not_found", "slug": slug})
        return json.dumps(
            {
                "slug": progress.slug,
                "total_lessons": progress.total_lessons,
                "completed_lessons": progress.completed_lessons,
                "percent": progress.percent,
                "completed": progress.completed,
                "lessons": [
                    {"title": view.title, "percent": view.percent, "completed": view.completed}
                    for view in progress.lessons
                ],
            }
        )

    async def _get_my_courses(self) -> str:
        if self._ctx.list_courses is None or self._ctx.get_my_course_progress is None:
            return json.dumps({"error": "courses_unavailable"})
        if self._ctx.user_id is None:
            return json.dumps({"error": "sign_in_required"})
        courses = await self._ctx.list_courses.execute(include_drafts=False)
        out = []
        for course in courses:
            progress = await self._ctx.get_my_course_progress.execute(
                user_id=self._ctx.user_id, slug=course.slug
            )
            out.append(
                {
                    "slug": course.slug,
                    "title": course.title,
                    "level": course.level.value,
                    "percent": progress.percent,
                    "completed": progress.completed,
                    "completed_lessons": progress.completed_lessons,
                    "total_lessons": progress.total_lessons,
                }
            )
        return json.dumps({"courses": out})

    async def _get_my_notes(self, course_slug: str | None) -> str:
        if self._ctx.list_user_notes is None:
            return json.dumps({"error": "notes_unavailable"})
        if self._ctx.user_id is None:
            return json.dumps({"error": "sign_in_required"})
        page = await self._ctx.list_user_notes.execute(
            user_id=self._ctx.user_id, course_slug=course_slug or None
        )
        return json.dumps(
            {
                "notes": [
                    {
                        "id": str(n.id),
                        "course_slug": n.course_slug,
                        "lesson_id": n.lesson_id,
                        "body": n.body,
                        "quote": n.quote,
                        "created_at": n.created_at.isoformat(),
                    }
                    for n in page.items
                ],
                "next_cursor": page.next_cursor,
            }
        )

    async def _get_my_notebook(self, query: str | None, due: bool, note_type: str | None) -> str:
        if self._ctx.list_notebook_notes is None:
            return json.dumps({"error": "notebook_unavailable"})
        if self._ctx.user_id is None:
            return json.dumps({"error": "sign_in_required"})
        # Lenient type parse: ignore an unrecognized value rather than error.
        parsed_type = next((t for t in NoteType if t.value == note_type), None)
        page = await self._ctx.list_notebook_notes.execute(
            user_id=self._ctx.user_id,
            type=parsed_type,
            query=query or None,
            due=due,
        )
        notes = [await self._notebook_note_json(n) for n in page.items]
        return json.dumps({"notes": notes, "next_cursor": page.next_cursor})

    async def _notebook_note_json(self, n: Note) -> dict[str, object]:
        cards: list[dict[str, str]] = []
        if self._ctx.list_note_flashcards is not None and self._ctx.user_id is not None:
            flashcards = await self._ctx.list_note_flashcards.execute(
                user_id=self._ctx.user_id, note_id=n.id
            )
            cards = [{"question": c.question, "answer": c.answer} for c in flashcards]
        return {
            "id": str(n.id),
            "title": n.title,
            "type": n.type.value,
            "body": n.body,
            "course_slug": n.course_slug,
            "lesson_id": str(n.lesson_id) if n.lesson_id else None,
            "language": n.language,
            "tags": list(n.tags),
            "next_review_at": n.next_review_at.isoformat() if n.next_review_at else None,
            "review_interval_days": n.review_interval_days,
            "flashcards": cards,
        }

    async def _get_user_tier(self) -> str:
        if self._ctx.get_wallet_access is None:
            return json.dumps({"error": "access_unavailable"})
        wallet = self._ctx.user.wallet_address if self._ctx.user else None
        if not wallet:
            return json.dumps({"error": "no_wallet_linked"})
        try:
            access = await self._ctx.get_wallet_access.execute(wallet)
        except InvalidWalletAddressError:
            return json.dumps({"error": "invalid_wallet_address", "wallet": wallet})
        t = access.traits
        return json.dumps(
            {
                "address": access.address,
                "has_access_nft": access.has_access_nft,
                "token_count": access.token_count,
                "traits": {
                    "learning": t.learning,
                    "frontend": t.frontend,
                    "backend": t.backend,
                    "blog_creator": t.blog_creator,
                    "admin": t.admin,
                    "marketplace": t.marketplace,
                },
            }
        )

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
