"""Health and metadata endpoint."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.config import Settings, get_settings

router = APIRouter()


@router.get("/health", summary="Liveness probe and API metadata")
def health(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    """Return a simple liveness payload with the app name and version.

    Args:
        settings: Injected application settings.

    Returns:
        A mapping with ``status``, ``app`` and ``version`` keys.
    """
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.version,
    }
