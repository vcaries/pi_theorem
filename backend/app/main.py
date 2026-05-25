"""FastAPI application factory and entry point.

Running ``uvicorn app.main:app`` (or ``python -m app.main``) starts the API.
The factory pattern (:func:`create_app`) keeps construction explicit and makes
the app trivial to instantiate in tests with overridden settings.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api import api_router
from app.config import Settings, get_settings
from app.logging_config import configure_logging

logger = logging.getLogger(__name__)

#: OpenAPI description shown on the ``/docs`` page.
_DESCRIPTION = (
    "Pi-Scope applies the Vaschy–Buckingham (Pi) theorem to determine the "
    "dimensionless groups that govern a physical problem from a set of "
    "dimensioned variables. Built on SymPy for exact linear algebra."
)


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure a FastAPI application instance.

    Args:
        settings: Optional settings override (useful for tests). When omitted,
            the cached process settings are used.

    Returns:
        A fully configured :class:`fastapi.FastAPI` application.
    """
    settings = settings or get_settings()
    configure_logging(settings.log_level if not settings.debug else "DEBUG")
    logger.info("Creating %s v%s", settings.app_name, settings.version)

    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        description=_DESCRIPTION,
        debug=settings.debug,
    )

    # Allow the browser-based frontend (Vite dev server, or a future static host)
    # to call the API across origins.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.api_prefix)

    @app.get("/", include_in_schema=False)
    def root() -> dict[str, str]:
        """Return a minimal landing payload pointing to the docs.

        Returns:
            A mapping with the app name, version and docs URL.
        """
        return {
            "name": settings.app_name,
            "version": __version__,
            "docs": "/docs",
        }

    return app


#: Module-level ASGI application used by ``uvicorn app.main:app``.
app = create_app()


def main() -> None:
    """Run a development server via ``python -m app.main``."""
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
