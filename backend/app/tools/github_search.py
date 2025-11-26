from typing import Any
import httpx
import logging
import urllib.parse
import re
from ..config import settings
from tenacity import AsyncRetrying, stop_after_attempt, wait_exponential
from app.tools.groq_api import summarize_query

logger = logging.getLogger("github_search")

async def search(query: str) -> dict[str, Any]:
    token = settings.GITHUB_TOKEN
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    if token:
        headers["Authorization"] = f"token {token.strip()}"

    # --- CLEANING LOGIC ---
    # 1. Remove common prefixes the Planner might leave behind
    for prefix in ["search github for", "find repos for", "search for"]:
        if query.lower().startswith(prefix):
            query = query[len(prefix):].strip()

    # 2. AGGRESSIVE: Remove quotes and special characters that break exact matching
    # We keep spaces, hyphens, and underscores.
    clean_query = query.replace('"', '').replace("'", "").strip()
    
    # 3. Fallback: If query is empty after cleaning, use "popular"
    if not clean_query:
        clean_query = "popular"

    logger.info(f"Original Query: {query} | Cleaned Query for API: {clean_query}")

    # Encode for URL
    encoded_query = urllib.parse.quote(clean_query)
    
    # We simply search by stars to guarantee "popular" results if the query is broad
    url = f"https://api.github.com/search/repositories?q={encoded_query}&sort=stars&order=desc&per_page=5"
    
    async with httpx.AsyncClient(timeout=20) as client:
        async for attempt in AsyncRetrying(stop=stop_after_attempt(3), wait=wait_exponential()):
            with attempt:
                try:
                    r = await client.get(url, headers=headers)
                    
                    if r.status_code == 401:
                        return {"error": "GitHub API Key Invalid (401)."}
                    if r.status_code == 403:
                        return {"error": "GitHub Rate Limit Exceeded."}
                        
                    r.raise_for_status()
                    data = r.json()
                    items = []
                    
                    for it in data.get("items", [])[:5]:
                        items.append({
                            "name": it.get("full_name"),
                            "description": it.get("description"),
                            "stars": it.get("stargazers_count"),
                            "url": it.get("html_url"),
                            "language": it.get("language")
                        })
                    
                    if not items:
                        # Fallback: Try searching without sort restrictions if strict search failed
                        return {"message": f"No results found for '{clean_query}'. Try broader keywords."}
                        
                    return {"results": items}

                except Exception as e:
                    logger.error(f"GitHub search error: {e}")
                    return {"error": str(e)}