# 使用官方 Python 3.12 运行时作为父镜像
FROM python:3.12
# 设置工作目录
WORKDIR /app
# 将当前目录内容复制到容器内的 WORKDIR
COPY . .
# 安装 pip 和 uv
RUN python3 -m ensurepip --upgrade
RUN pip install --no-cache-dir uv

# 使用 uv 安装依赖
RUN uv sync --reinstall
CMD [".venv/bin/python","-m","uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]