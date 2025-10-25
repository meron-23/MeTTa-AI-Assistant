from __future__ import annotations

import asyncio
from typing import List, Optional
import os
import random
import google.generativeai as genai

from app.core.utils.retry import async_retry, RetryConfig


def _is_rate_limit(err: Exception) -> bool:
    msg = str(err).lower()
    return (
        "429" in msg
        or "rate" in msg
        or "quota" in msg
        or "resourceexhausted" in msg
        or "exceeded" in msg
    )


class GeminiClient:
    """Gemini client with API key rotation and retry/backoff.

    Usage:
        client = GeminiClient(model_name)
        text = await client.generate_text(prompt)
    """

    def __init__(
        self,
        model_name: str,
        api_keys: Optional[List[str]] = None,
        retry_cfg: Optional[RetryConfig] = None,
    ) -> None:
        keys = api_keys or _load_keys_from_env()
        if not keys:
            raise ValueError("No Gemini API keys provided")
        self._keys = keys
        self._idx = 0
        self._model_name = model_name
        self._retry_cfg = retry_cfg or RetryConfig()

    def _next_key(self) -> str:
        key = self._keys[self._idx % len(self._keys)]
        self._idx += 1
        return key

    async def _call_generate(self, prompt: str, temperature: float, max_tokens: int):
        genai.configure(api_key=self._next_key())
        model = genai.GenerativeModel(self._model_name)
        return await asyncio.to_thread(
            lambda: model.generate_content(
                prompt,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                },
            )
        )

    @async_retry(retry_on=_is_rate_limit)
    async def generate_text(self, prompt: str, *, temperature: float, max_tokens: int) -> str:
        resp = await self._call_generate(prompt, temperature, max_tokens)
        return resp.text.strip()


def _load_keys_from_env() -> List[str]:
    csv = os.getenv("GEMINI_API_KEYS", "").strip()
    keys = [k.strip() for k in csv.split(",") if k.strip()]
    if not keys:
        single = os.getenv("GEMINI_API_KEY")
        if single:
            keys = [single]
    return keys
