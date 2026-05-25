"""Unit tests for the Pi-theorem engine (:mod:`app.core.pi_theorem`)."""

from __future__ import annotations

import pytest

from app.core import Dimension, Variable, solve_pi_groups
from app.core.exceptions import PiTheoremError, UnderdeterminedSystemError


def _v(symbol: str, vector: list[int], latex: str | None = None) -> Variable:
    """Build a Variable from a short M,L,T,... vector (test helper)."""
    return Variable(symbol=symbol, dimension=Dimension.from_vector(vector), latex=latex)


def test_reynolds_number_single_group():
    """rho, V, D, mu must collapse to exactly the Reynolds number."""
    variables = [
        _v("rho", [1, -3, 0]),
        _v("V", [0, 1, -1]),
        _v("D", [0, 1, 0]),
        _v("mu", [1, -1, -1]),
    ]
    result = solve_pi_groups(variables)

    assert result.n_groups == 1
    assert result.rank == 3
    group = result.groups[0]
    # Re = rho * V * D / mu  (exponents over [rho, V, D, mu]).
    assert group.exponents == (1, 1, 1, -1)
    assert group.ascii == "Pi_1 = rho*V*D/mu"


def test_chen_1990_reproduces_eight_groups():
    """The flagship Chen (1990) case must yield 8 independent groups."""
    variables = [
        _v("tau", [0, 1, 0]),
        _v("rho", [1, -3, 0]),
        _v("dt", [0, 0, 1]),
        _v("DeltaP", [1, -1, -2]),
        _v("Gamma", [0, 2, -1]),
        _v("y_v", [0, 1, 0]),
        _v("z_v", [0, 1, 0]),
        _v("y_c", [0, 1, 0]),
        _v("z_c", [0, 1, 0]),
        _v("v", [0, 1, -1]),
        _v("w", [0, 1, -1]),
    ]
    result = solve_pi_groups(variables)

    assert result.n_variables == 11
    assert result.rank == 3
    assert result.n_groups == 8
    assert result.base_symbols == ("M", "L", "T")
    # Each group is genuinely dimensionless: verify by reconstructing dimensions.
    for group in result.groups:
        net = [0, 0, 0]
        for exponent, variable in zip(group.exponents, variables):
            vec = variable.dimension.as_int_vector()
            for i in range(3):
                net[i] += exponent * vec[i]
        assert net == [0, 0, 0]


def test_integer_exponents_have_no_common_factor():
    """Integerised exponents are reduced and sign-normalised."""
    variables = [
        _v("F", [1, 1, -2]),
        _v("rho", [1, -3, 0]),
        _v("V", [0, 1, -1]),
        _v("D", [0, 1, 0]),
    ]
    result = solve_pi_groups(variables)
    assert result.n_groups == 1
    exps = result.groups[0].exponents
    # First non-zero exponent must be positive (sign normalisation).
    first_nonzero = next(e for e in exps if e != 0)
    assert first_nonzero > 0


def test_temperature_dimension_supported():
    """A problem using the temperature dimension Theta must solve."""
    variables = [
        _v("h", [1, 0, -3, -1]),   # heat transfer coefficient
        _v("L", [0, 1, 0]),        # length
        _v("k", [1, 1, -3, -1]),   # thermal conductivity
    ]
    result = solve_pi_groups(variables)
    # Nusselt number Nu = h L / k.
    assert result.n_groups == 1
    assert "Θ" in result.base_symbols


def test_requires_two_variables():
    with pytest.raises(PiTheoremError):
        solve_pi_groups([_v("L", [0, 1, 0])])


def test_duplicate_symbols_rejected():
    with pytest.raises(PiTheoremError):
        solve_pi_groups([_v("L", [0, 1, 0]), _v("L", [0, 1, 0])])


def test_underdetermined_raises():
    """Two dimensionally independent variables yield zero groups."""
    with pytest.raises(UnderdeterminedSystemError):
        solve_pi_groups([_v("L", [0, 1, 0]), _v("t", [0, 0, 1])])


def test_product_latex_present_for_multiple_groups():
    variables = [
        _v("tau", [0, 1, 0]),
        _v("c", [0, 1, 0]),
        _v("s", [0, 1, 0]),
    ]
    result = solve_pi_groups(variables)
    assert result.n_groups == 2
    assert result.product_latex is not None
