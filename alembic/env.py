from logging.config import fileConfig

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
import os
from dotenv import load_dotenv

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 加载环境变量
load_dotenv()

# 从环境变量构建连接字符串
DATABASE_URL = (
    f"postgresql+asyncpg://{os.environ['DATABASE_USERNAME']}:{os.environ['DATABASE_PASSWORD']}"
    f"@{os.environ['DATABASE_HOST']}:{os.environ['DATABASE_PORT']}/{os.environ['DATABASE_NAME']}"
)

print(DATABASE_URL)

# Configure the URL of the database
config.set_main_option('sqlalchemy.url', DATABASE_URL)

from extensions.ext_database import Base, engine
from model.user import User
from model.mcp_server import McpServer
from model.chat_window import ChatWindow
from model.llm_config import LlmConfig
from model.llm_template import LlmTemplate

target_metadata = Base.metadata

def run_migrations_offline() -> None:

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def debug_transaction(sync_connection):
    context.configure(
        connection=sync_connection,
        target_metadata=target_metadata,
        transactional_ddl=True
    )
    print("Configured context")
    context.run_migrations()
    print("Migrations executed")

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(
            lambda sync_connection: context.configure(
                connection=sync_connection,
                target_metadata=target_metadata,
                compare_type=True,  # 检查字段类型的变化
                transactional_ddl=True  # 确保事务性 DDL
            )
        )

        async with connection.begin() as trans:
            try:
                await connection.run_sync(lambda sync_connection: context.run_migrations())
                await trans.commit()  # 明确提交事务
            except Exception:
                await trans.rollback()  # 出现问题回滚事务
                raise

def run_migrations() -> None:
    """Run the migrations in an async way."""
    asyncio.run(run_migrations_online())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations()
