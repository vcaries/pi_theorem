"""Service exposing the curated variable library.

The library is loaded once from ``library.yaml`` at first use and cached for the
lifetime of the process. The service validates the file against the Pydantic
schemas so a malformed library fails fast and loudly at startup rather than
producing confusing runtime errors.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path

import yaml

from app.config import get_settings
from app.core.dimensions import BASE_DIMENSIONS
from app.models.schemas import (
    BaseDimensionInfo,
    LibraryCategory,
    LibraryResponse,
)

logger = logging.getLogger(__name__)


class LibraryService:
    """Loads and serves the curated, domain-organised variable library."""

    def __init__(self, library_path: Path) -> None:
        """Initialise the service.

        Args:
            library_path: Path to the YAML library file.
        """
        self._library_path = library_path
        self._cache: LibraryResponse | None = None

    def get_library(self) -> LibraryResponse:
        """Return the full library (base dimensions + categories).

        The result is parsed once and memoised.

        Returns:
            A validated :class:`LibraryResponse`.

        Raises:
            FileNotFoundError: If the library file does not exist.
            ValueError: If the file cannot be parsed or fails validation.
        """
        if self._cache is None:
            self._cache = self._load()
        return self._cache

    def _load(self) -> LibraryResponse:
        """Read, parse and validate the YAML library file.

        Returns:
            The validated library.

        Raises:
            FileNotFoundError: If the file is missing.
            ValueError: If parsing or validation fails.
        """
        logger.info("Loading variable library from %s", self._library_path)
        if not self._library_path.exists():
            raise FileNotFoundError(f"Variable library not found: {self._library_path}")

        raw = yaml.safe_load(self._library_path.read_text(encoding="utf-8")) or {}
        categories = [LibraryCategory(**cat) for cat in raw.get("categories", [])]
        base_dimensions = [
            BaseDimensionInfo(
                symbol=dim.symbol,
                name=dim.name,
                si_unit=dim.si_unit,
                label_en=dim.label_en,
                label_fr=dim.label_fr,
            )
            for dim in BASE_DIMENSIONS
        ]
        logger.info("Loaded %d categories", len(categories))
        return LibraryResponse(base_dimensions=base_dimensions, categories=categories)


@lru_cache
def get_library_service() -> LibraryService:
    """Return the process-wide :class:`LibraryService` singleton.

    Returns:
        The cached service, configured from application settings.
    """
    settings = get_settings()
    return LibraryService(settings.library_path)
