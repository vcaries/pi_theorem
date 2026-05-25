"""Application logging configuration.

A single :func:`configure_logging` entry point sets up consistent, readable log
formatting for the whole process. Keeping this separate from the app factory
makes it reusable from tests, scripts and the CLI.
"""

from __future__ import annotations

import logging
import sys

#: Log line format: timestamp, level, logger name and message.
_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging(level: str = "INFO") -> None:
    """Configure root logging once for the whole application.

    Args:
        level: Minimum level to emit, e.g. ``"DEBUG"`` or ``"INFO"``. Invalid
            values fall back to ``INFO``.
    """
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt=_LOG_FORMAT, datefmt=_DATE_FORMAT))

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(numeric_level)

    # Tame noisy third-party loggers while keeping our own at the chosen level.
    logging.getLogger("uvicorn.access").setLevel(max(numeric_level, logging.INFO))
