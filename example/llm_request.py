import os
import requests
from dotenv import load_dotenv

# .env ファイルを読み込む
load_dotenv()

# 環境変数の取得
API_KEY = os.getenv("LLM_SERVICE_API_KEY")
API_BASE = os.getenv("LLM_SERVICE_API_BASE")
MODEL = os.getenv("LLM_SERVICE_MODEL")

# API のエンドポイント設定
url = f"{API_BASE}/v1/chat/completions"

# リクエストデータ
payload = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "簡潔に自己紹介して"}
    ]
}

# ヘッダー設定
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# API コール
response = requests.post(url, headers=headers, json=payload)

# レスポンス出力
if response.status_code == 200:
    data = response.json()
    print("=== API Response ===")
    print(data["choices"][0]["message"]["content"])
else:
    print(f"Error: {response.status_code}")
    print(response.text)
