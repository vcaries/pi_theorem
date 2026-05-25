"""Centralised application configuration.

All tunable settings live here and are loaded from environment variables (or a
local ``.env`` file) via :class:`pydantic_settings.BaseSettings`. Centralising
configuration keeps secrets and environment-specific values out of the code and
makes the service trivial to configure in Docker or a future cloud deployment.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

#: Absolute path to the ``backend`` directory (parent of the ``app`` package).
BACKEND_ROOT: Path = Path(__file__).resolve().parent.parent

#: Directory holding bundled scientific data (variable library, examples).
DATA_DIR: Path = Path(__file__).resolve().parent / "data"


class Settings(BaseSettings):
    """Strongly-typed application settings.

    Attributes:
        app_name: Human-readable application name used in the OpenAPI docs.
        version: API version string surfaced under ``/api`` and in responses.
        debug: Enables verbose logging and FastAPI debug behaviour.
        log_level: Root log level (``DEBUG``, ``INFO``, ``WARNING`` ...).
        api_prefix: URL prefix under which all API routes are mounted.
        cors_origins: Origins allowed to call the API from a browser. Defaults to
            the local Vite dev server.
        library_path: Path to the YAML variable library.
        examples_path: Path to the YAML worked-examples file.
    """

    model_config = SettingsConfigDict(
        env_prefix="PISCOPE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Pi-Scope API"
    version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"

    api_prefix: str = "/api"
    cors_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    )

    library_path: Path = DATA_DIR / "library.yaml"
    examples_path: Path = DATA_DIR / "examples.yaml"


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide settings singleton.

    The result is cached so the ``.env`` file and environment are read only once.
    FastAPI dependencies and services should call this rather than instantiating
    :class:`Settings` directly.

    Returns:
        The cached :class:`Settings` instance.
    """
    return Settings()
