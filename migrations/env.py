from asyncio import run as aiorun
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

ctx_config = context.config

if ctx_config.config_file_name is not None:
    fileConfig(ctx_config.config_file_name)

from cryolvix.database.models import *
target_metadata = Base.metadata
print(Base.metadata.tables.keys())

def run_migrations_offline() -> None:
    url = ctx_config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    connectable = create_async_engine(
        ctx_config.get_main_option("sqlalchemy.url"), # type: ignore
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    aiorun(run_migrations_online())
