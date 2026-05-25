"""Scientific core of Pi-Scope.

This subpackage is intentionally free of any web-framework dependency. It can
be imported and used as a standalone library, embedded in a notebook, or driven
from a CLI. The FastAPI layer is a thin adapter on top of it.

Public API:
    BASE_DIMENSIONS: Ordered tuple of the seven SI base dimensions.
    Dimension: Immutable value object representing a dimensional formula.
    Variable: A named physical quantity with its dimensional formula.
    PiGroup, PiResult: Structured output of the engine.
    solve_pi_groups: Main entry point applying the Buckingham Pi theorem.
"""

from __future__ import annotations

from app.core.dimensions import BASE_DIMENSIONS, BaseDimension, Dimension
from app.core.exceptions import (
    DimensionError,
    PiTheoremError,
    UnderdeterminedSystemError,
)
from app.core.pi_theorem import (
    PiGroup,
    PiResult,
    Variable,
    solve_pi_groups,
)

__all__ = [
    "BASE_DIMENSIONS",
    "BaseDimension",
    "Dimension",
    "DimensionError",
    "PiTheoremError",
    "UnderdeterminedSystemError",
    "PiGroup",
    "PiResult",
    "Variable",
    "solve_pi_groups",
]
