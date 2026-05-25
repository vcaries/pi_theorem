/**
 * Pyodide engine: runs the genuine Python + SymPy Pi-theorem engine entirely in
 * the browser via WebAssembly. No server required — this is what powers the
 * static GitHub Pages demo.
 *
 * Strategy:
 *  - lazily inject the Pyodide runtime from a CDN on first use;
 *  - load the `sympy` package;
 *  - write the *vendored* `app.core` engine (the exact backend code) and the
 *    bridge into Pyodide's virtual filesystem, then import them;
 *  - exchange plain JSON strings across the JS <-> Python boundary.
 *
 * The curated library and worked examples are served as static JSON (generated
 * from the backend YAML at build time), so they need no Python at all.
 */
import { ApiError } from "@/api/client";
import type { PiEngine } from "@/api/engine";
import type {
  LibraryResponse,
  PiResultOut,
  VariableIn,
  WorkedExample,
} from "@/types";

// The vendored Python engine (kept in sync with backend/app/core), bundled as
// raw strings and written into the Pyodide filesystem at runtime.
import appInit from "@/pyodide/pycore/app/__init__.py?raw";
import coreInit from "@/pyodide/pycore/app/core/__init__.py?raw";
import dimensionsPy from "@/pyodide/pycore/app/core/dimensions.py?raw";
import exceptionsPy from "@/pyodide/pycore/app/core/exceptions.py?raw";
import piTheoremPy from "@/pyodide/pycore/app/core/pi_theorem.py?raw";
import bridgePy from "@/pyodide/pycore/bridge.py?raw";

const PYODIDE_VERSION = "0.26.4";
const PYODIDE_CDN = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;

// Minimal typing for the bits of the Pyodide API we use.
interface PyodideRuntime {
  loadPackage(names: string | string[]): Promise<void>;
  runPython(code: string): unknown;
  globals: { set(name: string, value: unknown): void };
  FS: {
    mkdirTree(path: string): void;
    writeFile(path: string, data: string): void;
  };
}

declare global {
  interface Window {
    loadPyodide?: (config: { indexURL: string }) => Promise<PyodideRuntime>;
  }
}

let pyodidePromise: Promise<PyodideRuntime> | null = null;

/** Inject a `<script>` once and resolve when it has loaded. */
function injectScript(src: string): Promise<void> {
  return new Promise((resolve, reject) => {
    if (document.querySelector(`script[src="${src}"]`)) {
      resolve();
      return;
    }
    const script = document.createElement("script");
    script.src = src;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error(`Failed to load ${src}`));
    document.head.appendChild(script);
  });
}

/** Download, boot and provision the Pyodide runtime exactly once. */
async function bootPyodide(): Promise<PyodideRuntime> {
  await injectScript(`${PYODIDE_CDN}pyodide.js`);
  if (!window.loadPyodide) {
    throw new Error("Pyodide failed to expose loadPyodide");
  }
  const pyodide = await window.loadPyodide({ indexURL: PYODIDE_CDN });
  await pyodide.loadPackage("sympy");

  // Recreate the `app/core` package inside the virtual filesystem.
  pyodide.FS.mkdirTree("/pycore/app/core");
  pyodide.FS.writeFile("/pycore/app/__init__.py", appInit);
  pyodide.FS.writeFile("/pycore/app/core/__init__.py", coreInit);
  pyodide.FS.writeFile("/pycore/app/core/dimensions.py", dimensionsPy);
  pyodide.FS.writeFile("/pycore/app/core/exceptions.py", exceptionsPy);
  pyodide.FS.writeFile("/pycore/app/core/pi_theorem.py", piTheoremPy);

  pyodide.runPython("import sys; sys.path.insert(0, '/pycore')");
  pyodide.runPython(bridgePy);
  return pyodide;
}

/** Memoised accessor: boots Pyodide on first call, reuses it afterwards. */
function getPyodide(): Promise<PyodideRuntime> {
  if (!pyodidePromise) {
    pyodidePromise = bootPyodide();
  }
  return pyodidePromise;
}

/** Fetch a bundled static JSON data file, respecting the deploy base path. */
async function fetchData<T>(file: string): Promise<T> {
  const response = await fetch(`${import.meta.env.BASE_URL}data/${file}`);
  if (!response.ok) {
    throw new ApiError(`Cannot load ${file} (status ${response.status})`, response.status);
  }
  return (await response.json()) as T;
}

export const pyodideEngine: PiEngine = {
  async prepare(): Promise<void> {
    await getPyodide();
  },

  async solvePiGroups(variables: VariableIn[], integerize = true): Promise<PiResultOut> {
    const pyodide = await getPyodide();
    pyodide.globals.set("_piscope_payload", JSON.stringify({ variables, integerize }));
    const resultJson = pyodide.runPython("solve_payload(_piscope_payload)") as string;
    const parsed = JSON.parse(resultJson) as PiResultOut & { error?: string };
    if (parsed.error) {
      throw new ApiError(parsed.error, 422);
    }
    return parsed;
  },

  fetchLibrary(): Promise<LibraryResponse> {
    return fetchData<LibraryResponse>("library.json");
  },

  fetchExamples(): Promise<WorkedExample[]> {
    return fetchData<WorkedExample[]>("examples.json");
  },
};
