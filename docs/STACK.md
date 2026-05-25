# Technology stack & rationale

Every choice below optimises for three goals stated in the project brief:
**(1)** keep Python as the scientific core, **(2)** present a modern, professional
web UI, and **(3)** stay easy to run locally and to deploy later.

## Backend

| Technology | Why it was chosen | Alternatives considered |
| --- | --- | --- |
| **Python 3.10+** | The original engine is Python; it remains the lingua franca of scientific computing. | — |
| **SymPy** | Exact symbolic linear algebra (rational null space) — no floating-point error in the exponents. Already used by the original script. | NumPy (floating point; rank/null-space less exact), hand-rolled fractions |
| **FastAPI** | Modern, async, automatic OpenAPI docs, first-class Pydantic integration, tiny boilerplate. Ideal for a typed scientific API. | Flask (no built-in validation/docs), Django (too heavy for a small API) |
| **Pydantic v2** | Declarative validation and serialisation; the schemas *are* the API contract and the OpenAPI spec. | dataclasses + manual validation, marshmallow |
| **pydantic-settings** | Typed, environment-driven configuration with `.env` support. | python-dotenv + manual parsing |
| **uvicorn** | Fast ASGI server, the de-facto standard for FastAPI. | hypercorn, gunicorn+workers |
| **PyYAML** | Human-editable variable library and examples (non-developers can extend them). | JSON (less friendly for hand editing), TOML |
| **pytest** | Concise, powerful testing with fixtures; integrates with coverage. | unittest |
| **Ruff + Mypy** | Ruff = ultra-fast lint + format (PEP 8, imports, docstrings); Mypy = static typing. | flake8 + black + isort (slower, more config) |

## Frontend

| Technology | Why it was chosen | Alternatives considered |
| --- | --- | --- |
| **React 18** | The most widely recognised UI library — the safest, most "portfolio-legible" choice. | Vue, Svelte (excellent, but less expected by reviewers) |
| **TypeScript** | End-to-end typing; the frontend types mirror the backend schema for a safe contract. | plain JavaScript (no compile-time safety) |
| **Vite** | Instant dev server, fast builds, simple config, first-class TS/React support. | Create React App (deprecated), webpack (heavy config) |
| **Tailwind CSS** | Rapid, consistent, themeable styling; trivial dark mode via the `class` strategy. | CSS Modules, styled-components, MUI (opinionated look) |
| **KaTeX** | Fast, dependency-light, server-safe LaTeX rendering — perfect for equations. | MathJax (heavier, slower first paint) |
| **i18next / react-i18next** | Mature, ergonomic internationalisation with interpolation and persistence. | react-intl, hand-rolled dictionaries |
| **Zustand** | Minimal global state without boilerplate; perfect for a single app store. | Redux Toolkit (overkill here), React Context (re-render churn) |
| **lucide-react** | Clean, consistent, tree-shakeable icon set. | react-icons, hand-drawn SVGs |

## Tooling & operations

| Technology | Purpose |
| --- | --- |
| **Docker + Docker Compose** | One-command full-stack run; identical environments; easy future deploy. |
| **GitHub Actions** | CI (lint, type-check, test, build) on every push/PR; release automation on tags. |
| **pre-commit** | Catch formatting/lint issues before they reach CI. |
| **Make** | A discoverable, language-agnostic task runner (`make help`). |
| **EditorConfig + .gitattributes** | Consistent line endings and indentation across OSes (fixes Windows CRLF churn). |

## Why not run Python in the browser (Pyodide)?

It was a strong candidate (it would allow a fully static GitHub Pages demo while
keeping the Python engine). It was set aside for the first version because the
brief prioritised a **clean frontend/backend separation** and a **local-first**
experience. The decoupled design keeps Pyodide on the table as a future,
deploy-anywhere option — see [`FUTURE.md`](FUTURE.md).
