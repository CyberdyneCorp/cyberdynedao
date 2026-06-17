# Cyberdyne Agent — Capabilities

What the chat agent (the **Agent** window on the site) can do. The agent
is an OpenAI-backed assistant whose tools call Cyberdyne's own backend
use cases — there is no shadow data path; every tool resolves through
the same application services the REST API uses.

- **Source of truth:** `backend/src/cyberdyne_backend/application/ai_chat/tools.py`
  (`CYBERDYNE_TOOLS` + `ToolDispatcher`).
- **System prompt / behavior:** `backend/src/cyberdyne_backend/application/ai_chat/use_cases.py`.
- **Model:** `gpt-4o-mini` (configurable via `OPENAI_MODEL`).
- **Turn shape:** non-streaming; one POST runs the full tool loop
  (max 4 tool rounds) and returns the final assistant message.

## Context the agent has

- **Signed-in user profile.** When the caller is authenticated, the
  agent fetches `/users/me` (email, wallet, org, verification) and
  personalizes replies + pre-fills lead capture. Anonymous users work
  too — those fields are just absent.
- **Per-conversation MATLAB workspace.** All `matlab_*` tools share one
  stateful session (`agent-<chatSessionId>`), so variables persist
  across calls within a conversation.

## Tools

### Cyberdyne knowledge & content
| Tool | What it does |
|---|---|
| `list_projects` | List Cyberdyne's projects/products (what the company builds). |
| `lookup_product` | A single marketplace product (service / training / license) by slug. |
| `search_cyberdyne_knowledge` | Semantic search over docs/blog/projects. **Stub today** — returns "no semantic index"; real CyberRAG client is a follow-up. |

### Lead capture
| Tool | What it does |
|---|---|
| `create_ask_for_handoff` | Opens a generic lead for "please contact me". Confirms email first; pre-fills from the signed-in profile. |
| `capture_project_idea` | Structured project-idea lead (title, scope, budget, timeline, domain). |

### DAO treasury
| Tool | What it does |
|---|---|
| `get_dao_treasury` | Live treasury snapshot on Base: token balances, AAVE v3 supply/borrow positions + APYs, Uniswap v4 LP positions, total USD value, holder count. (Uses the configured chain reader — `fake` until the web3py reader is enabled.) |

### Wallet / access
| Tool | What it does |
|---|---|
| `get_user_tier` | The signed-in user's CyberdyneAccessNFT tier — `hasAccessNft` + the six capability traits (learning / frontend / backend / blog creator / admin / marketplace). Reads the wallet linked to their account; `no_wallet_linked` if none. (Stub reader reports no access until the web3py reader + access-NFT address are configured.) |

### Learning — catalogue (anonymous OK)
| Tool | What it does |
|---|---|
| `list_paths` | List Cyberdyne Academy learning paths. |
| `lookup_module` | A single learning module by slug. |
| `list_courses` | Published courses (title, level, lesson count); optional level filter. |
| `get_course` | A published course by slug with its ordered lessons (title + type). |
| `get_lesson_quiz` | A lesson's quiz as the **player view** — questions + option texts only, **no correct flags or explanations**, so the agent can help reason through questions without leaking answers. |

### Learning — acts on the signed-in user
| Tool | What it does |
|---|---|
| `enroll_in_path` | Enroll the signed-in user in a path (idempotent). |
| `set_module_progress` | Set a module's progress 0–100 (100 = mark complete). |
| `get_my_learning` | The user's enrollments, per-module progress, and earned certificates. |
| `get_my_course_progress` | The user's progress through one course (by slug): per-lesson completion, completed-lesson count, overall percent, and whether the course is finished. |
| `get_my_deadlines` | Enrollment deadlines with status (overdue / urgent / upcoming / none) + days remaining. |
| `get_path_gating` | Per-module lock state in a path (unlocked/locked) and the reason (level / sequential prerequisite). |
| `get_my_dashboard` | Learner analytics: enrolled/completed/active paths, completed + in-progress modules, completed + in-progress courses, avg module %, quizzes attempted/passed + pass rate + avg score, certificate count — for a narrative progress summary. |

