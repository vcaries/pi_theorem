# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

_Nothing yet._

## [1.0.0] - 2026-05-25

### Added

- **Scientific engine** extended from 3 (M, L, T) to the **7 SI base dimensions**
  (M, L, T, Θ, I, N, J), with exact rational arithmetic via SymPy.
- Structured results: dimensional matrix, rank, group count, and each Π group as
  integer-reduced exponents plus LaTeX and ASCII renderings.
- **FastAPI backend** with `health`, `pi/solve`, `library`, and `examples`
  endpoints, typed Pydantic schemas, centralised configuration and logging.
- **Curated variable library** (YAML) across mechanics, fluid mechanics,
  thermodynamics, heat transfer, electromagnetism, acoustics, energetics and
  aerodynamics.
- **Worked examples** including the flagship Chen (1990) compressor tip-clearance
  case, plus Reynolds, drag-on-a-sphere and forced-convection.
- **React + TypeScript + Tailwind frontend**: variable form/table, library
  browser, examples menu, dimensional-matrix view, Π-group cards with KaTeX,
  light/dark themes, FR/EN internationalisation, and JSON/LaTeX export.
- **Tooling & ops:** pytest suite, Ruff + Mypy, ESLint, Docker images and
  `docker-compose`, GitHub Actions CI, issue/PR templates, pre-commit, Makefile,
  and full documentation under `docs/`.

### Changed

- Reworked the original `apply_pi_theorem` (which printed to stdout) into
  `solve_pi_groups`, returning a rich, serialisable `PiResult`.

### Preserved

- The original PyQt5 desktop script is kept under `legacy/` for provenance.

[Unreleased]: https://github.com/vcaries/pi-scope/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/vcaries/pi-scope/releases/tag/v1.0.0
