from __future__ import annotations

from fastapi import APIRouter

from app.api.routes import documents, events, geocoding, health, upload


api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(upload.router, prefix="/api", tags=["upload"])
api_router.include_router(documents.router, prefix="/api", tags=["documents"])
api_router.include_router(events.router, prefix="/api", tags=["events"])
api_router.include_router(geocoding.router, prefix="/api", tags=["geocoding"])
