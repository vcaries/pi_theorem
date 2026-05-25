/**
 * Engine abstraction.
 *
 * Pi-Scope can run against two interchangeable engines:
 *
 * - **http**   — calls the FastAPI backend (local development, future server).
 * - **pyodide** — runs the real Python + SymPy engine in the browser via
 *   WebAssembly, so the app is fully static (GitHub Pages, offline).
 *
 * The active engine is chosen at build time via `VITE_ENGINE`. The rest of the
 * app depends only on this `PiEngine` interface, never on a concrete transport.
 */
import * as httpClient from "@/api/client";
import { pyodideEngine } from "@/api/pyodideEngine";
import type {
  LibraryResponse,
  PiResultOut,
  VariableIn,
  WorkedExample,
} from "@/types";

export { ApiError } from "@/api/client";

/** Common contract implemented by every engine. */
export interface PiEngine {
  solvePiGroups(variables: VariableIn[], integerize?: boolean): Promise<PiResultOut>;
  fetchLibrary(): Promise<LibraryResponse>;
  fetchExamples(): Promise<WorkedExample[]>;
  /** Optional warm-up (e.g. download + boot Pyodide) for snappier first use. */
  prepare?(): Promise<void>;
}

const httpEngine: PiEngine = {
  solvePiGroups: httpClient.solvePiGroups,
  fetchLibrary: httpClient.fetchLibrary,
  fetchExamples: httpClient.fetchExamples,
};

/** Selected engine mode (`"http"` by default, `"pyodide"` for static builds). */
export const engineMode = (import.meta.env.VITE_ENGINE ?? "http") as "http" | "pyodide";

/** The active engine instance used throughout the app. */
export const engine: PiEngine = engineMode === "pyodide" ? pyodideEngine : httpEngine;
