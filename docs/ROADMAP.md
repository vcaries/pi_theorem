# Development roadmap

The project is delivered in incremental, shippable milestones. Each milestone is
independently demoable — a deliberate choice so the work always looks like a
product, never a half-finished prototype.

## ✅ Milestone 0 — Foundations (this release, v1.0.0)

- [x] Web-free scientific engine extended to the **7 SI base dimensions**.
- [x] Exact, integer-reduced, sign-normalised Π groups with LaTeX + ASCII output.
- [x] FastAPI backend: `solve`, `library`, `examples`, `health` endpoints.
- [x] Curated variable library across 8 physics domains (YAML).
- [x] Worked examples incl. the flagship **Chen (1990)** case.
- [x] React + TS + Tailwind UI: variable table/form, library browser, results.
- [x] KaTeX equation rendering + explicit dimensional matrix.
- [x] Light/dark themes, **FR/EN** i18n, JSON/LaTeX export.
- [x] Test suite (engine + API), CI, Docker, full repo professionalisation.

## 🔜 Milestone 1 — Depth & polish

- [ ] **Editable** variable rows (in-place exponent editing) in the table.
- [ ] Live dimensional-formula preview while typing a custom variable.
- [ ] Name the well-known groups automatically (Reynolds, Mach, Nusselt, …).
- [ ] Choice of **repeating variables** to steer which groups are produced.
- [ ] Persist the working session (localStorage) and shareable URL state.
- [ ] Frontend unit/component tests (Vitest + Testing Library) and Playwright E2E.

## 🧭 Milestone 2 — Scientific power features

- [ ] Detect and warn about **dimensionally inconsistent** sets.
- [ ] Alternative group bases (let the user recombine groups).
- [ ] Symbolic relation builder: express a target variable via the others.
- [ ] Import/export problems as JSON; a small gallery of saved problems.
- [ ] CSV/Markdown export of the matrix and groups.

## 🚀 Milestone 3 — Reach & deployment

- [ ] **Pyodide** build: run the real Python engine in-browser for a 100% static
      GitHub Pages demo (see [`FUTURE.md`](FUTURE.md)).
- [ ] One-click deploy recipes (Render, Fly.io, Hugging Face Spaces).
- [ ] PWA / offline support.
- [ ] Public API rate limiting + caching for a hosted demo.

## Definition of done (per feature)

A feature is "done" when it is: typed, tested, documented, accessible
(keyboard + ARIA), internationalised (FR + EN), and passing CI.
