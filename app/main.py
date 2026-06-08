from fastapi import FastAPI

from app.api.exception_handlers import add_exception_handlers
from app.api.router import api_router
from app.shared.config.settings import settings
from app.shared.logging.logger import setup_logging

# Setup global logging
setup_logging()

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        description="Plataforma backend empresarial para RAG documental.",
        version=settings.APP_VERSION,
    )

    # Register global exception handlers
    add_exception_handlers(app)

    # Include all API routes under the specified prefix
    app.include_router(api_router, prefix=settings.API_PREFIX)

    return app

app = create_app()
