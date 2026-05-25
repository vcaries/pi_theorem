"""Domain-specific exceptions for the Pi-Scope scientific engine.

Defining a small, well-typed exception hierarchy keeps the calculation code
free of bare ``ValueError`` calls and lets the API layer translate failures
into precise HTTP responses (see :mod:`app.api`).
"""

from __future__ import annotations


class PiTheoremError(Exception):
    """Base class for every error raised by the scientific engine.

    Catching this single type is enough to handle any expected, domain-level
    failure originating from :mod:`app.core`.
    """


class DimensionError(PiTheoremError):
    """Raised when a dimensional formula is malformed or inconsistent.

    Typical causes include an unknown base-dimension symbol, a non-numeric
    exponent, or a vector whose length does not match the number of base
    dimensions.
    """


class UnderdeterminedSystemError(PiTheoremError):
    """Raised when the variable set cannot yield dimensionless groups.

    This happens when the number of variables does not exceed the rank of the
    dimensional matrix, so the Buckingham Pi theorem predicts zero independent
    dimensionless groups.
    """


class InconsistentNullSpaceError(PiTheoremError):
    """Raised when the computed null space size contradicts the Pi theorem.

    This is a safety net: if SymPy returns a number of basis vectors that does
    not equal ``n - rank``, something is fundamentally wrong with the input or
    the linear-algebra backend, and we refuse to return a misleading result.
    """
