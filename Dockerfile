# 使用官方 Python 3.12 运行时作为父镜像
FROM python:3.12
# 设置工作目录
WORKDIR /app
# 将当前目录内容复制到容器内的 WORKDIR
COPY . .
# 安装 pip 和 uv
RUN python3 -m ensurepip --upgrade
RUN pip install --no-cache-dir uv

# 创建虚拟环境（如果需要）
RUN python3 -m venv .venv
# 激活虚拟环境并安装依赖
RUN ./.venv/bin/python -m pip install --upgrade pip
RUN ./.venv/bin/pip install uv
RUN ./.venv/bin/pip install uvicorn
# 使用 uv 安装依赖
RUN ./.venv/bin/uv sync --reinstall
CMD ["./.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]