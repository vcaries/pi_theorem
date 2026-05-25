"""Buckingham Pi solver endpoint."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.core.exceptions import PiTheoremError
from app.models.schemas import PiResultOut, SolveRequest
from app.services import solve_from_request

router = APIRouter()


@router.post(
    "/solve",
    response_model=PiResultOut,
    summary="Compute the dimensionless Pi groups for a set of variables",
)
def solve(request: SolveRequest) -> PiResultOut:
    """Apply the Buckingham Pi theorem to the submitted variables.

    Args:
        request: The variables and solver options.

    Returns:
        The dimensional matrix, its rank and the dimensionless groups.

    Raises:
        HTTPException: ``422`` if the input cannot yield dimensionless groups or
            is otherwise invalid at the domain level.
    """
    try:
        return solve_from_request(request)
    except PiTheoremError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
