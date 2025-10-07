"""
title: OpenWebUI Model Updater
author: you
version: 0.1.0
description: 既存のOpenWebUIカスタムモデルをAPI経由で更新するツール。
"""

import copy
import json
import os
from typing import Any, Dict, Optional

import requests


class Tools:
    def __init__(self):
        self.api_base = (os.getenv("LLM_SERVICE_API_BASE") or "").rstrip("/")
        self.api_key = os.getenv("LLM_SERVICE_API_KEY", "")
        default_model_id = os.getenv("OPENWEBUI_MODEL_ID", "example-model-003")
        self.default_payload = {
            "id": default_model_id,
            "base_model_id": os.getenv(
                "OPENWEBUI_BASE_MODEL_ID", "openai/gpt-4o-mini"
            ),
            "name": os.getenv("OPENWEBUI_MODEL_NAME", "My Custom Model (Updated)"),
            "meta": {
                "description": os.getenv(
                    "OPENWEBUI_MODEL_DESCRIPTION",
                    "Model updated via OpenWebUI API script.",
                ),
                "profile_image_url": os.getenv(
                    "OPENWEBUI_MODEL_AVATAR_URL",
                    "https://api.dicebear.com/7.x/bottts/png?seed=OpenWebUI",
                ),
                "capabilities": {"chat": {"enabled": True}},
            },
            "params": {},
            "is_active": True,
        }

    def _headers(self) -> Dict[str, str]:
        if not self.api_key:
            raise RuntimeError(
                "LLM_SERVICE_API_KEY is not set in environment variables."
            )
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _ensure_api_base(self) -> str:
        if not self.api_base:
            raise RuntimeError(
                "LLM_SERVICE_API_BASE is not set in environment variables."
            )
        return self.api_base

    def _deep_merge(self, base: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
        for key, value in overrides.items():
            if (
                key in base
                and isinstance(base[key], dict)
                and isinstance(value, dict)
            ):
                base[key] = self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base

    def update_model(
        self, payload_overrides: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        OpenWebUIのモデル更新APIを呼び出します。
        :param payload_overrides: デフォルトpayloadに対する上書き辞書
        :return: APIレスポンス or エラーメッセージ
        """
        payload = copy.deepcopy(self.default_payload)
        if payload_overrides:
            payload = self._deep_merge(payload, payload_overrides)

        model_id = payload.get("id")
        if not model_id:
            raise ValueError("Model ID is required to update an OpenWebUI model.")

        try:
            resp = requests.post(
                f"{self._ensure_api_base()}/v1/models/model/update?id={model_id}",
                headers=self._headers(),
                data=json.dumps(payload),
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
            return "✅ Model updated successfully\n" + json.dumps(
                data, indent=2, ensure_ascii=False
            )
        except requests.HTTPError as e:
            status = e.response.status_code if e.response else "unknown"
            body = e.response.text if e.response else ""
            return f"[HTTP Error] {status}: {body}"
        except Exception as e:
            return f"[Error] {type(e).__name__}: {e}"


if __name__ == "__main__":
    tool = Tools()
    print(tool.update_model())
