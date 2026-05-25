"""Pyodide bridge between the browser and the Pi-Scope engine.

This thin module is loaded into the Pyodide runtime (see ``pyodideEngine.ts``).
It exposes a single ``solve_payload`` function that accepts a JSON string,
drives the *same* :mod:`app.core` engine that powers the FastAPI backend, and
returns a JSON string with exactly the shape of the ``PiResultOut`` API model.

Exchanging plain JSON strings (rather than live proxies) keeps the
JavaScript <-> Python boundary simple and robust.
"""

from __future__ import annotations

import json

from app.core import Dimension, Variable, solve_pi_groups
from app.core.exceptions import PiTheoremError


def solve_payload(payload: str) -> str:
    """Solve a Pi-theorem request encoded as JSON.

    Args:
        payload: JSON string ``{"variables": [...], "integerize": bool}`` where
            each variable is ``{"symbol", "exponents", "latex"?, "name"?}``.

    Returns:
        A JSON string. On success it matches the ``PiResultOut`` API schema; on a
        domain error it is ``{"error": "<message>"}`` (mapped to a 422 in JS).
    """
    data = json.loads(payload)
    variables = [
        Variable(
            symbol=item["symbol"],
            dimension=Dimension.from_vector(list(item["exponents"])),
            latex=item.get("latex"),
            name=item.get("name"),
        )
        for item in data["variables"]
    ]

    try:
        result = solve_pi_groups(variables, integerize=data.get("integerize", True))
    except PiTheoremError as exc:
        return json.dumps({"error": str(exc)})

    return json.dumps(
        {
            "variables": list(result.variables),
            "base_symbols": list(result.base_symbols),
            "matrix": [list(row) for row in result.matrix],
            "rank": result.rank,
            "n_variables": result.n_variables,
            "n_groups": result.n_groups,
            "groups": [
                {
                    "index": group.index,
                    "exponents": list(group.exponents),
                    "latex": group.latex,
                    "ascii": group.ascii,
                }
                for group in result.groups
            ],
            "product_latex": result.product_latex,
        }
    )
