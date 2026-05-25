# Pi-Scope · Backend

FastAPI service wrapping the Buckingham Π (Vaschy–Buckingham) theorem engine.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8000
```

Interactive docs: <http://localhost:8000/docs>.

## Layout

```
app/
├── core/        # Pure engine (no web deps): dimensions, pi_theorem, exceptions
├── api/         # Routers: health, pi, library, examples
├── models/      # Pydantic schemas (API contract)
├── services/    # library / examples / solver adapter
├── data/        # library.yaml, examples.yaml
├── config.py    # pydantic-settings configuration
└── main.py      # FastAPI application factory
```

## Using the engine directly (no server)

```python
from app.core import Dimension, Variable, solve_pi_groups

variables = [
    Variable("rho", Dimension.from_vector([1, -3, 0])),
    Variable("V",   Dimension.from_vector([0, 1, -1])),
    Variable("D",   Dimension.from_vector([0, 1, 0])),
    Variable("mu",  Dimension.from_vector([1, -1, -1])),
]
result = solve_pi_groups(variables)
for group in result.groups:
    print(group.ascii)        # Pi_1 = rho*V*D/mu   (the Reynolds number)
```

Exponent vectors are ordered `[M, L, T, Θ, I, N, J]` and may be shorter
(trailing zeros are implied).

## Quality

```bash
pytest                 # tests (engine + API)
ruff check . && mypy app
```

## Configuration

Environment variables are prefixed `PISCOPE_` (see `.env.example`):
`PISCOPE_DEBUG`, `PISCOPE_LOG_LEVEL`, `PISCOPE_CORS_ORIGINS`.
