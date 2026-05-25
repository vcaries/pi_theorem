"""Service exposing preloaded, citeable worked examples.

Worked examples (such as the flagship Chen 1990 case) let a visitor see a real,
scientifically meaningful result in a single click, which is central to the
"demonstration" goal of the application.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path

import yaml

from app.config import get_settings
from app.models.schemas import WorkedExample

logger = logging.getLogger(__name__)


class ExampleService:
    """Loads and serves the bundled worked examples."""

    def __init__(self, examples_path: Path) -> None:
        """Initialise the service.

        Args:
            examples_path: Path to the YAML examples file.
        """
        self._examples_path = examples_path
        self._cache: dict[str, WorkedExample] | None = None

    def list_examples(self) -> list[WorkedExample]:
        """Return all worked examples.

        Returns:
            Every :class:`WorkedExample`, in file order.
        """
        return list(self._get_all().values())

    def get_example(self, example_id: str) -> WorkedExample | None:
        """Return one example by its identifier.

        Args:
            example_id: The example slug (e.g. ``"chen_1990"``).

        Returns:
            The matching example, or ``None`` if it does not exist.
        """
        return self._get_all().get(example_id)

    def _get_all(self) -> dict[str, WorkedExample]:
        """Return the memoised mapping of example id to example.

        Returns:
            A dict keyed by example id.
        """
        if self._cache is None:
            self._cache = self._load()
        return self._cache

    def _load(self) -> dict[str, WorkedExample]:
        """Read, parse and validate the YAML examples file.

        Returns:
            A dict keyed by example id.

        Raises:
            FileNotFoundError: If the file is missing.
            ValueError: If parsing or validation fails.
        """
        logger.info("Loading worked examples from %s", self._examples_path)
        if not self._examples_path.exists():
            raise FileNotFoundError(f"Examples file not found: {self._examples_path}")

        raw = yaml.safe_load(self._examples_path.read_text(encoding="utf-8")) or {}
        examples = [WorkedExample(**ex) for ex in raw.get("examples", [])]
        logger.info("Loaded %d worked examples", len(examples))
        return {example.id: example for example in examples}


@lru_cache
def get_example_service() -> ExampleService:
    """Return the process-wide :class:`ExampleService` singleton.

    Returns:
        The cached service, configured from application settings.
    """
    settings = get_settings()
    return ExampleService(settings.examples_path)
