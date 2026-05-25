/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** Base URL of the Pi-Scope API (defaults to "/api" via the dev proxy). */
  readonly VITE_API_URL?: string;
  /** Active engine: "http" (FastAPI) or "pyodide" (in-browser). Defaults to http. */
  readonly VITE_ENGINE?: "http" | "pyodide";
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
