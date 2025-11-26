from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AgentError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AgentError)
    async def agent_error_handler(request: Request, exc: AgentError):
        return JSONResponse({"error": exc.message}, status_code=400)

    @app.exception_handler(Exception)
    async def generic_handler(request: Request, exc: Exception):
        return JSONResponse({"error": "internal_server_error", "message": str(exc)}, status_code=500)
