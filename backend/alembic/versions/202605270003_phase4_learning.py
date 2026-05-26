"""Phase 4 — learning catalogue + per-user state tables.

Seeds the module + path catalogue verbatim from
``frontend/src/lib/data/learn.ts`` so the existing LearnView can
hydrate from the backend without any content drift.

Revision ID: 202605270003
Revises: 202605270002
Create Date: 2026-05-27 00:02:00
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202605270003"
down_revision: str | Sequence[str] | None = "202605270002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


_MODULES: list[dict[str, object]] = [
    {
        "slug": "blockchain-basics",
        "title": "Blockchain Fundamentals",
        "category": "Blockchain",
        "description": (
            "Distributed ledgers, consensus, cryptographic hashing — the "
            "substrate every Web3 system stands on."
        ),
        "level": "Beginner",
        "duration": "45 min",
        "icon": "🔗",
        "topics": [
            "Distributed Ledgers",
            "Consensus Mechanisms",
            "Cryptographic Hashing",
            "Blocks & Transactions",
        ],
        "sort_order": 10,
    },
    {
        "slug": "smart-contracts",
        "title": "Smart Contracts Deep Dive",
        "category": "Development",
        "description": (
            "Solidity, security patterns, gas optimization, and the test "
            "discipline that keeps mainnet deploys boring."
        ),
        "level": "Intermediate",
        "duration": "1h 30min",
        "icon": "📜",
        "topics": [
            "Solidity Basics",
            "Contract Security",
            "Gas Optimization",
            "Foundry & Hardhat",
        ],
        "sort_order": 20,
    },
    {
        "slug": "hexagonal-architecture",
        "title": "Hexagonal Architecture in Production",
        "category": "Architecture",
        "description": (
            "Ports & adapters, dependency inversion, and how to enforce "
            "them with import-linter so the boundaries actually hold "
            "over time."
        ),
        "level": "Intermediate",
        "duration": "1h 30min",
        "icon": "⬡",
        "topics": [
            "Ports & Adapters",
            "Dependency Inversion",
            "Import-Linter Contracts",
            "Use Cases & UoW",
        ],
        "sort_order": 30,
    },
    {
        "slug": "mcp-servers",
        "title": "MCP Servers & Agent Backends",
        "category": "Development",
        "description": (
            "Model Context Protocol — give an LLM agent first-class "
            "access to the same use cases your REST API serves."
        ),
        "level": "Intermediate",
        "duration": "1h 15min",
        "icon": "🔌",
        "topics": [
            "MCP Protocol",
            "FastMCP & FastAPI",
            "Dual REST + MCP Surfaces",
            "Tool Design",
        ],
        "sort_order": 40,
    },
    {
        "slug": "rag-knowledge-graphs",
        "title": "Knowledge Graphs & RAG",
        "category": "AI",
        "description": (
            "Beyond flat-chunk RAG — entity-relation graphs on pgvector "
            "+ Apache AGE, multi-hop queries, multi-tenant workspaces."
        ),
        "level": "Advanced",
        "duration": "2h",
        "icon": "🧠",
        "topics": [
            "LightRAG Engine",
            "pgvector + AGE",
            "Multi-hop Queries",
            "Multi-tenant Workspaces",
        ],
        "sort_order": 50,
    },
    {
        "slug": "geospatial-ai",
        "title": "Geospatial AI Foundations",
        "category": "Geospatial",
        "description": (
            "STAC catalogs, lazy xarray + Dask loading, spectral indices, "
            "parametric payouts, and EUDR compliance pipelines."
        ),
        "level": "Advanced",
        "duration": "2h 30min",
        "icon": "🌍",
        "topics": [
            "STAC + pgstac",
            "xarray + Dask",
            "Spectral Indices",
            "Parametric Insurance",
        ],
        "sort_order": 60,
    },
    {
        "slug": "dao-governance",
        "title": "DAO Governance & Structure",
        "category": "Governance",
        "description": (
            "Token-based voting, proposal systems, treasury management — "
            "and when to graduate from Snapshot to a sovereign chain."
        ),
        "level": "Intermediate",
        "duration": "1h 15min",
        "icon": "🏛️",
        "topics": [
            "Token-based Voting",
            "Proposal Systems",
            "Treasury Management",
            "Community Rituals",
        ],
        "sort_order": 70,
    },
    {
        "slug": "defi-protocols",
        "title": "DeFi Protocols & Yield Farming",
        "category": "DeFi",
        "description": (
            "AMM design, liquidity provision, yield strategies, and the "
            "risk model behind a yield-powered treasury."
        ),
        "level": "Advanced",
        "duration": "2h",
        "icon": "💰",
        "topics": [
            "AMM Design",
            "Liquidity Mining",
            "Yield Strategies",
            "Risk & Covered Loans",
        ],
        "sort_order": 80,
    },
    {
        "slug": "web3-development",
        "title": "Web3 Frontend Development",
        "category": "Development",
        "description": (
            "Modern Web3 apps with SvelteKit + TypeScript, Web3Auth "
            "social login, WalletConnect, and the Cyberdyne component "
            "library."
        ),
        "level": "Intermediate",
        "duration": "2h 30min",
        "icon": "🌐",
        "topics": [
            "SvelteKit + TypeScript",
            "Web3Auth / WalletConnect",
            "IPFS + Provenance",
            "@cyberdynecorp/svelte-ui-core",
        ],
        "sort_order": 90,
    },
    {
        "slug": "tokenomics",
        "title": "Tokenomics & Economic Models",
        "category": "Economics",
        "description": (
            "Distribution, incentive design, and how to keep a token "
            "tied to real product value instead of speculation."
        ),
        "level": "Advanced",
        "duration": "1h 45min",
        "icon": "🎯",
        "topics": [
            "Token Distribution",
            "Incentive Design",
            "Inflation Models",
            "Value Accrual",
        ],
        "sort_order": 100,
    },
    {
        "slug": "cosmos-sdk",
        "title": "Cosmos SDK & IBC",
        "category": "Infrastructure",
        "description": (
            "Build sovereign chains with the Cosmos SDK, integrate IBC, "
            "and design governance modules built for throughput."
        ),
        "level": "Advanced",
        "duration": "3h",
        "icon": "🌌",
        "topics": [
            "Tendermint Consensus",
            "Module Development",
            "IBC Protocol",
            "Chain Governance",
        ],
        "sort_order": 110,
    },
    {
        "slug": "cybersecurity-web3",
        "title": "Web3 Security & Sandboxing",
        "category": "Security",
        "description": (
            "Smart-contract audits, wallet security, and sandboxing user "
            "code with real OS isolation — subprocess + netns + egress "
            "allowlist."
        ),
        "level": "Intermediate",
        "duration": "1h 30min",
        "icon": "🛡️",
        "topics": [
            "Contract Audits",
            "Wallet Security",
            "OS Sandboxing",
            "Bridge Vulnerabilities",
        ],
        "sort_order": 120,
    },
]


_PATHS: list[dict[str, object]] = [
    {
        "slug": "blockchain-developer",
        "title": "Blockchain Developer",
        "description": (
            "From cryptography fundamentals to shipping audited smart "
            "contracts on mainnet."
        ),
        "module_slugs": [
            "blockchain-basics",
            "smart-contracts",
            "web3-development",
            "cybersecurity-web3",
        ],
        "icon": "👨‍💻",
        "estimated_time": "8–12 weeks",
        "sort_order": 10,
    },
    {
        "slug": "cyberdyne-stack",
        "title": "Build Like Cyberdyne",
        "description": (
            "The exact architecture behind our production services — "
            "hexagonal cores, MCP backends, knowledge graphs."
        ),
        "module_slugs": [
            "hexagonal-architecture",
            "mcp-servers",
            "rag-knowledge-graphs",
            "cybersecurity-web3",
        ],
        "icon": "⚡",
        "estimated_time": "10–14 weeks",
        "sort_order": 20,
    },
    {
        "slug": "sovereign-ai",
        "title": "Sovereign Geospatial AI",
        "description": (
            "For teams building regulated geospatial software — DFIs, "
            "parametric insurers, EUDR compliance."
        ),
        "module_slugs": [
            "hexagonal-architecture",
            "mcp-servers",
            "geospatial-ai",
            "cybersecurity-web3",
        ],
        "icon": "🛰️",
        "estimated_time": "12–16 weeks",
        "sort_order": 30,
    },
    {
        "slug": "dao-operator",
        "title": "DAO Operator",
        "description": (
            "Design, deploy, and govern DAOs that pay their own bills "
            "via DeFi yield."
        ),
        "module_slugs": [
            "blockchain-basics",
            "dao-governance",
            "tokenomics",
            "defi-protocols",
        ],
        "icon": "🏛️",
        "estimated_time": "6–8 weeks",
        "sort_order": 40,
    },
    {
        "slug": "defi-specialist",
        "title": "DeFi Specialist",
        "description": (
            "Master AMMs, liquidity strategies, and yield farming — "
            "including the risk side most courses skip."
        ),
        "module_slugs": [
            "blockchain-basics",
            "smart-contracts",
            "defi-protocols",
            "tokenomics",
        ],
        "icon": "💎",
        "estimated_time": "10–14 weeks",
        "sort_order": 50,
    },
]


def upgrade() -> None:
    modules = op.create_table(
        "learning_modules",
        sa.Column("slug", sa.String(length=64), primary_key=True),
        sa.Column("title", sa.String(length=128), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("level", sa.String(length=32), nullable=False),
        sa.Column("duration", sa.String(length=32), nullable=False),
        sa.Column("icon", sa.String(length=16), nullable=False),
        sa.Column("topics", sa.JSON(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
    )

    paths = op.create_table(
        "learning_paths",
        sa.Column("slug", sa.String(length=64), primary_key=True),
        sa.Column("title", sa.String(length=128), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("module_slugs", sa.JSON(), nullable=False),
        sa.Column("estimated_time", sa.String(length=64), nullable=False),
        sa.Column("icon", sa.String(length=16), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
    )

    op.create_table(
        "enrollments",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("path_slug", sa.String(length=64), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="active"),
        sa.UniqueConstraint("user_id", "path_slug", name="uq_enrollment_user_path"),
    )
    op.create_index("ix_enrollments_user_id", "enrollments", ["user_id"])
    op.create_index("ix_enrollments_path_slug", "enrollments", ["path_slug"])

    op.create_table(
        "module_progress",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("module_slug", sa.String(length=64), nullable=False),
        sa.Column("percent", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("user_id", "module_slug", name="uq_progress_user_module"),
    )
    op.create_index("ix_module_progress_user_id", "module_progress", ["user_id"])

    op.create_table(
        "certificates",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("path_slug", sa.String(length=64), nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("verification_hash", sa.String(length=128), nullable=False),
        sa.Column("signed_payload", sa.Text(), nullable=False),
        sa.UniqueConstraint("user_id", "path_slug", name="uq_cert_user_path"),
    )
    op.create_index("ix_certificates_user_id", "certificates", ["user_id"])

    op.bulk_insert(modules, _MODULES)
    op.bulk_insert(paths, _PATHS)


def downgrade() -> None:
    op.drop_index("ix_certificates_user_id", table_name="certificates")
    op.drop_table("certificates")
    op.drop_index("ix_module_progress_user_id", table_name="module_progress")
    op.drop_table("module_progress")
    op.drop_index("ix_enrollments_path_slug", table_name="enrollments")
    op.drop_index("ix_enrollments_user_id", table_name="enrollments")
    op.drop_table("enrollments")
    op.drop_table("learning_paths")
    op.drop_table("learning_modules")
