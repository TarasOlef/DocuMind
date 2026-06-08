from fastapi import APIRouter
from app.api.routes import health

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
# Add more routers here in the future:
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
