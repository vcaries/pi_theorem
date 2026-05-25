// Sync the vendored Python engine used by the Pyodide build with the canonical
// source in `backend/app/core`. The backend remains the single source of truth;
// this copies the exact same files the FastAPI server uses into the frontend so
// they can be bundled as raw assets and loaded into Pyodide.
//
// Runs automatically before dev/build via the `predev` / `prebuild` npm scripts,
// or manually with: `node scripts/sync-pyodide-core.mjs`.
//
// The vendored copies are also committed to the repository, so when the backend
// source is not present in the build context (e.g. the frontend-only Docker
// image), this script SKIPS gracefully and the committed copies are used.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const backendCore = resolve(here, "../../backend/app");
const vendor = resolve(here, "../src/pyodide/pycore/app");

const files = [
  "__init__.py",
  "core/__init__.py",
  "core/dimensions.py",
  "core/exceptions.py",
  "core/pi_theorem.py",
];

if (!existsSync(backendCore)) {
  console.log(
    "[sync-pyodide-core] backend source not found — using committed vendored copies (this is expected in the frontend-only Docker build).",
  );
  process.exit(0);
}

let copied = 0;
for (const file of files) {
  const from = resolve(backendCore, file);
  if (!existsSync(from)) continue;
  const to = resolve(vendor, file);
  mkdirSync(dirname(to), { recursive: true });
  copyFileSync(from, to);
  copied += 1;
}

console.log(`[sync-pyodide-core] synced ${copied} engine file(s) from backend/app -> frontend vendor.`);
