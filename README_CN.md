

<div align="center">
    <h1>Efflux - Backend</h1>
    <p>LLM Agent 智能体对话客户端后端</p>
    <p>
        <a href="LICENSE">
            <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
        </a>
        <a href="https://www.python.org/downloads/">
            <img src="https://img.shields.io/badge/Python-3.12+-blue.svg" alt="Python">
        </a>
        <a href="https://fastapi.tiangolo.com/">
            <img src="https://img.shields.io/badge/FastAPI-0.115.6+-brightgreen.svg" alt="FastAPI">
        </a>
        <a href="https://modelcontextprotocol.io/">
            <img src="https://img.shields.io/badge/MCP-1.1.1-coral.svg" alt="MCP">
        </a>
    </p>
    <p>
        <a href="./README.md">English</a> | <b>简体中文</b>
    </p>
    <br/>
</div>


Efflux 是一个基于大语言模型的 Agent 智能体对话客户端，提供流式会话响应和完整的对话历史管理。通过集成 MCP 协议，系统可作为 MCP Host 连接不同的 MCP Servers，为模型提供标准化的工具调用和数据访问能力。





### 主要特性
- 快速构建 Agent 智能体
- MCP 工具动态加载与调用
- 支持多种大语言模型接入
- 实时流式对话响应
- 会话历史记录管理





### 在线演示
您可以通过访问我们的[在线演示](http://47.236.204.213:3000/login)来体验Efflux的功能。



### 环境要求
- Python 3.12+
- PostgreSQL
- uv 包和项目管理工具，可通过`pip install uv`安装

### 快速开始

1. 克隆项目
```bash
git clone git@github.com:isoftstone-data-intelligence-ai/efflux-backend.git
cd efflux-backend
```

2. 安装 uv
```bash
pip install uv
```

3. 重载依赖项
```bash
uv sync --reinstall
```

4. 激活虚拟环境
```bash
# 激活虚拟环境
source .venv/bin/activate   # MacOS/Linux

# 退出虚拟环境（当需要时）
deactivate
```

5. 配置环境变量
```bash
# 复制环境变量模板
cp .env.sample .env

# 编辑 .env 文件，需要配置：
# 1. 数据库连接信息（DATABASE_NAME、DATABASE_USERNAME、DATABASE_PASSWORD）
# 2. 至少一个大语言模型的配置（如 Azure OpenAI、通义千问、豆包或月之暗面）
```

6. 选择使用的大模型
```bash
# 编辑 core/common/container.py 文件
# 找到 llm 的注册部分，根据需要替换为以下任一模型（默认使用通义千问）：
# - QwenLlm：通义千问
# - AzureLlm：Azure OpenAI
# - DoubaoLlm：豆包
# - MoonshotLlm：月之暗面

# 示例：使用 Azure OpenAI
from core.llm.azure_open_ai import AzureLlm
# ...
llm = providers.Singleton(AzureLlm)
```

7. 启动 postgres 数据库
```bash
# 方法一：如果你本地已安装 PostgreSQL
# 直接启动本地的 PostgreSQL 服务即可

# 方法二：使用 Docker 启动（示例）
docker run -d --name local-postgres \
    -e POSTGRES_DB=your_database_name \
    -e POSTGRES_USER=your_username \
    -e POSTGRES_PASSWORD=your_password \
    -p 5432:5432 \
    postgres

# 注意：无论使用哪种方式，请确保数据库的连接信息与 .env 文件中的配置保持一致
```

8. 初始化数据库
```bash
# 创建一个新的版本，并在alembic/versions下创建一个修改数据结构版本的py文件
alembic revision --autogenerate -m "initial migration"

# 预览将要执行的 SQL：
alembic upgrade head --sql

# 如果预览没有问题，执行迁移
alembic upgrade head
```

9. 初始化 LLM 模板数据
```bash
# 运行初始化脚本
python scripts/init_llm_templates.py
```

10. 启动服务
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```


### 致谢 

本项目使用了以下优秀的开源项目和技术：

- [@modelcontextprotocol/mcp](https://modelcontextprotocol.io) - 标准化的 LLM 数据交互开放协议
- [@langchain-ai/langchain](https://github.com/langchain-ai/langchain) - LLM 应用开发框架
- [@sqlalchemy/sqlalchemy](https://github.com/sqlalchemy/sqlalchemy) - Python SQL 工具包和 ORM 框架
- [@pydantic/pydantic](https://github.com/pydantic/pydantic) - 数据验证和设置管理
- [@tiangolo/fastapi](https://github.com/tiangolo/fastapi) - 现代、快速的 Web 框架
- [@aio-libs/aiohttp](https://github.com/aio-libs/aiohttp) - 异步 HTTP 客户端/服务器框架
- [@sqlalchemy/alembic](https://github.com/sqlalchemy/alembic) - SQLAlchemy 的数据库迁移工具
- [@astral-sh/uv](https://github.com/astral-sh/uv) - 极速 Python 包管理器
- [@python-colorlog/colorlog](https://github.com/python-colorlog/colorlog) - 彩色日志输出工具
- [@jlowin/fastmcp](https://github.com/jlowin/fastmcp) - 快速构建 MCP 服务器的 Python 框架
- [@langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) - 构建状态化多智能体 LLM 应用的框架

感谢这些项目的开发者和维护者为开源社区做出的贡献。



