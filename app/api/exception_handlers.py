from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.shared.errors.base import ApplicationError
from app.shared.logging.logger import get_logger

logger = get_logger(__name__)

def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApplicationError)
    async def application_error_handler(request: Request, exc: ApplicationError) -> JSONResponse:
        logger.warning(f"Application error: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message}
        )
