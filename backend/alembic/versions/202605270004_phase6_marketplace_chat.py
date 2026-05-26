"""Phase 6 — marketplace + Stripe + AI chat tables.

Seeds the product catalogue from ``frontend/src/lib/data/shop.ts``.
Service-type products have no Stripe price id (they route to lead
capture); training + license products carry a placeholder
``stripe_price_id`` — replace with real Stripe price ids before the
first paid order. The frontend already filters out non-purchasable
products gracefully.

Revision ID: 202605270004
Revises: 202605270003
Create Date: 2026-05-27 00:03:00
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202605270004"
down_revision: str | Sequence[str] | None = "202605270003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


_SERVICE_DEFAULTS: list[dict[str, object]] = [
    {
        "slug": "frontend-webapp",
        "title": "Custom Web Application",
        "description_md": (
            "Full-stack web application development with modern React/Svelte "
            "frontend, responsive design, and seamless user experience."
        ),
        "price_cents": 500000,
        "duration_label": "4-8 weeks",
        "features": [
            "React/Svelte/Vue",
            "Responsive Design",
            "TypeScript",
            "Tailwind CSS",
            "Component Library",
        ],
        "category": "Services",
        "subcategory": "Frontend",
        "popular": True,
        "sort_order": 10,
    },
    {
        "slug": "frontend-dapp",
        "title": "Web3 dApp Frontend",
        "description_md": (
            "Modern decentralized application frontend with wallet integration, "
            "smart contract interaction, and Web3 UX patterns."
        ),
        "price_cents": 750000,
        "duration_label": "6-10 weeks",
        "features": [
            "Wallet Integration",
            "Smart Contract UI",
            "Web3 Libraries",
            "IPFS Storage",
            "MetaMask Support",
        ],
        "category": "Services",
        "subcategory": "Frontend",
        "popular": True,
        "sort_order": 20,
    },
    {
        "slug": "frontend-dashboard",
        "title": "Analytics Dashboard",
        "description_md": (
            "Custom analytics dashboard with real-time data visualization, "
            "charts, and comprehensive reporting features."
        ),
        "price_cents": 400000,
        "duration_label": "3-6 weeks",
        "features": [
            "Chart.js/D3.js",
            "Real-time Updates",
            "Data Export",
            "Custom Widgets",
            "Mobile Responsive",
        ],
        "category": "Services",
        "subcategory": "Frontend",
        "sort_order": 30,
    },
    {
        "slug": "backend-api",
        "title": "REST API Development",
        "description_md": (
            "Scalable REST API with authentication, database integration, "
            "and comprehensive documentation."
        ),
        "price_cents": 600000,
        "duration_label": "4-8 weeks",
        "features": [
            "Node.js/Python",
            "Database Design",
            "Authentication",
            "API Documentation",
            "Testing Suite",
        ],
        "category": "Services",
        "subcategory": "Backend",
        "popular": True,
        "sort_order": 40,
    },
    {
        "slug": "backend-blockchain",
        "title": "Blockchain Backend",
        "description_md": (
            "Custom blockchain integration with smart contract deployment, "
            "indexing, and Web3 infrastructure."
        ),
        "price_cents": 850000,
        "duration_label": "6-12 weeks",
        "features": [
            "Smart Contracts",
            "Web3 Integration",
            "Blockchain Indexing",
            "IPFS Backend",
            "Event Listeners",
        ],
        "category": "Services",
        "subcategory": "Backend",
        "popular": True,
        "sort_order": 50,
    },
    {
        "slug": "backend-microservices",
        "title": "Microservices Architecture",
        "description_md": (
            "Scalable microservices architecture with containerization, "
            "load balancing, and monitoring."
        ),
        "price_cents": 1200000,
        "duration_label": "8-16 weeks",
        "features": [
            "Docker/Kubernetes",
            "Service Mesh",
            "Load Balancing",
            "Monitoring",
            "CI/CD Pipeline",
        ],
        "category": "Services",
        "subcategory": "Backend",
        "sort_order": 60,
    },
]


_TRAINING_DEFAULTS: list[dict[str, object]] = [
    {
        "slug": "training-web3-basics",
        "title": "Web3 Development Fundamentals",
        "description_md": (
            "Comprehensive course covering blockchain basics, smart contracts, "
            "and dApp development from scratch."
        ),
        "price_cents": 29900,
        "duration_label": "40 hours",
        "features": [
            "Video Lectures",
            "Hands-on Projects",
            "Code Examples",
            "Certificate",
            "Community Access",
        ],
        "category": "Training Material",
        "popular": True,
        "linked_learning_path_slug": "blockchain-developer",
        "stripe_price_id": "price_placeholder_training_web3_basics",
        "sort_order": 100,
    },
    {
        "slug": "training-solidity-advanced",
        "title": "Advanced Solidity Programming",
        "description_md": (
            "Deep dive into Solidity optimization, security patterns, and "
            "complex smart contract architecture."
        ),
        "price_cents": 39900,
        "duration_label": "60 hours",
        "features": [
            "Advanced Patterns",
            "Security Auditing",
            "Gas Optimization",
            "Testing Frameworks",
            "Real Projects",
        ],
        "category": "Training Material",
        "popular": True,
        "linked_learning_path_slug": "blockchain-developer",
        "stripe_price_id": "price_placeholder_training_solidity_advanced",
        "sort_order": 110,
    },
    {
        "slug": "training-defi-protocols",
        "title": "DeFi Protocol Development",
        "description_md": (
            "Learn to build DeFi protocols including AMMs, lending platforms, "
            "and yield farming contracts."
        ),
        "price_cents": 49900,
        "duration_label": "80 hours",
        "features": [
            "AMM Development",
            "Lending Protocols",
            "Yield Strategies",
            "Tokenomics",
            "Live Deployment",
        ],
        "category": "Training Material",
        "linked_learning_path_slug": "defi-specialist",
        "stripe_price_id": "price_placeholder_training_defi_protocols",
        "sort_order": 120,
    },
    {
        "slug": "training-dao-governance",
        "title": "DAO Governance & Operations",
        "description_md": (
            "Complete guide to DAO creation, governance mechanisms, and "
            "community management strategies."
        ),
        "price_cents": 34900,
        "duration_label": "50 hours",
        "features": [
            "Governance Design",
            "Token Models",
            "Voting Systems",
            "Treasury Management",
            "Case Studies",
        ],
        "category": "Training Material",
        "linked_learning_path_slug": "dao-operator",
        "stripe_price_id": "price_placeholder_training_dao_governance",
        "sort_order": 130,
    },
]


_LICENSE_DEFAULTS: list[dict[str, object]] = [
    {
        "slug": "license-trade4me",
        "title": "Trade4Me License",
        "description_md": (
            "Advanced algorithmic trading platform with AI-powered market "
            "analysis and automated execution strategies."
        ),
        "price_cents": 249900,
        "duration_label": "1 year",
        "features": [
            "AI Trading Algorithms",
            "Market Analysis",
            "Risk Management",
            "Portfolio Optimization",
            "API Access",
        ],
        "category": "Licenses",
        "popular": True,
        "stripe_price_id": "price_placeholder_license_trade4me",
        "sort_order": 200,
    },
    {
        "slug": "license-liquidity4me",
        "title": "Liquidity4Me License",
        "description_md": (
            "DeFi liquidity management platform with yield optimization, "
            "impermanent loss protection, and automated rebalancing."
        ),
        "price_cents": 199900,
        "duration_label": "1 year",
        "features": [
            "Yield Optimization",
            "LP Management",
            "Risk Analysis",
            "Auto-rebalancing",
            "Multi-chain Support",
        ],
        "category": "Licenses",
        "popular": True,
        "stripe_price_id": "price_placeholder_license_liquidity4me",
        "sort_order": 210,
    },
    {
        "slug": "license-study4me",
        "title": "Study4Me License",
        "description_md": (
            "AI-powered learning platform with personalized curricula, progress "
            "tracking, and skill assessment for Web3 education."
        ),
        "price_cents": 79900,
        "duration_label": "1 year",
        "features": [
            "Personalized Learning",
            "Progress Tracking",
            "Skill Assessment",
            "Certification",
            "Mentor Access",
        ],
        "category": "Licenses",
        "status": "beta",
        "stripe_price_id": "price_placeholder_license_study4me",
        "sort_order": 220,
    },
    {
        "slug": "license-surf4me",
        "title": "Surf4Me License",
        "description_md": (
            "Intelligent Web3 navigation and discovery platform with curated "
            "content, trend analysis, and research tools."
        ),
        "price_cents": 59900,
        "duration_label": "1 year",
        "features": [
            "Content Curation",
            "Trend Analysis",
            "Research Tools",
            "Bookmark Management",
            "Team Collaboration",
        ],
        "category": "Licenses",
        "status": "coming_soon",
        "stripe_price_id": "price_placeholder_license_surf4me",
        "sort_order": 230,
    },
]


def _finalize_seed(rows: list[dict[str, object]], product_type: str) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for r in rows:
        merged: dict[str, object] = {
            "type": product_type,
            "currency": "USD",
            "subcategory": None,
            "image_url": "",
            "popular": False,
            "status": "available",
            "stripe_price_id": None,
            "linked_learning_path_slug": None,
        }
        merged.update(r)
        out.append(merged)
    return out


def upgrade() -> None:
    products = op.create_table(
        "marketplace_products",
        sa.Column("slug", sa.String(length=64), primary_key=True),
        sa.Column("type", sa.String(length=16), nullable=False),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column("description_md", sa.Text(), nullable=False),
        sa.Column("price_cents", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("currency", sa.String(length=8), nullable=False, server_default="USD"),
        sa.Column("duration_label", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("features", sa.JSON(), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("subcategory", sa.String(length=64), nullable=True),
        sa.Column("image_url", sa.String(length=512), nullable=False, server_default=""),
        sa.Column("popular", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="available"),
        sa.Column("stripe_price_id", sa.String(length=64), nullable=True),
        sa.Column("linked_learning_path_slug", sa.String(length=64), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_marketplace_products_type", "marketplace_products", ["type"])
    op.create_index("ix_marketplace_products_category", "marketplace_products", ["category"])

    op.create_table(
        "marketplace_orders",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("product_slug", sa.String(length=64), nullable=False),
        sa.Column("amount_cents", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(length=8), nullable=False),
        sa.Column(
            "stripe_checkout_session_id",
            sa.String(length=128),
            nullable=False,
            unique=True,
        ),
        sa.Column("stripe_payment_intent_id", sa.String(length=128), nullable=True),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_marketplace_orders_user_id", "marketplace_orders", ["user_id"])
    op.create_index(
        "ix_marketplace_orders_product_slug", "marketplace_orders", ["product_slug"]
    )
    op.create_index(
        "ix_marketplace_orders_session_id",
        "marketplace_orders",
        ["stripe_checkout_session_id"],
    )
    op.create_index(
        "ix_marketplace_orders_payment_intent",
        "marketplace_orders",
        ["stripe_payment_intent_id"],
    )

    op.create_table(
        "marketplace_licenses",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("order_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("product_slug", sa.String(length=64), nullable=False),
        sa.Column("key_hash", sa.String(length=128), nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_marketplace_licenses_user_id", "marketplace_licenses", ["user_id"])
    op.create_index("ix_marketplace_licenses_order_id", "marketplace_licenses", ["order_id"])

    op.create_table(
        "stripe_webhook_events",
        sa.Column("stripe_event_id", sa.String(length=128), primary_key=True),
        sa.Column("type", sa.String(length=64), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "chat_sessions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_message_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_chat_sessions_user_id", "chat_sessions", ["user_id"])

    op.create_table(
        "chat_messages",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("session_id", sa.Uuid(), nullable=False),
        sa.Column("role", sa.String(length=16), nullable=False),
        sa.Column("content", sa.Text(), nullable=False, server_default=""),
        sa.Column("tool_calls", sa.JSON(), nullable=False),
        sa.Column("tool_call_id", sa.String(length=64), nullable=True),
        sa.Column("tokens_in", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("tokens_out", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("model", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_chat_messages_session_id", "chat_messages", ["session_id"])
    op.create_index("ix_chat_messages_created_at", "chat_messages", ["created_at"])

    seed = (
        _finalize_seed(_SERVICE_DEFAULTS, "service")
        + _finalize_seed(_TRAINING_DEFAULTS, "training")
        + _finalize_seed(_LICENSE_DEFAULTS, "license")
    )
    op.bulk_insert(products, seed)


def downgrade() -> None:
    op.drop_index("ix_chat_messages_created_at", table_name="chat_messages")
    op.drop_index("ix_chat_messages_session_id", table_name="chat_messages")
    op.drop_table("chat_messages")
    op.drop_index("ix_chat_sessions_user_id", table_name="chat_sessions")
    op.drop_table("chat_sessions")
    op.drop_table("stripe_webhook_events")
    op.drop_index("ix_marketplace_licenses_order_id", table_name="marketplace_licenses")
    op.drop_index("ix_marketplace_licenses_user_id", table_name="marketplace_licenses")
    op.drop_table("marketplace_licenses")
    op.drop_index("ix_marketplace_orders_payment_intent", table_name="marketplace_orders")
    op.drop_index("ix_marketplace_orders_session_id", table_name="marketplace_orders")
    op.drop_index("ix_marketplace_orders_product_slug", table_name="marketplace_orders")
    op.drop_index("ix_marketplace_orders_user_id", table_name="marketplace_orders")
    op.drop_table("marketplace_orders")
    op.drop_index("ix_marketplace_products_category", table_name="marketplace_products")
    op.drop_index("ix_marketplace_products_type", table_name="marketplace_products")
    op.drop_table("marketplace_products")
