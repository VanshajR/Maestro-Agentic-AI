from typing import List
import asyncio

import httpx
from tenacity import AsyncRetrying, stop_after_attempt, wait_exponential

from ..config import settings


class LLMProvider:
    def __init__(self):
        self.groq_key = settings.GROQ_API_KEY
        self.groq_models = settings.GROQ_MODELS
        self.hf_key = settings.HF_API_KEY

    async def _groq_request(self, prompt: str, model: str) -> str:
        if not self.groq_key:
            raise RuntimeError("Groq API key not configured")
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.groq_key}", "Content-Type": "application/json"}
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 800,
        }

        async with httpx.AsyncClient(timeout=30) as client:
            async for attempt in AsyncRetrying(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10)):
                with attempt:
                    response = await client.post(url, headers=headers, json=payload)
                    response.raise_for_status()
                    data = response.json()
                    return data["choices"][0]["message"]["content"]

    async def _groq_complete(self, prompt: str, preferred_model: str | None = None) -> str:
        models: List[str] = []
        if preferred_model:
            models.append(preferred_model)
        for m in self.groq_models:
            if m not in models:
                models.append(m)

        last_error: Exception | None = None
        for model_name in models:
            try:
                return await self._groq_request(prompt, model_name)
            except httpx.HTTPStatusError as exc:
                last_error = exc
                if exc.response.status_code == 429:
                    # rotate to next model if rate limited
                    continue
            except Exception as exc:
                last_error = exc
                continue

        if last_error:
            raise last_error
        raise RuntimeError("No Groq models available")

    async def _hf_complete(self, prompt: str, model: str = "gpt2") -> str:
        if not self.hf_key:
            raise RuntimeError("HF API key not configured")
        url = f"https://api-inference.huggingface.co/models/{model}"
        headers = {"Authorization": f"Bearer {self.hf_key}"}
        async with httpx.AsyncClient(timeout=30) as client:
            async for attempt in AsyncRetrying(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10)):
                with attempt:
                    response = await client.post(url, headers=headers, json={"inputs": prompt})
                    response.raise_for_status()
                    data = response.json()
                    if isinstance(data, list) and data:
                        return data[0].get("generated_text", "")
                    return str(data)

    async def complete(self, prompt: str, model: str | None = None) -> str:
        try:
            return await self._groq_complete(prompt, preferred_model=model)
        except Exception:
            pass

        try:
            return await self._hf_complete(prompt)
        except Exception:
            pass

        await asyncio.sleep(0.05)
        return f"[fallback] LLM providers unavailable. Prompt length={len(prompt)}\nPrompt:\n{prompt[:2000]}"


llm_provider = LLMProvider()
