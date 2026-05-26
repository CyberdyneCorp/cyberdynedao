"""Phase 2 — content extensions (projects, services, contact, resources) + leads.

Creates and seeds:
- ``projects`` from ``frontend/src/lib/data/products.ts``
- ``service_sections`` from ``services.ts`` + ``services-meta`` page payload
- ``contact_methods`` from ``contact.ts`` + ``contact-meta`` page payload
- ``resource_groups`` from the ``learn.ts`` Resources section
- ``asks`` + ``ask_events`` tables (empty)

Revision ID: 202605270001
Revises: 202605260001
Create Date: 2026-05-27 00:00:00
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202605270001"
down_revision: str | Sequence[str] | None = "202605260001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


# ── Seed data ────────────────────────────────────────────────────────


PROJECTS = [
    {
        "id": "cyberspace",
        "name": "CyberSpace",
        "icon": "🌍",
        "description": (
            "Four-pillar 3D geospatial platform combining a real-time dashboard, "
            "agricultural parametric-insurance workbench, RF coverage & link planning, "
            "and OpenFOAM wind + structural FSI simulation — with a single conversational "
            "AI agent across all of it."
        ),
        "features": [
            "25 toggleable layers across 7 sections",
            "Multi-tenant insurance portfolios + parametric triggers",
            "ITM & ITU-R P.1812-7 RF planning",
            "OpenFOAM CFD + Calculix FEA",
        ],
        "extra_features": [
            "Live S1 / S3 / S5P satellite cross-checks",
            "JRC / UN GDACS hazard alerts",
            "AIS, OpenSky and Celestrak feeds",
            "EUDR-ready polygon analysis",
        ],
        "palette": "green",
        "status": "live",
        "full_width": True,
        "sort_order": 10,
    },
    {
        "id": "cyberdynedao",
        "name": "CyberdyneDAO",
        "icon": "🖥️",
        "description": (
            "Retro-terminal Web3 platform for DAO operations. SvelteKit on Base with "
            "Web3Auth social login, WalletConnect, and NFT-gated access — wrapped in a "
            "green-phosphor cyberpunk shell."
        ),
        "features": [
            "Six-tier NFT-based access control",
            "IPFS + USDC training-materials contract",
            "Real-time on-chain balance & permissions",
            "Draggable retro window UI",
        ],
        "extra_features": None,
        "palette": "blue",
        "status": "active",
        "full_width": False,
        "sort_order": 20,
    },
    {
        "id": "cyberdyneauth",
        "name": "CyberdyneAuth",
        "icon": "🔐",
        "description": (
            "Centralized identity backbone for the Cyberdyne stack. FastAPI microservice "
            "issuing short-lived JWTs over httpOnly cookies (browsers) and Bearer tokens "
            "(services)."
        ),
        "features": [
            "Google + Microsoft OAuth + EIP-4361 wallet sign-in",
            "Sandboxed user hooks (subprocess + netns)",
            "NFT-gated access & on-chain IAM",
            "143+ tests, >83% coverage",
        ],
        "extra_features": None,
        "palette": "red",
        "status": "live",
        "full_width": False,
        "sort_order": 30,
    },
    {
        "id": "cyberstac",
        "name": "CyberSTAC",
        "icon": "📡",
        "description": (
            "STAC-compliant catalog server for satellite and drone imagery, exposing both "
            "a standards REST API and a first-class MCP surface so LLM agents can query "
            "the catalog natively."
        ),
        "features": [
            "REST + MCP dual interface",
            "Dual backend: MongoDB or pgstac",
            "bbox / datetime / CQL2 filters",
            "Hexagonal + MVVM SvelteKit frontend",
        ],
        "extra_features": None,
        "palette": "purple",
        "status": "active",
        "full_width": False,
        "sort_order": 40,
    },
    {
        "id": "cybergeopy",
        "name": "CyberGeoPy",
        "icon": "🗺️",
        "description": (
            "Geospatial processing engine of the Cyberdyne stack. Python library unifying "
            "ten satellite product managers, spectral indices, SAR primitives, anomaly "
            "detection, parametric payouts, and EUDR compliance."
        ),
        "features": [
            "Sentinel-1/2/3/5P + Landsat + VIIRS + SMAP + ERA5",
            "Pure-Python SAR (coherence, interferogram, unwrap)",
            "Climatology baseline + anomaly engine",
            "EUDR pipeline with TRACES-ready DDS payload",
        ],
        "extra_features": None,
        "palette": "orange",
        "status": "development",
        "full_width": False,
        "sort_order": 50,
    },
    {
        "id": "orgpilot",
        "name": "OrgPilot",
        "icon": "🧭",
        "description": (
            "AI-native company operating system. Connects people, projects, tasks, code, "
            "AI agents, and treasury under one governance layer — answers not just "
            '"what tasks exist?" but "who should do this, what is blocked, should '
            'capital move?"'
        ),
        "features": [
            "270+ REST endpoints, 50+ MCP tools",
            "Company digital twin (skills, capacity, roles)",
            "PM intelligence & overload detection",
            "2000+ backend tests",
        ],
        "extra_features": None,
        "palette": "blue",
        "status": "active",
        "full_width": False,
        "sort_order": 60,
    },
    {
        "id": "yieldpath",
        "name": "YieldPath",
        "icon": "📊",
        "description": (
            "AI-powered DeFi life planner. Monitors LPs, lending, and staking positions, "
            "optimizes yields, and projects your path to financial independence — all in "
            "natural language."
        ),
        "features": [
            "DeFi LP / lending / staking monitoring",
            "Automated yield optimization",
            "FIRE-planning simulations",
            "Natural-language AI chat",
        ],
        "extra_features": None,
        "palette": "green",
        "status": "planning",
        "full_width": False,
        "sort_order": 70,
    },
    {
        "id": "terraform-game",
        "name": "Terraform",
        "icon": "🤖",
        "description": (
            "Mobile Action-RTS where you pilot a bipedal robot rebuilding a post-"
            "apocalyptic Earth, defending against insectoid swarms, and earning real DeFi "
            "yield via AAVE and Uniswap on Base."
        ),
        "features": [
            "Unity3D URP — iPad / iPhone first",
            "USDC economy (no proprietary token)",
            "AAVE V3 supply + Uniswap V3 LP fees",
            "Cute-anime low-poly art",
        ],
        "extra_features": None,
        "palette": "purple",
        "status": "design",
        "full_width": False,
        "sort_order": 80,
    },
    {
        "id": "matlab-compiler",
        "name": "Matlab Compiler",
        "icon": "⚙️",
        "description": (
            "Real LLVM + MLIR compiler stack for MATLAB. Treats MATLAB as a source "
            "language and lowers through progressive MLIR passes — emit portable "
            "C/C++/Python/TS, synthesizable SystemVerilog, Verilog-A, or JIT in-process."
        ),
        "features": [
            "322-program regression corpus",
            "Modular ~36k-LoC runtime, no BLAS/LAPACK shipped",
            "6 toolbox surfaces: Signal, Control, Comms, RF, Antenna, Propagation",
            "DAP debug server + .mflow flowchart I/O",
        ],
        "extra_features": None,
        "palette": "orange",
        "status": "active",
        "full_width": False,
        "sort_order": 90,
    },
    {
        "id": "matforge-ide",
        "name": "MatForge IDE",
        "icon": "💻",
        "description": (
            "SwiftUI macOS IDE for the matlab_llvm toolchain. Editor, REPL, full DAP "
            "debugger, visual .mflow flowchart editor, mflowLink signal-flow modeling, "
            "and mStateflow state-charts in one window."
        ),
        "features": [
            "Conditional / log / hit-count breakpoints",
            "Simulink-style signal-flow modeling",
            "State-chart authoring with TeX annotations",
            "≥97% test coverage on logic core",
        ],
        "extra_features": None,
        "palette": "red",
        "status": "development",
        "full_width": False,
        "sort_order": 100,
    },
    {
        "id": "hdl-simulator",
        "name": "HDL Backend Simulator",
        "icon": "🔌",
        "description": (
            "Cloud-ready HDL simulation platform + visual digital-circuit designer. "
            "REST API for compiling and simulating VHDL/Verilog (GHDL + Icarus + Yosys); "
            "SvelteKit frontend (DigiSim) for drag-and-drop circuit design."
        ),
        "features": [
            "VHDL / Verilog / SystemVerilog",
            "VCD + GHW waveforms, Yosys netlists",
            "18 component types, 50-level undo/redo",
            "Webhook callbacks on job completion",
        ],
        "extra_features": None,
        "palette": "blue",
        "status": "active",
        "full_width": False,
        "sort_order": 110,
    },
    {
        "id": "vision-factory",
        "name": "Vision Factory",
        "icon": "👁️",
        "description": (
            "Computer-vision pipeline validating that warehouse operators deposit items "
            "in the correct bin slot. Hybrid YOLOv8 + ByteTrack + SAM2 architecture, "
            "built for Mercado Livre."
        ),
        "features": [
            "~30 FPS real-time detection",
            "SAM2 precision masks at the critical ROI",
            "~40% less compute via hybrid scheduling",
            "Edge-deployable: Jetson + TensorRT",
        ],
        "extra_features": None,
        "palette": "green",
        "status": "active",
        "full_width": False,
        "sort_order": 120,
    },
    {
        "id": "surf4me",
        "name": "Surf4Me",
        "icon": "🏄",
        "description": (
            "Multi-platform marketplace connecting surfers with instructors, "
            "photographers, gear rentals, and accommodations. Five user types share one "
            "ecosystem."
        ),
        "features": [
            "SwiftUI (iOS) + Jetpack Compose (Android)",
            "Web3Auth wallet login",
            "Live surf + marine conditions",
            "Location-based discovery & bookings",
        ],
        "extra_features": None,
        "palette": "purple",
        "status": "active",
        "full_width": False,
        "sort_order": 130,
    },
    {
        "id": "obsidian-mcp",
        "name": "Obsidian MCP Server",
        "icon": "🧠",
        "description": (
            "Dual REST + MCP backend giving AI agents structured access to Obsidian "
            "vaults — semantic search via pgvector, knowledge graph via Apache AGE, and "
            "user-defined typed tables."
        ),
        "features": [
            "Vault ingestion from ZIP + wiki-link parsing",
            "pgvector + OpenAI embedding semantic search",
            "Graph queries: backlinks, shortest path, hubs, orphans",
            "CSV-importable structured tables",
        ],
        "extra_features": None,
        "palette": "orange",
        "status": "active",
        "full_width": False,
        "sort_order": 140,
    },
    {
        "id": "claude-skills",
        "name": "Claude Skills",
        "icon": "⚡",
        "description": (
            "Open collection of custom skills extending Claude Code — daily journaling, "
            "image / PDF / JSON tooling, NotebookLM automation, PostgreSQL exploration, "
            "Obsidian sync, and more."
        ),
        "features": [
            "Drop-in skills for Claude Code",
            "Workflow automation (journal, study, bookmarks)",
            "Data tooling (PG, JSON, CSV, PDF, image)",
            "Open source — leonardoaraujosantos/my_ai_skills",
        ],
        "extra_features": None,
        "palette": "red",
        "status": "active",
        "full_width": False,
        "sort_order": 150,
    },
]


SERVICE_SECTIONS = [
    {
        "id": "geospatial-sovereign",
        "icon": "🌍",
        "title": "Geospatial & Sovereign AI",
        "intro": (
            "Domain-specific AI on real satellite data — built for regulated buyers: "
            "insurers, ministries, development finance, EUDR-affected exporters."
        ),
        "bullets": [
            {"title": "3D dashboards", "description": "25 toggleable layers, multi-tenant RLS, agent-driven workflows."},
            {"title": "STAC catalogs with native MCP", "description": "dual backend (MongoDB / pgstac), CQL2 filters, agent-first discovery."},
            {"title": "Parametric insurance", "description": "climatology baseline + anomaly engine + step / linear / sigmoid payouts."},
            {"title": "EUDR pipelines", "description": "polygon → JRC + Hansen + WDPA → TRACES-ready DDS payload."},
            {"title": "SAR primitives", "description": "pure-Python coherence, interferogram, unwrap_phase — no SNAP / GAMMA dependency."},
            {"title": "RF planning", "description": "ITM, ITU-R P.1812-7, sector plans, link budgets, GeoJSON / KML export."},
        ],
        "palette": "green",
        "full_width": True,
        "sort_order": 10,
    },
    {
        "id": "strategy",
        "icon": "🎯",
        "title": "Strategy & Discovery",
        "intro": "Turn an idea into a buildable plan — architecture decided before the first commit.",
        "bullets": [
            {"title": "Product strategy & PRDs", "description": "scoped for full-stack delivery, not slideware."},
            {"title": "Architecture review", "description": "hexagonal cores, ports & adapters, tested at the seams."},
            {"title": "Tokenomics & DAO design", "description": "yield-powered models where DeFi pays the ops bill."},
            {"title": "Roadmap fit", "description": "phased, governance-aware, Cosmos-SDK + IBC when scale demands it."},
        ],
        "palette": "purple",
        "full_width": False,
        "sort_order": 20,
    },
    {
        "id": "frontend",
        "icon": "🎨",
        "title": "Frontend Engineering",
        "intro": "Fast, portable frontends on the same component library already shipping in production.",
        "bullets": [
            {"title": "Web apps", "description": "Svelte + TypeScript + Tailwind, MVVM end-to-end."},
            {"title": "Mobile", "description": "SwiftUI (iOS) + Kotlin / Jetpack Compose (Android)."},
            {"title": "Design system", "description": "@cyberdynecorp/svelte-ui-core — retro chrome and crypto primitives included."},
            {"title": "Accessibility & type-safety", "description": "svelte-check clean, a11y-tested on every PR."},
        ],
        "palette": "blue",
        "full_width": False,
        "sort_order": 30,
    },
    {
        "id": "backend",
        "icon": "⚡",
        "title": "Backend, Data & DevOps",
        "intro": "Hexagonal cores, real coverage gates, predictable releases.",
        "bullets": [
            {"title": "APIs", "description": "FastAPI, Go, Rust — import-linter contracts enforce architecture on every PR."},
            {"title": "REST + MCP dual surfaces", "description": "the same use cases serve agents and apps."},
            {"title": "PostgreSQL stack", "description": "pgvector + Apache AGE for knowledge graphs; pgstac for spatial."},
            {"title": "Ops", "description": "Coolify-first deploys, containers, structlog + Prometheus + Sentry."},
        ],
        "palette": "orange",
        "full_width": False,
        "sort_order": 40,
    },
    {
        "id": "ai",
        "icon": "🧠",
        "title": "AI & Knowledge Systems",
        "intro": "From RAG to agents — production, not demos.",
        "bullets": [
            {"title": "Knowledge graphs", "description": "LightRAG-backed, multi-tenant from day one."},
            {"title": "Document ingestion", "description": "nine adapters, automatic fallback, LLM image enrichment, 97% coverage."},
            {"title": "LLM ops", "description": "hosted (OpenRouter, Anthropic, OpenAI) or self-hosted (Ollama, vLLM)."},
            {"title": "MCP servers", "description": "first-class agent access to your data — same use cases over HTTP."},
        ],
        "palette": "red",
        "full_width": False,
        "sort_order": 50,
    },
    {
        "id": "blockchain",
        "icon": "⛓️",
        "title": "Blockchain & On-Chain Apps",
        "intro": "Credible Web3 that survives mainnet.",
        "bullets": [
            {"title": "EVM smart contracts", "description": "Solidity with oracles, tested release flows, audited."},
            {"title": "Wallet auth", "description": "EIP-4361, Web3Auth social login, WalletConnect (50+ wallets)."},
            {"title": "Chain focus", "description": "Base + Arbitrum for cost/perf, USDC-native economies."},
            {"title": "NFT-tier IAM", "description": "on-chain Identity / Policy / Group contracts, dynamic permissions."},
            {"title": "DeFi treasury", "description": "AAVE supply, Uniswap LPs, covered loans — proven, not theorized."},
            {"title": "DAO at scale", "description": "Cosmos-SDK + IBC when governance throughput needs to scale."},
        ],
        "palette": "blue",
        "full_width": False,
        "sort_order": 60,
    },
    {
        "id": "security",
        "icon": "🔒",
        "title": "Security & Reliability",
        "intro": "Trust is a feature — and we test it like one.",
        "bullets": [
            {"title": "Sandboxed user code", "description": "real subprocess + Linux netns + egress allowlist (the model in CyberdyneAuth)."},
            {"title": "Hardened parsers", "description": "XXE defenses, size caps, sanitization, fuzzing on untrusted input."},
            {"title": "SLA-style support", "description": "incident response, patch windows, monthly ops reviews."},
            {"title": "Least-privilege everywhere", "description": "secrets hygiene, threat modeling, audit trails."},
        ],
        "palette": "purple",
        "full_width": False,
        "sort_order": 70,
    },
]


SERVICES_META_PAYLOAD = {
    "hero_subtitle": (
        "Production-grade software end-to-end — strategy, full-stack engineering, AI, "
        "geospatial intelligence, blockchain, and the open infrastructure to run it."
    ),
    "workflow_steps": [
        {"title": "Discover", "description": "Find the smallest valuable slice."},
        {"title": "Architect", "description": "Pick ports & adapters before the first PR."},
        {"title": "Build", "description": "Tests, telemetry, and CI from day zero."},
        {"title": "Ship", "description": "To users, not staging."},
        {"title": "Measure", "description": "What moved (or didn't) and why."},
        {"title": "Govern", "description": "DAO rituals and clear economics, when it's time."},
    ],
    "why_points": [
        {"title": "Production proof", "description": "18 projects shipping. Coverage gates at 83–97%. Tests in the thousands."},
        {"title": "Open by default", "description": "Every project hexagonal, open-source, swappable at the seams — no vendor lock-in."},
        {"title": "Full stack, one collective", "description": "Strategy, mobile, backend, AI, geospatial, and Web3 — one team, one taste."},
        {"title": "Yield-powered economics", "description": "For clients who want ops funded by DeFi yield, not per-seat SaaS taxes."},
    ],
    "cta_headline": "Ready to Build?",
    "cta_body": (
        "Whether it's a regulated geospatial system, an AI-native operating system, or "
        "a DeFi-funded platform — let's scope the first valuable slice."
    ),
    "cta_pills": ["Strategy", "Engineering", "AI", "Geospatial", "Web3"],
}


CONTACT_METHODS = [
    {
        "id": "whatsapp",
        "name": "WhatsApp",
        "icon": "💬",
        "description": "Quickest path to a human. Project enquiries, contracts, and quick technical questions.",
        "action": "Start Chatting",
        "link": "https://wa.me/1234567890?text=Hello%20Cyberdyne%20Team",
        "brand_solid": "#25d366",
        "brand_hover": "#128c7e",
        "brand_rgb": "37, 211, 102",
        "tagline": "Usually responds within hours",
        "sort_order": 10,
    },
    {
        "id": "discord",
        "name": "Discord",
        "icon": "🎮",
        "description": "Our open community — builders, researchers, and the curious. Drop in, lurk, ask questions.",
        "action": "Join Server",
        "link": "https://discord.gg/cyberdyne",
        "brand_solid": "#5865f2",
        "brand_hover": "#4752c4",
        "brand_rgb": "88, 101, 242",
        "tagline": "Community channel",
        "sort_order": 20,
    },
    {
        "id": "github",
        "name": "GitHub",
        "icon": "🛠️",
        "description": "Source for everything we ship. Open an issue, send a PR, or just browse the stack.",
        "action": "Visit Org",
        "link": "https://github.com/CyberdyneCorp",
        "brand_solid": "#1f2937",
        "brand_hover": "#000000",
        "brand_rgb": "31, 41, 55",
        "tagline": "Open source, by default",
        "sort_order": 30,
    },
]


CONTACT_META_PAYLOAD = {
    "headline": "Let's talk",
    "body": (
        "Whether it's a contract, a collaboration, or a research partnership — pick the "
        "channel that fits. We read everything that lands."
    ),
}


RESOURCE_GROUPS = [
    {
        "id": "cyberdyne",
        "icon": "🛠️",
        "title": "Cyberdyne",
        "links": [
            {"label": "CyberdyneCorp on GitHub", "href": "https://github.com/CyberdyneCorp", "disabled": False},
            {"label": "Svelte UI Core (component library)", "href": "https://cyberdynecorp.github.io/", "disabled": False},
            {"label": "CyberDocExtractor on PyPI", "href": "https://pypi.org/project/cyberdocextractor/", "disabled": False},
        ],
        "sort_order": 10,
    },
    {
        "id": "protocols",
        "icon": "📚",
        "title": "Protocols & Specs",
        "links": [
            {"label": "Model Context Protocol (MCP)", "href": "https://modelcontextprotocol.io/", "disabled": False},
            {"label": "STAC — SpatioTemporal Asset Catalog", "href": "https://stacspec.org/", "disabled": False},
            {"label": "EIP-4361 (Sign-In With Ethereum)", "href": "https://eips.ethereum.org/EIPS/eip-4361", "disabled": False},
            {"label": "Cosmos SDK Docs", "href": "https://docs.cosmos.network/", "disabled": False},
            {"label": "Solidity Documentation", "href": "https://docs.soliditylang.org/", "disabled": False},
        ],
        "sort_order": 20,
    },
    {
        "id": "tools",
        "icon": "⚙️",
        "title": "Tools",
        "links": [
            {"label": "FastMCP", "href": "https://github.com/jlowin/fastmcp", "disabled": False},
            {"label": "LightRAG", "href": "https://github.com/HKUDS/LightRAG", "disabled": False},
            {"label": "Foundry (smart-contract toolkit)", "href": "https://book.getfoundry.sh/", "disabled": False},
            {"label": "Hardhat", "href": "https://hardhat.org/", "disabled": False},
            {"label": "Web3Auth", "href": "https://web3auth.io/", "disabled": False},
        ],
        "sort_order": 30,
    },
    {
        "id": "communities",
        "icon": "🌐",
        "title": "Communities",
        "links": [
            {"label": "Cyberdyne Discord (coming soon)", "href": "#", "disabled": True},
            {"label": "Developer Forum (coming soon)", "href": "#", "disabled": True},
            {"label": "Weekly Dev Calls (coming soon)", "href": "#", "disabled": True},
        ],
        "sort_order": 40,
    },
]


def upgrade() -> None:
    projects_table = op.create_table(
        "projects",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("icon", sa.String(length=16), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("features", sa.JSON(), nullable=False),
        sa.Column("extra_features", sa.JSON(), nullable=True),
        sa.Column("palette", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("full_width", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
    )
    service_sections_table = op.create_table(
        "service_sections",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("icon", sa.String(length=16), nullable=False),
        sa.Column("title", sa.String(length=128), nullable=False),
        sa.Column("intro", sa.Text(), nullable=False),
        sa.Column("bullets", sa.JSON(), nullable=False),
        sa.Column("palette", sa.String(length=32), nullable=False),
        sa.Column("full_width", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
    )
    contact_methods_table = op.create_table(
        "contact_methods",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("icon", sa.String(length=16), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("action", sa.String(length=64), nullable=False),
        sa.Column("link", sa.String(length=512), nullable=False),
        sa.Column("brand_solid", sa.String(length=16), nullable=False),
        sa.Column("brand_hover", sa.String(length=16), nullable=False),
        sa.Column("brand_rgb", sa.String(length=32), nullable=False),
        sa.Column("tagline", sa.String(length=128), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
    )
    resource_groups_table = op.create_table(
        "resource_groups",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("icon", sa.String(length=16), nullable=False),
        sa.Column("title", sa.String(length=128), nullable=False),
        sa.Column("links", sa.JSON(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_table(
        "asks",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("channel", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("email", sa.String(length=256), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("product_slug", sa.String(length=64), nullable=True),
        sa.Column("source_url", sa.String(length=512), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("owner_user_id", sa.Uuid(), nullable=True),
        sa.Column("notes_md", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_asks_status", "asks", ["status"])
    op.create_index("ix_asks_channel", "asks", ["channel"])
    op.create_index("ix_asks_created_at", "asks", ["created_at"])
    op.create_table(
        "ask_events",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "ask_id",
            sa.Uuid(),
            sa.ForeignKey("asks.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("by_user_id", sa.Uuid(), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_ask_events_ask_id", "ask_events", ["ask_id"])

    op.bulk_insert(projects_table, PROJECTS)
    op.bulk_insert(service_sections_table, SERVICE_SECTIONS)
    op.bulk_insert(contact_methods_table, CONTACT_METHODS)
    op.bulk_insert(resource_groups_table, RESOURCE_GROUPS)
    # Page-level payloads use the existing content_pages table.
    op.bulk_insert(
        sa.table(
            "content_pages",
            sa.column("slug", sa.String),
            sa.column("payload", sa.JSON),
            sa.column("updated_at", sa.DateTime(timezone=True)),
        ),
        [
            {"slug": "services-meta", "payload": SERVICES_META_PAYLOAD, "updated_at": None},
            {"slug": "contact-meta", "payload": CONTACT_META_PAYLOAD, "updated_at": None},
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM content_pages WHERE slug IN ('services-meta', 'contact-meta')")
    op.drop_index("ix_ask_events_ask_id", table_name="ask_events")
    op.drop_table("ask_events")
    op.drop_index("ix_asks_created_at", table_name="asks")
    op.drop_index("ix_asks_channel", table_name="asks")
    op.drop_index("ix_asks_status", table_name="asks")
    op.drop_table("asks")
    op.drop_table("resource_groups")
    op.drop_table("contact_methods")
    op.drop_table("service_sections")
    op.drop_table("projects")
