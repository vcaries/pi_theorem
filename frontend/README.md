# Pi-Scope · Frontend

React + TypeScript + Vite + Tailwind UI for the Pi-Scope API.

## Run

```bash
npm install
npm run dev        # http://localhost:5173
```

The dev server proxies `/api` to the backend on port 8000 (see `vite.config.ts`),
so start the backend first.

## Scripts

| Command | Description |
| --- | --- |
| `npm run dev` | Start the Vite dev server. |
| `npm run build` | Type-check and build the production bundle to `dist/`. |
| `npm run typecheck` | Type-check without emitting. |
| `npm run lint` | Lint with ESLint. |

## Layout

```
src/
├── api/         # Typed fetch client
├── store/       # Zustand store (variables, library, examples, result)
├── components/  # UI components
├── hooks/       # useTheme
├── i18n/        # i18next + fr/en bundles
├── lib/         # KaTeX wrapper, formatting, export, constants
└── types/       # API contract mirror
```

## Configuration

`VITE_API_URL` overrides the API base URL (defaults to `/api` via the dev proxy).
See `.env.example`.
