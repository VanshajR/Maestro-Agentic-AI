from typing import Any
import httpx
from ..tools.web_fetch import fetch


async def crawl_url(url: str) -> dict[str, Any]:
    return await fetch(url)
