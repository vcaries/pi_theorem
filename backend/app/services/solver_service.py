"""Adapter between the API schemas and the pure scientific engine.

This thin service keeps the routes declarative: it converts inbound Pydantic
models into engine value objects, runs the engine, and converts the structured
result back into outbound Pydantic models.
"""

from __future__ import annotations

import logging

from app.core import Dimension, PiResult, Variable, solve_pi_groups
from app.models.schemas import (
    PiGroupOut,
    PiResultOut,
    SolveRequest,
    VariableIn,
)

logger = logging.getLogger(__name__)


def _to_variable(payload: VariableIn) -> Variable:
    """Convert an inbound :class:`VariableIn` into an engine :class:`Variable`.

    Args:
        payload: The validated request variable.

    Returns:
        The corresponding engine variable.

    Raises:
        DimensionError: If the exponent vector is invalid.
    """
    return Variable(
        symbol=payload.symbol,
        dimension=Dimension.from_vector(payload.exponents),
        latex=payload.latex,
        name=payload.name,
    )


def _to_output(result: PiResult) -> PiResultOut:
    """Convert an engine :class:`PiResult` into an outbound :class:`PiResultOut`.

    Args:
        result: The engine result.

    Returns:
        The serialisable API response model.
    """
    return PiResultOut(
        variables=list(result.variables),
        base_symbols=list(result.base_symbols),
        matrix=[list(row) for row in result.matrix],
        rank=result.rank,
        n_variables=result.n_variables,
        n_groups=result.n_groups,
        groups=[
            PiGroupOut(
                index=group.index,
                exponents=list(group.exponents),
                latex=group.latex,
                ascii=group.ascii,
            )
            for group in result.groups
        ],
        product_latex=result.product_latex,
    )


def solve_from_request(request: SolveRequest) -> PiResultOut:
    """Run the Pi-theorem engine for an API request.

    Args:
        request: The validated solve request.

    Returns:
        The serialisable result.

    Raises:
        PiTheoremError: Propagated from the engine for any domain-level failure;
            the API layer maps these to HTTP 422 responses.
    """
    variables = [_to_variable(item) for item in request.variables]
    logger.info("Solving Pi groups for %d variables", len(variables))
    result = solve_pi_groups(variables, integerize=request.integerize)
    return _to_output(result)
