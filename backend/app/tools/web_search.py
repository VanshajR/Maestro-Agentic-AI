from typing import Any
from urllib.parse import quote_plus

import httpx
from tenacity import AsyncRetrying, stop_after_attempt, wait_exponential

from ..config import settings


async def search(query: str) -> dict[str, Any]:
    key = settings.SERP_API_KEY
    if key:
        url = "https://serpapi.com/search.json"
        params = {"q": query, "api_key": key}
        async with httpx.AsyncClient(timeout=20) as client:
            async for attempt in AsyncRetrying(stop=stop_after_attempt(3), wait=wait_exponential()):
                with attempt:
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    return {"source": "serpapi", "data": response.json()}

    search_url = f"https://duckduckgo.com/html/?q={quote_plus(query)}"
    async with httpx.AsyncClient(timeout=20) as client:
        async for attempt in AsyncRetrying(stop=stop_after_attempt(2), wait=wait_exponential()):
            with attempt:
                response = await client.get(search_url)
                response.raise_for_status()
                return {"source": "duckduckgo_html", "html_snippet": response.text[:8000]}
