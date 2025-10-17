# 使用 Python 3.11 作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# 安装 uv (Python 包管理器)
RUN pip install uv -i https://mirrors.aliyun.com/pypi/simple/

# 复制项目代码
COPY . .

# 重新生成 uv.lock 文件
RUN rm -rf uv.lock && uv lock

# 安装项目依赖
RUN uv sync --frozen

# 创建数据目录
RUN mkdir -p data log

# 设置权限
RUN chmod +x /app/main.py

# 设置默认命令
CMD ["uv", "run", "python", "main.py", "--mode", "service"]