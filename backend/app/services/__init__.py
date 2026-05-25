"""Application services layer.

Services encapsulate use-cases that sit between the HTTP routes and the pure
:mod:`app.core` engine: loading the curated variable library, serving worked
examples, and converting API schemas into engine value objects.
"""

from __future__ import annotations

from app.services.library_service import LibraryService, get_library_service
from app.services.example_service import ExampleService, get_example_service
from app.services.solver_service import solve_from_request

__all__ = [
    "LibraryService",
    "get_library_service",
    "ExampleService",
    "get_example_service",
    "solve_from_request",
]
