"""Buckingham :math:`\\Pi` (Vaschy--Buckingham) theorem engine.

This module is the modern, structured successor of the original
``pi_theorem.py`` script. It keeps the exact same mathematical idea --- the
dimensionless groups are a basis of the null space of the dimensional matrix ---
but returns a rich, serialisable result instead of printing to ``stdout``:

* the dimensional matrix actually shown to the user (active rows only),
* its rank and the predicted number of independent groups,
* each :class:`PiGroup` with integer exponents, a symbolic form and LaTeX.

The Vaschy--Buckingham theorem states that a physically meaningful relation
between ``n`` variables involving ``k`` independent base dimensions can be
rewritten as a relation between ``n - k`` independent dimensionless groups.
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from dataclasses import dataclass, field
from fractions import Fraction
from functools import reduce
from math import gcd

import sympy as sp

from app.core.dimensions import (
    BASE_DIMENSIONS,
    Dimension,
    active_dimension_indices,
)
from app.core.exceptions import (
    InconsistentNullSpaceError,
    PiTheoremError,
    UnderdeterminedSystemError,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------- #
# Input / output value objects                                          #
# ---------------------------------------------------------------------- #
@dataclass(frozen=True, slots=True)
class Variable:
    """A physical quantity participating in the analysis.

    Attributes:
        symbol: Short identifier used in the symbolic output (e.g. ``"rho"``).
        dimension: The variable's dimensional formula.
        latex: Optional LaTeX rendering of the symbol (e.g. ``"\\rho"``). When
            omitted, ``symbol`` is used verbatim.
        name: Optional human-readable name (e.g. ``"Density"``).
    """

    symbol: str
    dimension: Dimension
    latex: str | None = None
    name: str | None = None

    @property
    def display_latex(self) -> str:
        """str: LaTeX symbol to render, falling back to the raw symbol."""
        return self.latex if self.latex else _escape_latex(self.symbol)


@dataclass(frozen=True, slots=True)
class PiGroup:
    """A single dimensionless group :math:`\\Pi_i`.

    Attributes:
        index: 1-based index of the group.
        exponents: Integer exponent applied to each input variable, aligned with
            the variable order passed to :func:`solve_pi_groups`.
        latex: LaTeX rendering of the group, e.g. ``"\\Pi_{1} = \\dfrac{...}{...}"``.
        ascii: Plain-text rendering, e.g. ``"Pi_1 = rho*v**2/DeltaP"``.
    """

    index: int
    exponents: tuple[int, ...]
    latex: str
    ascii: str


@dataclass(frozen=True, slots=True)
class PiResult:
    """Complete, serialisable result of a Pi-theorem computation.

    Attributes:
        variables: The variable symbols, in input order (matrix column labels).
        base_symbols: Active base-dimension symbols (matrix row labels).
        matrix: Dimensional matrix as integer rows (one row per active base
            dimension, one column per variable).
        rank: Rank of the dimensional matrix (number of independent dimensions).
        n_variables: Number of input variables.
        n_groups: Number of independent dimensionless groups (``n - rank``).
        groups: The computed :class:`PiGroup` objects.
        product_latex: LaTeX of the product of all groups, mirroring the original
            tool's behaviour; ``None`` when there is at most one group.
    """

    variables: tuple[str, ...]
    base_symbols: tuple[str, ...]
    matrix: tuple[tuple[int, ...], ...]
    rank: int
    n_variables: int
    n_groups: int
    groups: tuple[PiGroup, ...]
    product_latex: str | None = field(default=None)


# ---------------------------------------------------------------------- #
# Public engine entry point                                             #
# ---------------------------------------------------------------------- #
def solve_pi_groups(
    variables: Sequence[Variable],
    *,
    integerize: bool = True,
) -> PiResult:
    """Apply the Buckingham Pi theorem to a set of dimensioned variables.

    The algorithm assembles the dimensional matrix ``D`` whose columns are the
    variables' exponent vectors, computes a basis of its null space, and turns
    each basis vector into a dimensionless group.

    Args:
        variables: The physical quantities to analyse. At least two variables
            are required for a meaningful analysis.
        integerize: When ``True`` (default), each group's exponents are scaled to
            the smallest integers (clearing fractions and common factors) and
            sign-normalised, which is the conventional way to present Pi groups.

    Returns:
        A :class:`PiResult` describing the matrix, its rank and every group.

    Raises:
        PiTheoremError: If fewer than two variables are supplied or symbols are
            not unique.
        UnderdeterminedSystemError: If the theorem predicts zero groups
            (``n <= rank``), i.e. more independent dimensions than free
            variables.
        InconsistentNullSpaceError: If the null-space size returned by the linear
            algebra backend contradicts ``n - rank`` (a safety net).
    """
    _validate_inputs(variables)

    n_variables = len(variables)
    logger.debug("Solving Pi groups for %d variables", n_variables)

    # Restrict the matrix to base dimensions that actually appear, so the matrix
    # shown to the user has no all-zero rows.
    active = active_dimension_indices(v.dimension for v in variables)
    if not active:
        raise UnderdeterminedSystemError(
            "All variables are dimensionless; there is nothing to reduce."
        )
    base_symbols = tuple(BASE_DIMENSIONS[i].symbol for i in active)

    # Dimensional matrix: rows = active base dimensions, columns = variables.
    matrix_rows: list[list[int]] = []
    for i in active:
        matrix_rows.append([v.dimension.as_int_vector()[i] for v in variables])
    dim_matrix = sp.Matrix(matrix_rows)

    rank = dim_matrix.rank()
    n_groups = n_variables - rank
    logger.debug("Matrix rank=%d -> %d dimensionless group(s)", rank, n_groups)

    if n_groups <= 0:
        raise UnderdeterminedSystemError(
            f"With {n_variables} variables and rank {rank}, the Pi theorem "
            f"predicts {n_groups} dimensionless groups. Add more variables or "
            f"remove dimensionally independent ones."
        )

    null_space = dim_matrix.nullspace()
    if len(null_space) != n_groups:
        raise InconsistentNullSpaceError(
            f"Expected {n_groups} null-space vectors but got {len(null_space)}."
        )

    groups = _build_groups(variables, null_space, integerize=integerize)
    product_latex = _product_latex(groups) if len(groups) > 1 else None

    return PiResult(
        variables=tuple(v.symbol for v in variables),
        base_symbols=base_symbols,
        matrix=tuple(tuple(row) for row in matrix_rows),
        rank=rank,
        n_variables=n_variables,
        n_groups=n_groups,
        groups=tuple(groups),
        product_latex=product_latex,
    )


# ---------------------------------------------------------------------- #
# Internal helpers                                                       #
# ---------------------------------------------------------------------- #
def _validate_inputs(variables: Sequence[Variable]) -> None:
    """Validate the variable list before any computation.

    Args:
        variables: Candidate variables.

    Raises:
        PiTheoremError: If there are fewer than two variables or symbols clash.
    """
    if len(variables) < 2:
        raise PiTheoremError("At least two variables are required.")
    symbols = [v.symbol for v in variables]
    duplicates = {s for s in symbols if symbols.count(s) > 1}
    if duplicates:
        raise PiTheoremError(f"Duplicate variable symbols: {sorted(duplicates)}.")


def _build_groups(
    variables: Sequence[Variable],
    null_space: list[sp.Matrix],
    *,
    integerize: bool,
) -> list[PiGroup]:
    """Convert null-space basis vectors into :class:`PiGroup` objects.

    Args:
        variables: The input variables (for symbols and LaTeX).
        null_space: SymPy column vectors spanning the matrix null space.
        integerize: Whether to scale exponents to the smallest integers.

    Returns:
        One :class:`PiGroup` per basis vector.
    """
    groups: list[PiGroup] = []
    for index, basis_vector in enumerate(null_space, start=1):
        exponents = [Fraction(int(x.p), int(x.q)) for x in basis_vector]
        if integerize:
            exponents = _integerize(exponents)
        int_exponents = tuple(int(e) for e in exponents) if integerize else None

        latex = _group_latex(index, variables, exponents)
        ascii_form = _group_ascii(index, variables, exponents)
        groups.append(
            PiGroup(
                index=index,
                exponents=int_exponents if int_exponents is not None else (),
                latex=latex,
                ascii=ascii_form,
            )
        )
    return groups


def _integerize(exponents: list[Fraction]) -> list[Fraction]:
    """Scale a rational exponent vector to the smallest integers.

    The vector is multiplied by the least common multiple of the denominators,
    divided by the greatest common divisor of the resulting numerators, and
    sign-normalised so the first non-zero exponent is positive.

    Args:
        exponents: Rational exponents of a single group.

    Returns:
        An equivalent vector of integer-valued fractions.
    """
    denominators = [e.denominator for e in exponents]
    multiplier = reduce(_lcm, denominators, 1)
    scaled = [int(e * multiplier) for e in exponents]

    non_zero = [abs(value) for value in scaled if value != 0]
    common = reduce(gcd, non_zero, 0)
    if common > 1:
        scaled = [value // common for value in scaled]

    for value in scaled:
        if value != 0:
            if value < 0:
                scaled = [-v for v in scaled]
            break
    return [Fraction(value) for value in scaled]


def _lcm(a: int, b: int) -> int:
    """Return the least common multiple of two integers.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        ``lcm(a, b)``; ``0`` if either argument is ``0``.
    """
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def _group_latex(index: int, variables: Sequence[Variable], exponents: Sequence[Fraction]) -> str:
    """Render a single group as ``\\Pi_{i} = \\dfrac{num}{den}`` LaTeX.

    Positive exponents go to the numerator, negative ones to the denominator, so
    the result reads like a conventional dimensionless number.

    Args:
        index: 1-based group index.
        variables: Input variables (for LaTeX symbols).
        exponents: This group's exponents (one per variable).

    Returns:
        A LaTeX equation string.
    """
    numerator: list[str] = []
    denominator: list[str] = []
    for variable, exponent in zip(variables, exponents):
        if exponent == 0:
            continue
        magnitude = abs(exponent)
        factor = _latex_power(variable.display_latex, magnitude)
        (numerator if exponent > 0 else denominator).append(factor)

    if not numerator and not denominator:
        body = "1"
    elif not denominator:
        body = r"\,".join(numerator)
    elif not numerator:
        body = r"\dfrac{1}{" + r"\,".join(denominator) + "}"
    else:
        body = r"\dfrac{" + r"\,".join(numerator) + "}{" + r"\,".join(denominator) + "}"
    return rf"\Pi_{{{index}}} = {body}"


def _group_ascii(index: int, variables: Sequence[Variable], exponents: Sequence[Fraction]) -> str:
    """Render a single group as a copy-pasteable ASCII expression.

    Args:
        index: 1-based group index.
        variables: Input variables (for plain symbols).
        exponents: This group's exponents (one per variable).

    Returns:
        A string such as ``"Pi_1 = rho*v**2/DeltaP"``.
    """
    numerator: list[str] = []
    denominator: list[str] = []
    for variable, exponent in zip(variables, exponents):
        if exponent == 0:
            continue
        magnitude = abs(exponent)
        token = (
            variable.symbol
            if magnitude == 1
            else f"{variable.symbol}**{_fraction_str(magnitude)}"
        )
        (numerator if exponent > 0 else denominator).append(token)

    num = "*".join(numerator) if numerator else "1"
    if denominator:
        den = "*".join(denominator)
        if len(denominator) > 1:
            return f"Pi_{index} = {num}/({den})"
        return f"Pi_{index} = {num}/{den}"
    return f"Pi_{index} = {num}"


def _product_latex(groups: Sequence[PiGroup]) -> str:
    """Build the LaTeX of the product of all groups (legacy behaviour).

    The original tool displayed the product of every :math:`\\Pi_i`; we keep this
    as an extra, optional line in the results.

    Args:
        groups: The computed groups.

    Returns:
        LaTeX such as ``"\\Pi_{1}\\,\\Pi_{2} = ..."``.
    """
    lhs = r"\,".join(rf"\Pi_{{{g.index}}}" for g in groups)
    # The product of dimensionless groups is itself dimensionless; we present the
    # symbolic product of their right-hand sides for completeness.
    rhs_parts = [g.latex.split("=", 1)[1].strip() for g in groups]
    rhs = r"\cdot".join(f"\\left({part}\\right)" for part in rhs_parts)
    return f"{lhs} = {rhs}"


def _latex_power(symbol: str, exponent: Fraction) -> str:
    """Render ``symbol`` raised to ``exponent`` in LaTeX.

    Args:
        symbol: LaTeX of the base symbol.
        exponent: A positive exponent (sign handled by the caller).

    Returns:
        ``symbol`` for an exponent of 1, otherwise ``symbol^{exponent}``.
    """
    if exponent == 1:
        return symbol
    return f"{symbol}^{{{_fraction_str(exponent)}}}"


def _fraction_str(value: Fraction) -> str:
    """Format a fraction as ``"2"`` or ``"1/2"``.

    Args:
        value: The fraction to format.

    Returns:
        The compact textual form.
    """
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _escape_latex(symbol: str) -> str:
    """Best-effort escaping of a raw symbol for LaTeX math mode.

    Args:
        symbol: A plain identifier such as ``"DeltaP"`` or ``"y_v"``.

    Returns:
        A LaTeX-friendly version (common Greek names mapped to commands, the
        first underscore preserved as a subscript group).
    """
    greek = {
        "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta",
        "iota", "kappa", "lambda", "mu", "nu", "xi", "pi", "rho", "sigma",
        "tau", "phi", "chi", "psi", "omega",
    }
    base, _, sub = symbol.partition("_")
    rendered = f"\\{base}" if base.lower() in greek else base
    if base[:1].isupper() and base.lower() in greek:
        rendered = f"\\{base.capitalize()}"
    if sub:
        rendered = f"{rendered}_{{{sub}}}"
    return rendered
