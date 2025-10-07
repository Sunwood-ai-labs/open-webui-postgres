import os
import json
import requests
from dotenv import load_dotenv

# === .env 読み込み ===
load_dotenv()

API_KEY = os.getenv("LLM_SERVICE_API_KEY")
API_BASE = os.getenv("LLM_SERVICE_API_BASE")

MODEL_ID = "example-model-003"
# 初回作成時の base_model_id を再指定（上書きで消えないように）
BASE_MODEL_ID = "openai/gpt-4o-mini"

url = f"{API_BASE}/v1/models/model/update?id={MODEL_ID}"

payload = {
    "id": MODEL_ID,
    "base_model_id": BASE_MODEL_ID,  # ← 重要：省略すると null になる実装がある
    "name": "My Custom Model (Updated)",
    "meta": {
        "description": "Model updated via OpenWebUI API script.",
        # ランダムじゃない固定画像（DiceBear の固定seed例）
        "profile_image_url": "https://api.dicebear.com/7.x/bottts/png?seed=OpenWebUI",
        "capabilities": {
            "chat": {"enabled": True}
        }
    },
    # params は必須。空でもOK（必要なら中に温度などを入れる）
    "params": {},
    "is_active": True
}

headers = {"Content-Type": "application/json"}
if API_KEY:
    headers["Authorization"] = f"Bearer {API_KEY}"

response = requests.post(url, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    data = response.json()
    print("✅ モデルが正常に更新されました！")
    print(json.dumps(data, indent=2, ensure_ascii=False))
else:
    print(f"❌ エラー: ステータスコード {response.status_code}")
    print(response.text)
