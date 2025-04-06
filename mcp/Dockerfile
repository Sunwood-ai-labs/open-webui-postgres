FROM python:3.11-slim

# 必要なツールをインストール
RUN apt-get update && \
    apt-get install -y curl wget

# Node.jsとnpmをインストール
RUN apt-get install -y nodejs npm

# n（Node.jsバージョンマネージャ）をインストールして最新版に更新
RUN npm install -g n && \
    n latest

# unzipをインストール
RUN apt-get install -y unzip

# aptキャッシュをクリーンアップ
RUN rm -rf /var/lib/apt/lists/*

# mcpoをインストール
RUN pip install mcpo

# mcpのNode.jsモジュールをグローバルにインストール
RUN npm install -g @modelcontextprotocol/server-memory
RUN npm install -g @modelcontextprotocol/sdk

RUN pip install uv

WORKDIR /app/mcp

# ポート8000を公開
EXPOSE 8000

# mcpoを実行（コメントアウトされています）
# CMD ["mcpo", "--port", "8000", "--config", "/app/mcp/settings.json"]
