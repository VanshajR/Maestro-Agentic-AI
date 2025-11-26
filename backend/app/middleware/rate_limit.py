from __future__ import annotations

import time
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_429_TOO_MANY_REQUESTS


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._bucket: dict[str, list[float]] = {}

    async def dispatch(self, request: Request, call_next: Callable):
        client_ip = request.client.host if request.client else "anonymous"
        now = time.time()
        bucket = self._bucket.setdefault(client_ip, [])
        bucket[:] = [ts for ts in bucket if now - ts < self.window_seconds]
        if len(bucket) >= self.max_requests:
            return Response("Too Many Requests", HTTP_429_TOO_MANY_REQUESTS)
        bucket.append(now)
        return await call_next(request)
