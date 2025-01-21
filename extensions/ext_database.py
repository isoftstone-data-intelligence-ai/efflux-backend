from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dependency_injector.providers import Singleton
import os
from dotenv import load_dotenv
# 加载环境变量
load_dotenv()

# 从环境变量构建连接字符串
DATABASE_URL = (
    f"postgresql+asyncpg://{os.environ['DATABASE_USERNAME']}:{os.environ['DATABASE_PASSWORD']}"
    f"@{os.environ['DATABASE_HOST']}:{os.environ['DATABASE_PORT']}/{os.environ['DATABASE_NAME']}"
)

# # 数据库连接字符串（根据实际情况替换 user, password, host, database）
# DATABASE_URL = "postgresql+asyncpg://admin:123456@localhost:5432/efflux"


# 创建 SQLAlchemy Async Engine
engine = create_async_engine(DATABASE_URL, future=True, echo=False)

# 创建 Async Session 工厂
async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

# 用作依赖注入的单例 Session
class DatabaseProvider(Singleton):
    session_factory = async_session_factory