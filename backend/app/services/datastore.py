from typing import Any, Dict
import asyncio

# Very small in-memory store for intermediate results and plans
_STORE: Dict[str, Any] = {}


async def save(key: str, value: Any) -> None:
    _STORE[key] = value


async def load(key: str) -> Any:
    return _STORE.get(key)
