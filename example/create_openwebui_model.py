import os
import json
import requests
from dotenv import load_dotenv

# === .env 読み込み ===
load_dotenv()

API_KEY = os.getenv("LLM_SERVICE_API_KEY")
API_BASE = os.getenv("LLM_SERVICE_API_BASE")

url = f"{API_BASE}/v1/models/create"

payload = {
    "id": "example-model-003",
    "base_model_id": "openai/gpt-4o-mini",
    "name": "My Custom Model",
    "meta": {
        "description": "Model created via OpenWebUI API script.",
        "profile_image_url": "https://api.dicebear.com/7.x/bottts/png?seed=OpenWebUI-1stModel",
        "capabilities": {
            "chat": {"enabled": True}
        }
    },
    # ← これが必須。空オブジェクトでOK
    "params": {},
    # オプション（必要に応じて）
    # "access_control": {},
    "is_active": True
}

headers = {"Content-Type": "application/json"}
if API_KEY:
    headers["Authorization"] = f"Bearer {API_KEY}"

response = requests.post(url, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    data = response.json()
    print("✅ モデルが正常に作成されました！")
    print(json.dumps(data, indent=2, ensure_ascii=False))
else:
    print(f"❌ エラー: ステータスコード {response.status_code}")
    print(response.text)
