"""
title: OpenWebUI Model Lister
author: you
version: 0.1.0
description: OpenWebUIに登録されたモデルのID・名前・説明を一覧表示するツール。
"""

import json
import os
from typing import Dict, Iterable, Optional

import requests


class Tools:
    def __init__(self):
        self.api_base = (os.getenv("LLM_SERVICE_API_BASE") or "").rstrip("/")
        self.api_key = os.getenv("LLM_SERVICE_API_KEY", "")

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

    def list_models(self, model_id: Optional[str] = None) -> str:
        """
        OpenWebUIに登録されたモデルの名前・ID・説明を取得して整形済み文字列で返す。
        :param model_id: 絞り込み用のモデルID。指定しない場合は全件取得。
        :return: 整形済み文字列 or エラーメッセージ
        """
        params = {"id": model_id} if model_id else None
        errors = []
        models = None

        for suffix in ("/v1/models", "/v1/models/", "/api/v1/models", "/api/v1/models/"):
            resp = None
            url = f"{self._ensure_api_base()}{suffix}"
            try:
                resp = requests.get(
                    url,
                    headers=self._headers(),
                    params=params,
                    timeout=60,
                )
                resp.raise_for_status()
                models = resp.json()
                break
            except requests.HTTPError as e:
                status = e.response.status_code if e.response else "unknown"
                body = e.response.text if e.response else ""
                errors.append(f"{url} -> HTTP {status}: {body[:120]}")
            except ValueError:
                preview = resp.text[:200] if resp and resp.text else ""
                errors.append(f"{url} -> Parse error: {preview}")
            except Exception as e:
                errors.append(f"{url} -> {type(e).__name__}: {e}")

        if models is None:
            return "[Error] Unable to fetch models. Tried:\n" + "\n".join(errors)

        if isinstance(models, dict) and "data" in models:
            candidate = models.get("data")
            if isinstance(candidate, Iterable):
                models = candidate

        if isinstance(models, dict) and "models" in models:
            candidate = models.get("models")
            if isinstance(candidate, Iterable):
                models = candidate

        if isinstance(models, (str, bytes)):
            return (
                "[Error] UnexpectedResponse: Expected a list of models but received "
                + str(models)
            )

        if not isinstance(models, list):
            return (
                "[Error] UnexpectedResponse: Expected a list of models but received "
                + json.dumps(models, ensure_ascii=False)
            )

        lines = []
        for model in models:
            if not isinstance(model, dict):
                continue
            model_id = model.get("id", "unknown-id")
            name = model.get("name", "Unnamed Model")
            description = ""
            meta = model.get("meta") or {}
            if isinstance(meta, dict):
                description = meta.get("description", "")
            lines.append(f"- {name} ({model_id}): {description}")

        return "\n".join(lines) if lines else "No models found."


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    tool = Tools()
    print(tool.list_models())
