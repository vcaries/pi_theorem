// Sync the vendored Python engine used by the Pyodide build with the canonical
// source in `backend/app/core`. The backend remains the single source of truth;
// this copies the exact same files the FastAPI server uses into the frontend so
// they can be bundled as raw assets and loaded into Pyodide.
//
// Run automatically before dev/build via the `predev` / `prebuild` npm scripts,
// or manually with: `node scripts/sync-pyodide-core.mjs`.
import { copyFileSync, mkdirSync } from "node:fs";
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

for (const file of files) {
  const from = resolve(backendCore, file);
  const to = resolve(vendor, file);
  mkdirSync(dirname(to), { recursive: true });
  copyFileSync(from, to);
}

console.log(`Synced ${files.length} engine files from backend/app -> frontend vendor.`);
