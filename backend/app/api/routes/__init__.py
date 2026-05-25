"""Route modules for the Pi-Scope API.

Each module defines a focused :class:`fastapi.APIRouter`:

* :mod:`health` -- liveness / metadata probe.
* :mod:`pi` -- the Buckingham Pi solver endpoint.
* :mod:`library` -- the curated variable library.
* :mod:`examples` -- preloaded worked examples.
"""

from __future__ import annotations

__all__ = ["health", "pi", "library", "examples"]
