"""Variable-library endpoint."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.models.schemas import LibraryResponse
from app.services import LibraryService, get_library_service

router = APIRouter()


@router.get(
    "",
    response_model=LibraryResponse,
    summary="List the SI base dimensions and the curated variable library",
)
def get_library(
    service: LibraryService = Depends(get_library_service),
) -> LibraryResponse:
    """Return the base dimensions and all library categories.

    Args:
        service: Injected library service.

    Returns:
        The full :class:`LibraryResponse`.
    """
    return service.get_library()
