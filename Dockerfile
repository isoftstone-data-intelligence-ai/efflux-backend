# 使用官方 Python 3.12 运行时作为父镜像
FROM python:3.12
# 设置工作目录
WORKDIR /app
# 将当前目录内容复制到容器内的 WORKDIR
COPY . .
# 创建虚拟环境（如果需要）
RUN python3 -m venv .venv
# 激活虚拟环境并安装依赖
RUN ./.venv/bin/python -m pip install --upgrade pip
RUN ./.venv/bin/pip install uv
# 使用 uv 安装依赖
RUN ./.venv/bin/uv sync --reinstall
# 确保你的应用可以通过命令行启动
# CMD ["nohup", "python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "&>", "~/app/app.log", "&"]
# 注意：直接在CMD中使用nohup可能会导致问题，建议通过一个启动脚本来处理后台运行和日志重定向。
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh
CMD ["/app/start.sh"]