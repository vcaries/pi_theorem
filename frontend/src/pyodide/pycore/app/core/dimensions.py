"""Definition of the SI base dimensions and the :class:`Dimension` value object.

The International System of Units (SI) is built on seven mutually independent
base dimensions. Every physical quantity has a *dimensional formula* that is a
product of integer powers of these base dimensions. This module encodes that
model in a small, immutable, well-tested value object that the Buckingham Pi
engine consumes.

The chosen ordering keeps ``M``, ``L`` and ``T`` first so that legacy
three-dimensional inputs (the original ``[M, L, T]`` vectors of the project)
map onto the first three components without any conversion.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction

from app.core.exceptions import DimensionError


@dataclass(frozen=True, slots=True)
class BaseDimension:
    """A single SI base dimension.

    Attributes:
        symbol: One-character physics symbol (e.g. ``"M"`` for mass).
        name: Machine-friendly snake_case name (e.g. ``"mass"``).
        si_unit: The coherent SI unit of this base dimension (e.g. ``"kg"``).
        label_en: Human-readable English label.
        label_fr: Human-readable French label.
    """

    symbol: str
    name: str
    si_unit: str
    label_en: str
    label_fr: str


#: The seven SI base dimensions, in the canonical order used everywhere in the
#: engine. ``M``, ``L`` and ``T`` come first for backward compatibility with the
#: original three-dimensional model.
BASE_DIMENSIONS: tuple[BaseDimension, ...] = (
    BaseDimension("M", "mass", "kg", "Mass", "Masse"),
    BaseDimension("L", "length", "m", "Length", "Longueur"),
    BaseDimension("T", "time", "s", "Time", "Temps"),
    BaseDimension("Θ", "temperature", "K", "Temperature", "Température"),
    BaseDimension("I", "electric_current", "A", "Electric current", "Courant électrique"),
    BaseDimension("N", "amount_of_substance", "mol", "Amount of substance", "Quantité de matière"),
    BaseDimension("J", "luminous_intensity", "cd", "Luminous intensity", "Intensité lumineuse"),
)

#: Number of SI base dimensions (7).
NB_BASE_DIMENSIONS: int = len(BASE_DIMENSIONS)

#: Fast lookup from a base-dimension symbol to its index in :data:`BASE_DIMENSIONS`.
_SYMBOL_TO_INDEX: dict[str, int] = {dim.symbol: i for i, dim in enumerate(BASE_DIMENSIONS)}

#: Ordered tuple of base-dimension symbols, e.g. ``("M", "L", "T", "Θ", "I", "N", "J")``.
BASE_SYMBOLS: tuple[str, ...] = tuple(dim.symbol for dim in BASE_DIMENSIONS)


@dataclass(frozen=True, slots=True)
class Dimension:
    """An immutable dimensional formula expressed in the SI base dimensions.

    Internally the formula is stored as a 7-tuple of :class:`fractions.Fraction`
    exponents aligned with :data:`BASE_DIMENSIONS`. Fractions are used so that
    intermediate results (e.g. the null-space basis of the dimensional matrix)
    remain exact, avoiding floating-point drift.

    Example:
        A dynamic pressure has the formula ``M L^-1 T^-2``::

            >>> Dimension.from_mapping({"M": 1, "L": -1, "T": -2}).to_latex()
            'M\\\\,L^{-1}\\\\,T^{-2}'
    """

    exponents: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        """Validate the internal representation.

        Raises:
            DimensionError: If the number of exponents does not match the number
                of SI base dimensions.
        """
        if len(self.exponents) != NB_BASE_DIMENSIONS:
            raise DimensionError(
                f"A dimensional formula needs exactly {NB_BASE_DIMENSIONS} "
                f"exponents, got {len(self.exponents)}."
            )

    # ------------------------------------------------------------------ #
    # Constructors                                                       #
    # ------------------------------------------------------------------ #
    @classmethod
    def from_vector(cls, vector: Sequence[float | int | Fraction | str]) -> Dimension:
        """Build a dimension from an ordered exponent vector.

        The vector may be shorter than seven entries; missing trailing
        components default to zero. This keeps legacy ``[M, L, T]`` inputs valid.

        Args:
            vector: Exponents aligned with :data:`BASE_DIMENSIONS` (M, L, T, ...).

        Returns:
            The corresponding :class:`Dimension`.

        Raises:
            DimensionError: If the vector is longer than seven entries or an
                exponent cannot be interpreted as a rational number.
        """
        if len(vector) > NB_BASE_DIMENSIONS:
            raise DimensionError(
                f"Exponent vector has {len(vector)} entries, "
                f"expected at most {NB_BASE_DIMENSIONS}."
            )
        padded = list(vector) + [0] * (NB_BASE_DIMENSIONS - len(vector))
        return cls(tuple(_to_fraction(value) for value in padded))

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, float | int | Fraction | str]) -> Dimension:
        """Build a dimension from a ``{symbol: exponent}`` mapping.

        Args:
            mapping: Keys are base-dimension symbols (``"M"``, ``"L"``, ...) or
                their snake_case names (``"mass"``, ``"length"``, ...); values
                are exponents. Omitted base dimensions are treated as zero.

        Returns:
            The corresponding :class:`Dimension`.

        Raises:
            DimensionError: If a key is not a recognised base dimension or an
                exponent is not a rational number.
        """
        exponents = [Fraction(0)] * NB_BASE_DIMENSIONS
        for key, value in mapping.items():
            index = _resolve_symbol(key)
            exponents[index] = _to_fraction(value)
        return cls(tuple(exponents))

    # ------------------------------------------------------------------ #
    # Queries                                                            #
    # ------------------------------------------------------------------ #
    @property
    def is_dimensionless(self) -> bool:
        """bool: ``True`` if every exponent is zero (a pure number)."""
        return all(exponent == 0 for exponent in self.exponents)

    def as_int_vector(self) -> list[int]:
        """Return the exponents as plain integers.

        Returns:
            The seven exponents as ``int`` values.

        Raises:
            DimensionError: If any exponent is not integral (base dimensions are
                always integral by construction, so this signals a bug upstream).
        """
        result: list[int] = []
        for exponent in self.exponents:
            if exponent.denominator != 1:
                raise DimensionError(f"Non-integer base exponent: {exponent}.")
            result.append(int(exponent))
        return result

    # ------------------------------------------------------------------ #
    # Rendering                                                          #
    # ------------------------------------------------------------------ #
    def to_latex(self) -> str:
        """Render the dimensional formula as a LaTeX string.

        Returns:
            A LaTeX fragment such as ``"M\\,L^{-1}\\,T^{-2}"`` or ``"1"`` for a
            dimensionless quantity.
        """
        if self.is_dimensionless:
            return "1"
        parts: list[str] = []
        for symbol, exponent in zip(BASE_SYMBOLS, self.exponents):
            if exponent == 0:
                continue
            if exponent == 1:
                parts.append(symbol)
            else:
                parts.append(f"{symbol}^{{{_format_fraction(exponent)}}}")
        return "\\,".join(parts)

    def __str__(self) -> str:
        """Return a compact ASCII representation, e.g. ``"M L^-1 T^-2"``."""
        if self.is_dimensionless:
            return "[-]"
        parts: list[str] = []
        for symbol, exponent in zip(BASE_SYMBOLS, self.exponents):
            if exponent == 0:
                continue
            parts.append(symbol if exponent == 1 else f"{symbol}^{_format_fraction(exponent)}")
        return " ".join(parts)


# ---------------------------------------------------------------------- #
# Module-level helpers                                                   #
# ---------------------------------------------------------------------- #
def get_base_dimension(symbol: str) -> BaseDimension:
    """Look up a base dimension by its symbol.

    Args:
        symbol: A base-dimension symbol, e.g. ``"L"``.

    Returns:
        The matching :class:`BaseDimension`.

    Raises:
        DimensionError: If ``symbol`` is not an SI base dimension.
    """
    index = _SYMBOL_TO_INDEX.get(symbol)
    if index is None:
        raise DimensionError(f"Unknown base dimension symbol: {symbol!r}.")
    return BASE_DIMENSIONS[index]


def active_dimension_indices(dimensions: Iterable[Dimension]) -> list[int]:
    """Return the indices of base dimensions that appear in *any* input.

    Reducing the dimensional matrix to its active rows keeps the matrix shown to
    the user compact and readable (no all-zero rows for unused dimensions).

    Args:
        dimensions: The dimensional formulae of the problem's variables.

    Returns:
        Sorted indices into :data:`BASE_DIMENSIONS` of dimensions with at least
        one non-zero exponent across the inputs.
    """
    active: set[int] = set()
    for dimension in dimensions:
        for index, exponent in enumerate(dimension.exponents):
            if exponent != 0:
                active.add(index)
    return sorted(active)


def _resolve_symbol(key: str) -> int:
    """Resolve a base-dimension key (symbol or name) to its index.

    Args:
        key: A symbol (``"M"``) or snake_case name (``"mass"``).

    Returns:
        The index into :data:`BASE_DIMENSIONS`.

    Raises:
        DimensionError: If the key matches no base dimension.
    """
    if key in _SYMBOL_TO_INDEX:
        return _SYMBOL_TO_INDEX[key]
    for index, dimension in enumerate(BASE_DIMENSIONS):
        if key == dimension.name:
            return index
    raise DimensionError(f"Unknown base dimension key: {key!r}.")


def _to_fraction(value: float | int | Fraction | str) -> Fraction:
    """Convert an arbitrary numeric input to an exact :class:`Fraction`.

    Args:
        value: An int, float, :class:`Fraction`, or numeric string.

    Returns:
        The value as an exact fraction.

    Raises:
        DimensionError: If the value cannot be parsed as a rational number.
    """
    try:
        if isinstance(value, float):
            # ``Fraction(0.1)`` is exact-but-ugly; limit the denominator so that
            # user-entered decimals such as 0.5 become 1/2 rather than a huge
            # binary fraction.
            return Fraction(value).limit_denominator(10_000)
        return Fraction(value)
    except (ValueError, ZeroDivisionError, TypeError) as exc:
        raise DimensionError(f"Cannot interpret {value!r} as a rational exponent.") from exc


def _format_fraction(value: Fraction) -> str:
    """Format a fraction for display (``"2"``, ``"-1"``, ``"1/2"``).

    Args:
        value: The fraction to format.

    Returns:
        A compact string without a trailing ``/1`` for integral values.
    """
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"
