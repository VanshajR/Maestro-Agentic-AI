import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware import Middleware
from starlette.requests import Request
from fastapi.security import APIKeyHeader

from .config import settings
from .agent.router import router as agent_router
from .utils.logger import get_logger
from .middleware.rate_limit import RateLimitMiddleware
from .middleware.auth import APIKeyAuthMiddleware
from .utils.error_handler import register_exception_handlers

logger = get_logger()

middleware = [
    Middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_methods=["*"], allow_headers=["*"]),
    Middleware(RateLimitMiddleware, max_requests=settings.RATE_LIMIT_PER_MINUTE),
]

app = FastAPI(title=settings.APP_NAME, middleware=middleware)

app.include_router(agent_router, prefix="/api/v1/agent")

api_key_header = APIKeyHeader(name="Authorization")

@app.get("/api/v1/health")
async def health():
    return JSONResponse({"status": "ok", "app": settings.APP_NAME})


@app.middleware("http")
async def api_key_auth_middleware(request: Request, call_next):
    response = await call_next(request)
    return response

register_exception_handlers(app)
