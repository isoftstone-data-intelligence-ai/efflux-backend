import os
import sys
import asyncio

# 将项目根目录添加到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from dotenv import load_dotenv
from model.llm_template import LlmTemplate

# 加载环境变量
load_dotenv()

# 构建数据库连接 URL（使用 asyncpg）
DATABASE_URL = (
    f"postgresql+asyncpg://{os.environ['DATABASE_USERNAME']}:{os.environ['DATABASE_PASSWORD']}"
    f"@{os.environ['DATABASE_HOST']}:{os.environ['DATABASE_PORT']}/{os.environ['DATABASE_NAME']}"
)

# 创建异步引擎和会话
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# 定义模板数据
TEMPLATES = [
    {
        "provider": "Azure",
        "model_display_name": "gpt-4o",
        "api_key_variable": "API Key",
        "base_url_variable": "Endpoint",
        "model_variable": "API Version",
    },
    {
        "provider": "Open AI",
        "model_display_name": "gpt-4o",
        "api_key_variable": "API Key",
        "base_url_variable": "Base URL",
        "model_variable": "Model",
    },
    {
        "provider": "Anthropic",
        "model_display_name": "claude-3.5-sonnet",
        "api_key_variable": "API Key",
        "base_url_variable": "Base URL",
        "model_variable": "Model",
    },
    {
        "provider": "Deepseek",
        "model_display_name": "deepseek-r1",
        "api_key_variable": "API Key",
        "base_url_variable": "Base URL",
        "model_variable": "Model",
    },
    {
        "provider": "Ollama",
        "model_display_name": "deepseek-r1:8b",
        "api_key_variable": "API Key",
        "base_url_variable": "Base URL",
        "model_variable": "Model",
    },
    {
        "provider": "阿里",
        "model_display_name": "qwen-max",
        "api_key_variable": "API Key",
        "base_url_variable": "Base URL",
        "model_variable": "Model",
    },
    {
        "provider": "字节跳动",
        "model_display_name": "doubao-pro",
        "api_key_variable": "API Key",
        "base_url_variable": "Base URL",
        "model_variable": "Model",
    },
    {
        "provider": "Moonshot",
        "model_display_name": "moonshot-v1",
        "api_key_variable": "API Key",
        "base_url_variable": "Base URL",
        "model_variable": "Model",
    },
]

async def init_templates():
    """初始化 LLM 模板数据"""
    async with AsyncSessionLocal() as session:
        try:
            # 检查是否已存在数据
            result = await session.execute(select(LlmTemplate))
            if result.scalar_one_or_none():
                print("模板数据已存在，跳过初始化...")
                return

            # 插入模板数据
            for template_data in TEMPLATES:
                template = LlmTemplate(**template_data)
                session.add(template)
            
            await session.commit()
            print("成功初始化 LLM 模板数据！")
        except Exception as e:
            await session.rollback()
            print(f"初始化模板时出错: {e}")
            raise

async def main():
    try:
        await init_templates()
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main()) 