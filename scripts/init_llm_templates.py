import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from model.llm_template import LlmTemplate

# 加载环境变量
load_dotenv()

# 构建数据库连接 URL
DATABASE_URL = (
    f"postgresql://{os.environ['DATABASE_USERNAME']}:{os.environ['DATABASE_PASSWORD']}"
    f"@{os.environ['DATABASE_HOST']}:{os.environ['DATABASE_PORT']}/{os.environ['DATABASE_NAME']}"
)

# 创建引擎和会话
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# 定义模板数据
TEMPLATES = [
    {
        "provider": "Deepseek",
        "model_display_name": "deepseek-r1",
        "api_key_variable": "API Key",
        "base_url_variable": "Base URL",
        "model_variable": "Model",
    },
    {
        "provider": "Open AI",
        "model_display_name": "gpt-4o",
        "api_key_variable": "API Key",
        "base_url_variable": "Base URL",
        "model_variable": "Model",
    },
    {
        "provider": "Claude",
        "model_display_name": "claude-3.5-sonnet",
        "api_key_variable": "API Key",
        "base_url_variable": "Base URL",
        "model_variable": "Model",
    },
    {
        "provider": "Azure",
        "model_display_name": "gpt-4o",
        "api_key_variable": "API Key",
        "base_url_variable": "Endpoint",
        "model_variable": "API Version",
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

def init_templates():
    """初始化 LLM 模板数据"""
    session = Session()
    try:
        # 检查是否已存在数据
        if session.query(LlmTemplate).first():
            print("模板数据已存在，跳过初始化...")
            return

        # 插入模板数据
        for template_data in TEMPLATES:
            template = LlmTemplate(**template_data)
            session.add(template)
        
        session.commit()
        print("成功初始化 LLM 模板数据！")
    except Exception as e:
        session.rollback()
        print(f"初始化模板时出错: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    init_templates() 