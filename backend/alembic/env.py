"""Alembic env — wires migrations against the same engine as the app."""

from __future__ import annotations

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from cyberdyne_backend.infrastructure.database.base import Base
from cyberdyne_backend.infrastructure.settings import get_settings

# Import every package that defines SQLAlchemy models so they register
# against Base.metadata before autogenerate runs. Add new modules here
# when new bounded contexts ship persistence adapters.
from cyberdyne_backend.adapters.outbound.persistence.blog import (  # noqa: F401
    models as _blog_models,
)
from cyberdyne_backend.adapters.outbound.persistence.content import (  # noqa: F401
    models as _content_models,
)
from cyberdyne_backend.adapters.outbound.persistence.courses import (  # noqa: F401
    models as _courses_models,
)
from cyberdyne_backend.adapters.outbound.persistence.leads import (  # noqa: F401
    models as _leads_models,
)
from cyberdyne_backend.adapters.outbound.persistence.uploads import (  # noqa: F401
    models as _uploads_models,
)
from cyberdyne_backend.adapters.outbound.persistence.learning import (  # noqa: F401
    models as _learning_models,
)
from cyberdyne_backend.adapters.outbound.persistence.quizzes import (  # noqa: F401
    models as _quizzes_models,
)
from cyberdyne_backend.adapters.outbound.persistence.marketplace import (  # noqa: F401
    models as _marketplace_models,
)
from cyberdyne_backend.adapters.outbound.persistence.ai_chat import (  # noqa: F401
    models as _ai_chat_models,
)
from cyberdyne_backend.adapters.outbound.persistence.academy import (  # noqa: F401
    models as _academy_models,
)
from cyberdyne_backend.adapters.outbound.persistence.concepts import (  # noqa: F401
    models as _concepts_models,
)

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _get_url() -> str:
    return get_settings().database_url


def run_migrations_offline() -> None:
    context.configure(
        url=_get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    config.set_main_option("sqlalchemy.url", _get_url())
    engine = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
