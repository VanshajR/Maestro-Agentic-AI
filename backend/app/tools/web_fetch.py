from typing import Any
import httpx
from bs4 import BeautifulSoup
from tenacity import AsyncRetrying, stop_after_attempt, wait_exponential


async def fetch(query: str) -> dict[str, Any]:
    # try to extract URL from query
    url = None
    parts = query.split()
    for p in parts:
        if p.startswith("http://") or p.startswith("https://"):
            url = p
            break
    if not url:
        # If no url, try google query via text
        return {"error": "no URL found in query", "query": query}

    async with httpx.AsyncClient(timeout=20) as client:
        async for attempt in AsyncRetrying(stop=stop_after_attempt(3), wait=wait_exponential()):
            with attempt:
                r = await client.get(url)
                r.raise_for_status()
                soup = BeautifulSoup(r.text, "html.parser")
                for s in soup(["script", "style"]):
                    s.decompose()
                text = "\n".join([p.get_text(separator=" ") for p in soup.find_all("p")])
                title = soup.title.string if soup.title else url
                return {"url": url, "title": title, "text": text[:10000]}
