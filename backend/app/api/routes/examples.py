"""Worked-examples endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.schemas import WorkedExample
from app.services import ExampleService, get_example_service

router = APIRouter()


@router.get(
    "",
    response_model=list[WorkedExample],
    summary="List all preloaded worked examples",
)
def list_examples(
    service: ExampleService = Depends(get_example_service),
) -> list[WorkedExample]:
    """Return every bundled worked example.

    Args:
        service: Injected example service.

    Returns:
        The list of worked examples.
    """
    return service.list_examples()


@router.get(
    "/{example_id}",
    response_model=WorkedExample,
    summary="Fetch a single worked example by id",
)
def get_example(
    example_id: str,
    service: ExampleService = Depends(get_example_service),
) -> WorkedExample:
    """Return a single worked example.

    Args:
        example_id: The example slug (e.g. ``"chen_1990"``).
        service: Injected example service.

    Returns:
        The matching worked example.

    Raises:
        HTTPException: ``404`` if no example has the given id.
    """
    example = service.get_example(example_id)
    if example is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unknown example id: {example_id!r}",
        )
    return example
