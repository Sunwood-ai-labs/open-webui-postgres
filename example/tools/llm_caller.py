"""
title: LLM Caller
author: you
version: 0.1.0
description: 任意のモデルとプロンプトを指定して、LLM APIを呼び出す最小構成ツール。
"""

import os
import json
import requests

class Tools:
    def __init__(self):
        # 環境変数で設定可能
        self.api_base = os.getenv("LLM_SERVICE_API_BASE", "https://api.openai.com/v1")
        self.api_key = os.getenv("LLM_SERVICE_API_KEY", "")
        self.default_model = os.getenv("LLM_SERVICE_MODEL", "gpt-4o-mini")

    def _headers(self):
        if not self.api_key:
            raise RuntimeError(
                "LLM_SERVICE_API_KEY is not set in environment variables."
            )
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def call_llm(self, model: str, prompt: str) -> str:
        """
        指定されたモデルとプロンプトで LLM を呼び出します。
        :param model: 使用するモデル名 (例: gpt-4o-mini)
        :param prompt: 投げたいテキストプロンプト
        :return: LLMからの応答テキスト
        """
        body = {
            "model": model or self.default_model,
            "messages": [{"role": "user", "content": prompt}],
        }

        try:
            resp = requests.post(
                f"{self.api_base}/chat/completions",
                headers=self._headers(),
                data=json.dumps(body),
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
        except requests.HTTPError as e:
            return f"[HTTP Error] {e.response.status_code}: {e.response.text}"
        except Exception as e:
            return f"[Error] {type(e).__name__}: {e}"