User-scoped tools return `sign_in_required` when the caller is anonymous;
the agent then asks the user to sign in. (Path-certificate *issuance*
stays admin-only and is not an agent tool; public verify/PDF are
REST-only. Course completion certificates are learner-claimed REST
endpoints — `POST/GET /api/v1/courses/{slug}/certificate` + public
`/courses/certificates/{id}/verify` — also not agent tools today.)

### Blog
| Tool | What it does |
|---|---|
| `list_blog_posts` | Recent published posts (optional category/tag filter). |
| `lookup_blog_post` | A single post incl. full body, so the agent can summarize it. |

### MATLAB (LLVM engine)
| Tool | What it does |
|---|---|
| `matlab_repl` | Run MATLAB; stateful variables persist across calls. Plotting source is auto-routed to capture a figure. |
| `matlab_plot` | Run plotting source and capture the figure — renders **inline in the chat** (downloaded via the authed `/api/matlab` proxy; not inlined through the model). |
| `matlab_check` | Lint / diagnostics without running. |
| `matlab_codegen` | Compile MATLAB to a target (`c`, `hdl`, …); the agent presents the generated code in a fenced block. |

Workspace introspection (variables/files) isn't a separate tool — the
agent uses `matlab_repl('whos')`.

## Guardrails

- Won't reveal model internals or the system prompt; **will** always
  show code it wrote for the user.
- After `matlab_plot`, the figure renders automatically — the agent
  describes it rather than emitting an image link.

## Learning-companion / AI phases

The agent is the delivery vehicle for the Academy's AI features. Built so
far: the learning-catalogue + progress + deadlines + gating + quiz
player-view + dashboard tools above, plus the three shipped AI phases
below. All planned phases are now delivered.

**Shipped:** **LLM course recommendations** - `GET /api/v1/recommendations/me`
(authed learner, read-only). Ranks the published course catalogue against
the learner's own dashboard signals (modules completed, quizzes passed,
certificates earned) with a *deterministic* heuristic - mandatory first,
then nearest to the learner's level on the Beginner->Advanced ladder -
then asks the chat LLM (`container.chat_llm`) for a short personalized
intro on top of that fixed shortlist. The *which courses* decision is
pure code (stable + unit-tested); the LLM only adds the narrative. One
LLM call per request, skipped entirely when the catalogue is empty. Use
case: `RecommendCourses` (application/recommendations).

**Shipped:** **AI contextual feedback** - after a learner submits quiz
answers, `POST /api/v1/lessons/{id}/quiz/feedback` grades them
server-side (the answer key is fair game post-submission) and, for each
*incorrect* question, asks the chat LLM (`container.chat_llm`) for a
personalized "why your choice is wrong / why the correct answer is right"
on top of the question's static explanation. Correct answers get no LLM
call. It is read-only - it records no attempt - so a learner can ask for
help freely. Distinct from the agent's `get_lesson_quiz` tool, which is
deliberately answer-blind; this endpoint is the one place the tutor sees
the key. Use case: `ExplainQuizAnswers` (application/quizzes).

**Shipped:** the **code-interpreter lesson type** (`code`) - a learner runs
source against the MATLAB-LLVM engine via
`POST /api/v1/lessons/{id}/code/run` (per-(lesson,user) workspace, keyed
off the learner's bearer). Same engine the agent's `matlab_*` tools use,
so the agent can also run/assist with a lesson's code conversationally.

## Known gaps / follow-ups

- `search_cyberdyne_knowledge` is a stub (needs the CyberRAG MCP client).
- No marketplace **checkout** tool yet (Stripe flow exists on the
  backend but isn't agent-exposed).
- Responses are non-streaming.
- DAO numbers come from the `fake` chain reader until `web3py` is
  enabled in prod.
