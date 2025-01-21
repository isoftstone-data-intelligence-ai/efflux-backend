<div align="center">
    <h1>Efflux - Backend</h1>
    <p>LLM Agent Chat Client Backend</p>
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
        <b>English</b> | <a href="./README_CN.md">简体中文</a>
    </p>
    <br/>
</div>

Efflux is an LLM-based Agent chat client featuring streaming responses and chat history management. As an MCP Host, it leverages the Model Context Protocol to connect with various MCP Servers, enabling standardized tool invocation and data access for large language models.

### Key Features
- Rapid Agent construction
- Dynamic MCP tool loading and invocation
- Support for multiple large language models
- Real-time streaming chat responses
- Chat history management

### Requirements
- Python 3.12+
- PostgreSQL
- uv (Python package & environment manager), installable via `pip install uv`

### Quick Start

1. Clone the project
```bash
git clone git@github.com:isoftstone-data-intelligence-ai/efflux-backend.git
cd efflux-backend
```

2. Install uv
```bash
pip install uv
```

3. Reload dependencies
```bash
uv sync --reinstall
```

4. Configure environment variables
```bash
# Copy environment variable template
cp .env.sample .env

# Edit .env file, configure:
# 1. Database connection info (DATABASE_NAME, DATABASE_USERNAME, DATABASE_PASSWORD)
# 2. At least one LLM configuration (e.g., Azure OpenAI, Qwen, Doubao, or Moonshot)
```

5. Select the LLM
```bash
# Edit core/common/container.py file
# Find the llm registration section, replace with any of the following models (Qwen by default):
# - QwenLlm: Qwen
# - AzureLlm: Azure OpenAI
# - DoubaoLlm: Doubao
# - MoonshotLlm: Moonshot

# Example: Using Azure OpenAI
from core.llm.azure_open_ai import AzureLlm
# ...
llm = providers.Singleton(AzureLlm)
```

6. Start PostgreSQL database
```bash
# Method 1: If PostgreSQL is installed locally
# Simply start your local PostgreSQL service

# Method 2: Using Docker (example)
docker run -d --name local-postgres \
    -e POSTGRES_DB=your_database_name \
    -e POSTGRES_USER=your_username \
    -e POSTGRES_PASSWORD=your_password \
    -p 5432:5432 \
    postgres

# Note: Ensure database connection info matches the configuration in your .env file
```

7. Initialize database
```bash
# Create a new version and generate a migration file in alembic/versions
alembic revision --autogenerate -m "initial migration"

# Preview SQL to be executed:
alembic upgrade head --sql

# If preview looks good, execute migration
alembic upgrade head
```

8. Start the service
```bash
# Start service using Python from project virtual environment
$(pwd)/.venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Acknowledgments

This project utilizes the following excellent open-source projects and technologies:

- [@modelcontextprotocol/mcp](https://modelcontextprotocol.io) - Standardized open protocol for LLM data interaction
- [@langchain-ai/langchain](https://github.com/langchain-ai/langchain) - LLM application development framework
- [@sqlalchemy/sqlalchemy](https://github.com/sqlalchemy/sqlalchemy) - Python SQL toolkit and ORM framework
- [@pydantic/pydantic](https://github.com/pydantic/pydantic) - Data validation and settings management
- [@tiangolo/fastapi](https://github.com/tiangolo/fastapi) - Modern, fast web framework
- [@aio-libs/aiohttp](https://github.com/aio-libs/aiohttp) - Async HTTP client/server framework
- [@sqlalchemy/alembic](https://github.com/sqlalchemy/alembic) - Database migration tool for SQLAlchemy
- [@astral-sh/uv](https://github.com/astral-sh/uv) - Ultra-fast Python package manager
- [@python-colorlog/colorlog](https://github.com/python-colorlog/colorlog) - Colored log output tool
- [@jlowin/fastmcp](https://github.com/jlowin/fastmcp) - Python framework for building MCP servers
- [@langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) - Framework for building stateful multi-agent LLM applications

Thanks to the developers and maintainers of these projects for their contributions to the open-source community.
