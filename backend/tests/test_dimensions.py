"""Unit tests for the dimensional model (:mod:`app.core.dimensions`)."""

from __future__ import annotations

from fractions import Fraction

import pytest

from app.core.dimensions import (
    BASE_SYMBOLS,
    NB_BASE_DIMENSIONS,
    Dimension,
    active_dimension_indices,
    get_base_dimension,
)
from app.core.exceptions import DimensionError


def test_seven_base_dimensions():
    assert NB_BASE_DIMENSIONS == 7
    assert BASE_SYMBOLS[:3] == ("M", "L", "T")


def test_from_vector_zero_pads_legacy_mlt():
    # A legacy [M, L, T] vector must still be valid.
    dim = Dimension.from_vector([1, -1, -2])
    assert dim.exponents == (
        Fraction(1), Fraction(-1), Fraction(-2),
        Fraction(0), Fraction(0), Fraction(0), Fraction(0),
    )


def test_from_vector_rejects_too_long():
    with pytest.raises(DimensionError):
        Dimension.from_vector([1, 2, 3, 4, 5, 6, 7, 8])


def test_from_mapping_by_symbol_and_name():
    by_symbol = Dimension.from_mapping({"M": 1, "L": -1, "T": -2})
    by_name = Dimension.from_mapping({"mass": 1, "length": -1, "time": -2})
    assert by_symbol == by_name


def test_from_mapping_unknown_symbol():
    with pytest.raises(DimensionError):
        Dimension.from_mapping({"Q": 1})


def test_is_dimensionless():
    assert Dimension.from_vector([0, 0, 0]).is_dimensionless
    assert not Dimension.from_vector([0, 1, 0]).is_dimensionless


def test_to_latex_pressure():
    # Dynamic pressure: M L^-1 T^-2
    assert Dimension.from_vector([1, -1, -2]).to_latex() == "M\\,L^{-1}\\,T^{-2}"


def test_to_latex_dimensionless():
    assert Dimension.from_vector([0, 0, 0]).to_latex() == "1"


def test_active_dimension_indices():
    dims = [Dimension.from_vector([1, -3, 0]), Dimension.from_vector([0, 1, -1])]
    # Only M, L, T (indices 0, 1, 2) are used.
    assert active_dimension_indices(dims) == [0, 1, 2]


def test_get_base_dimension():
    assert get_base_dimension("T").si_unit == "s"
    with pytest.raises(DimensionError):
        get_base_dimension("?")
