"""
title: OpenWebUI Model Creator
author: you
version: 0.1.0
description: OpenWebUIのカスタムモデルをAPI経由で作成するツール。
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
        self.default_payload = {
            "id": os.getenv("OPENWEBUI_MODEL_ID", "example-model-003"),
            "base_model_id": os.getenv(
                "OPENWEBUI_BASE_MODEL_ID", "openai/gpt-4o-mini"
            ),
            "name": os.getenv("OPENWEBUI_MODEL_NAME", "My Custom Model"),
            "meta": {
                "description": os.getenv(
                    "OPENWEBUI_MODEL_DESCRIPTION",
                    "Model created via OpenWebUI API script.",
                ),
                "profile_image_url": os.getenv(
                    "OPENWEBUI_MODEL_AVATAR_URL",
                    "https://api.dicebear.com/7.x/bottts/png?seed=OpenWebUI-1stModel",
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

    def create_model(
        self,
        model_id: Optional[str] = None,
        base_model_id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        profile_image_url: Optional[str] = None,
        capabilities: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        is_active: Optional[bool] = None,
    ) -> str:
        """
        OpenWebUIのモデル作成APIを呼び出します。
        :param model_id: 作成するモデルID
        :param base_model_id: ベースモデルID
        :param name: モデル表示名
        :param description: モデル説明文
        :param profile_image_url: モデルアイコンURL
        :param capabilities: meta.capabilities の内容
        :param params: 推論パラメータ辞書
        :param is_active: モデルの有効/無効
        :return: APIレスポンス or エラーメッセージ
        """
        payload = copy.deepcopy(self.default_payload)

        if model_id is not None:
            payload["id"] = model_id
        if base_model_id is not None:
            payload["base_model_id"] = base_model_id
        if name is not None:
            payload["name"] = name
        if params is not None:
            payload["params"] = params
        if is_active is not None:
            payload["is_active"] = is_active

        meta = payload.setdefault("meta", {})
        if description is not None:
            meta["description"] = description
        if profile_image_url is not None:
            meta["profile_image_url"] = profile_image_url
        if capabilities is not None:
            meta["capabilities"] = capabilities

        try:
            resp = requests.post(
                f"{self._ensure_api_base()}/v1/models/create",
                headers=self._headers(),
                data=json.dumps(payload),
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
            return "✅ Model created successfully\n" + json.dumps(
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
    print(tool.create_model())
