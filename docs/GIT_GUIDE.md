# Git & GitHub guide

A practical playbook for running Pi-Scope as a professional open-source product:
how the repository is structured, how branches and commits are organised, how
releases are cut, and how the project is maintained over time.

---

## 1. Repository structure

A clean monorepo with one obvious home for everything:

```
pi_theorem/
├── backend/      # Python service (own pyproject, tests, Dockerfile)
├── frontend/     # Web app (own package.json, Dockerfile)
├── docs/         # Design & process documentation
├── legacy/       # The original script, preserved for provenance
├── .github/      # CI/CD workflows, issue & PR templates
├── docker-compose.yml, Makefile
└── README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, CHANGELOG
```

Principles:

- **One concern per directory.** Backend and frontend are self-contained and
  could be split into separate repos later with no untangling.
- **Tooling config lives at the layer it configures** (`backend/pyproject.toml`,
  `frontend/.eslintrc.cjs`), while cross-cutting config (`.editorconfig`,
  `.gitattributes`, `.pre-commit-config.yaml`) lives at the root.
- **No build artefacts in Git** — `node_modules/`, `dist/`, `__pycache__/`,
  `.venv/` and `.env` are all git-ignored.

## 2. Branching strategy

A lightweight **trunk-based** flow with a stable `main` and short-lived branches.

| Branch | Purpose | Lifetime |
| --- | --- | --- |
| `main` | Always releasable. Protected. | permanent |
| `develop` *(optional)* | Integration branch if you prefer staged releases. | permanent |
| `feat/<slug>` | A new feature. | hours–days |
| `fix/<slug>` | A bug fix. | hours |
| `chore/<slug>` | Tooling, deps, docs, CI. | hours |
| `release/x.y.z` | Stabilise a release if needed. | short |

```bash
git switch -c feat/editable-variables       # branch off main
# …work, commit in small steps…
git push -u origin feat/editable-variables  # open a PR
```

**Rules of thumb:** branch off `main`, keep branches small and focused, rebase on
`main` before opening the PR, delete the branch after merge.

### Protecting `main`

In *Settings → Branches*, add a rule for `main`:

- Require a pull request before merging (≥ 1 approval).
- Require status checks to pass (the `CI` workflow).
- Require branches to be up to date before merging.
- Disallow force-pushes and deletions.

## 3. Commit conventions

This project uses **[Conventional Commits](https://www.conventionalcommits.org)**.
The format makes history readable *and* lets tools derive changelogs and version
bumps automatically.

```
<type>(<optional scope>): <short imperative summary>

<optional body explaining what & why>

<optional footer: BREAKING CHANGE:, Closes #123>
```

| Type | When to use | SemVer effect |
| --- | --- | --- |
| `feat` | A new user-facing feature | MINOR |
| `fix` | A bug fix | PATCH |
| `docs` | Documentation only | — |
| `style` | Formatting, no logic change | — |
| `refactor` | Code change, no behaviour change | — |
| `perf` | Performance improvement | PATCH |
| `test` | Add/adjust tests | — |
| `build`/`ci` | Build system or CI | — |
| `chore` | Maintenance, deps | — |

A `!` after the type (or a `BREAKING CHANGE:` footer) signals a **MAJOR** bump.

**Examples**

```
feat(engine): support the 7 SI base dimensions (Θ, I, N, J)
fix(api): return 422 instead of 500 for underdetermined systems
docs(readme): add Docker quick-start
refactor(core)!: return PiResult objects instead of printing

BREAKING CHANGE: apply_pi_theorem no longer prints; use solve_pi_groups.
```

## 4. Versioning

Pi-Scope follows **[Semantic Versioning](https://semver.org)**: `MAJOR.MINOR.PATCH`.

- **MAJOR** — incompatible API/behaviour change.
- **MINOR** — backwards-compatible feature.
- **PATCH** — backwards-compatible fix.

The version is kept in sync in three places: `backend/app/__init__.py`,
`backend/pyproject.toml`, and `frontend/package.json`. Update all three in the
release commit.

## 5. Releases

Releases are driven by **git tags**; pushing a `vX.Y.Z` tag triggers the
[`release.yml`](../.github/workflows/release.yml) workflow, which publishes a
GitHub Release.

```bash
# 1. Ensure main is green and CHANGELOG.md has an entry for the version.
# 2. Bump the version in the three files above.
git commit -am "chore(release): v1.1.0"

# 3. Tag and push.
git tag -a v1.1.0 -m "Pi-Scope v1.1.0"
git push origin main --follow-tags
```

Keep [`CHANGELOG.md`](../CHANGELOG.md) in the **Keep a Changelog** format: collect
changes under an `## [Unreleased]` heading as you merge PRs, then rename it to the
version with a date at release time.

## 6. Pull-request workflow

1. Open the PR from your `feat/…` branch; fill in the template.
2. CI runs lint, type-check, tests and Docker builds automatically.
3. Address review comments with additional commits (squash on merge).
4. Use **Squash and merge** so `main` keeps one clean, conventional commit per PR.
5. Delete the branch.

## 7. Maintaining an open-source project

- **Lower the barrier to entry:** a crisp README, a working `make dev-*`, and an
  honest "good first issue" label.
- **Templates do the triage:** issue forms capture the right info; the PR
  template enforces the checklist.
- **Automate quality:** CI + pre-commit mean reviewers discuss design, not
  formatting.
- **Document decisions:** the `docs/` folder records *why*, not just *how* — this
  is what separates a script from a product.
- **Be responsive and kind:** acknowledge issues quickly even if you can't fix
  them immediately; a `CODE_OF_CONDUCT.md` sets the tone.
- **Communicate change:** the changelog and release notes tell users what moved.

## 8. First push (from this repository)

```bash
# The repo already has history. Set the remote and push:
git remote -v                       # check origin
git add -A
git commit -m "feat: web application (FastAPI + React) for the Pi theorem"
git push origin main
```

If you start a fresh repository instead:

```bash
git init -b main
git add -A
git commit -m "feat: initial Pi-Scope web application"
git remote add origin git@github.com:vcaries/pi-scope.git
git push -u origin main
```
