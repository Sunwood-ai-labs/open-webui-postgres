FROM python:3.11-slim

# 必要なツールとNode.js、UVをインストール
RUN apt-get update && \
    apt-get install -y curl wget nodejs npm unzip && \
    npm install -g n && \
    n latest && \
    curl -fsSL https://github.com/astro/uvx/releases/download/v0.2.0/uvx-linux-x64.zip -o uvx.zip && \
    unzip uvx.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/uvx && \
    rm uvx.zip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# mcpoをインストール
RUN pip install mcpo

WORKDIR /app/mcp

# ポート8000を公開
EXPOSE 8000

# mcpoを実行
CMD ["mcpo", "--port", "8000", "--config", "/app/mcp/settings.json"]
