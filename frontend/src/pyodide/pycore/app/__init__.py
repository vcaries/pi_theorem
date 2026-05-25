"""Pi-Scope backend application package.

This package exposes the FastAPI application factory and the scientific
engine that powers the Buckingham :math:`\\Pi` (Vaschy--Buckingham) theorem
calculator.

Modules:
    core: Pure scientific engine (dimensional analysis, no web dependencies).
    models: Pydantic schemas shared across the API boundary.
    services: Application services (variable library, worked examples).
    api: FastAPI routers exposing the engine over HTTP.

Author:
    V. Caries
"""

from __future__ import annotations

__all__ = ["__version__"]

#: Semantic version of the backend package, kept in sync with the project tag.
__version__ = "1.0.0"
