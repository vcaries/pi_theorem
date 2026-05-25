"""HTTP API layer.

Thin FastAPI routers that translate requests into service/engine calls and map
domain exceptions to HTTP status codes. No scientific logic lives here.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.api.routes import examples, health, library, pi

#: Aggregate router mounted under the configured API prefix in the app factory.
api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(pi.router, prefix="/pi", tags=["pi-theorem"])
api_router.include_router(library.router, prefix="/library", tags=["library"])
api_router.include_router(examples.router, prefix="/examples", tags=["examples"])

__all__ = ["api_router"]
