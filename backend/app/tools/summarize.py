from typing import Any
from ..agent.llm import llm_provider


async def summarize_text(text: str) -> dict[str, Any]:
    prompt = f"Summarize the following text concisely:\n{text[:4000]}"
    res = await llm_provider.complete(prompt)
    return {"summary": res}
