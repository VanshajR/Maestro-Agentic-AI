from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from typing import Any
from urllib.parse import urlparse

import httpx
from PyPDF2 import PdfReader


def _extract_bytes(data: bytes, source: str) -> dict[str, Any]:
    try:
        reader = PdfReader(BytesIO(data))
        text = []
        for page in reader.pages:
            text.append(page.extract_text() or "")
        return {"source": source, "text": "\n".join(text)[:20000]}
    except Exception as exc:
        return {"source": source, "error": str(exc)}


def _extract_file(path: str) -> dict[str, Any]:
    try:
        reader = PdfReader(path)
        text = []
        for page in reader.pages:
            text.append(page.extract_text() or "")
        return {"source": path, "text": "\n".join(text)[:20000]}
    except Exception as exc:
        return {"source": path, "error": str(exc)}


async def extract(path_or_url: str) -> dict[str, Any]:
    parsed = urlparse(path_or_url)
    if parsed.scheme in {"http", "https"}:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(path_or_url)
            response.raise_for_status()
            return _extract_bytes(response.content, path_or_url)

    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=2) as executor:
        return await loop.run_in_executor(executor, _extract_file, path_or_url)
