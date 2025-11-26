from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED


class APIKeyAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, api_key: str | None = None):
        super().__init__(app)
        self.api_key = api_key

    async def dispatch(self, request: Request, call_next):
        if self.api_key:
            header = request.headers.get("x-api-key")
            if header != self.api_key:
                return Response("Unauthorized", HTTP_401_UNAUTHORIZED)
        return await call_next(request)
