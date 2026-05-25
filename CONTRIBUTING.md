# Contributing to Pi-Scope

Thanks for your interest in improving Pi-Scope! This guide gets you productive
quickly. For the full process (branching, commits, releases) see
[`docs/GIT_GUIDE.md`](docs/GIT_GUIDE.md).

## Getting started

```bash
git clone https://github.com/vcaries/pi-scope.git
cd pi-scope

# Backend
cd backend && pip install -r requirements-dev.txt && cd ..
# Frontend
cd frontend && npm install && cd ..

# Run both (two terminals)
make dev-backend
make dev-frontend
```

Optional but recommended:

```bash
pip install pre-commit && pre-commit install
```

## Development workflow

1. Create a branch off `main`: `git switch -c feat/my-feature`.
2. Make focused commits using **Conventional Commits**
   (e.g. `feat(engine): name common dimensionless groups`).
3. Keep things green:

   ```bash
   cd backend && pytest && ruff check . && mypy app
   cd frontend && npm run typecheck && npm run lint && npm run build
   ```

4. Add an entry to `CHANGELOG.md` under **Unreleased**.
5. Open a pull request and fill in the template.

## Coding standards

- **Python:** PEP 8, type hints everywhere, **Google-style docstrings**
  (`Args`, `Returns`, `Raises`). Ruff enforces lint + format; Mypy enforces types.
- **TypeScript:** `strict` mode, no `any` without justification, ESLint clean.
- **Tests:** new behaviour ships with tests. The engine and API are covered by
  `backend/tests/`.
- **i18n:** user-facing strings go in `frontend/src/i18n/{fr,en}.json` — never
  hard-coded.
- **Accessibility:** interactive elements are labelled and keyboard-operable.

## Adding a library variable or example

Both are plain YAML — no code required:

- Variables: `backend/app/data/library.yaml` (exponents in order
  `[M, L, T, Θ, I, N, J]`; trailing zeros may be omitted).
- Examples: `backend/app/data/examples.yaml`.

Run `pytest` afterwards: the schemas validate your additions automatically.

## Reporting bugs & requesting features

Use the issue templates (Bug report / Feature request). Include reproduction
steps, expected vs actual behaviour, and your environment.

## Code of conduct

By participating you agree to abide by our
[Code of Conduct](CODE_OF_CONDUCT.md).
