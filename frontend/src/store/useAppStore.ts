/**
 * Global application state (Zustand).
 *
 * Holds the working set of variables, the curated library, worked examples and
 * the latest solver result. Keeping this in one small store avoids prop drilling
 * while staying far simpler than a full Redux setup.
 */
import { create } from "zustand";

import { ApiError, engine } from "@/api/engine";
import { NB_BASE_DIMENSIONS } from "@/types";
import type {
  LibraryResponse,
  PiResultOut,
  VariableDraft,
  VariableIn,
  VariableLibraryEntry,
  WorkedExample,
} from "@/types";

/** Generate a reasonably unique id for a draft variable. */
function makeId(): string {
  return Math.random().toString(36).slice(2, 10);
}

/** Pad/trim an exponent vector to exactly NB_BASE_DIMENSIONS entries. */
function normalizeExponents(exponents: number[]): number[] {
  const out = exponents.slice(0, NB_BASE_DIMENSIONS);
  while (out.length < NB_BASE_DIMENSIONS) out.push(0);
  return out;
}

interface AppState {
  variables: VariableDraft[];
  library: LibraryResponse | null;
  examples: WorkedExample[];
  result: PiResultOut | null;
  loading: boolean;
  error: string | null;
  /** True while the (Pyodide) engine is downloading/booting in the background. */
  enginePreparing: boolean;

  loadInitialData: () => Promise<void>;
  addVariable: (draft: Omit<VariableDraft, "id">) => boolean;
  addLibraryVariable: (entry: VariableLibraryEntry) => void;
  removeVariable: (id: string) => void;
  clearVariables: () => void;
  loadExample: (example: WorkedExample) => void;
  solve: () => Promise<void>;
  setError: (message: string | null) => void;
}

export const useAppStore = create<AppState>((set, get) => ({
  variables: [],
  library: null,
  examples: [],
  result: null,
  loading: false,
  error: null,
  enginePreparing: false,

  loadInitialData: async () => {
    try {
      const [library, examples] = await Promise.all([
        engine.fetchLibrary(),
        engine.fetchExamples(),
      ]);
      set({ library, examples });
    } catch (error) {
      set({ error: resolveError(error) });
    }
    // Warm up the engine (e.g. download + boot Pyodide) in the background so the
    // first computation feels instant and the UI can show a clear status.
    if (engine.prepare) {
      set({ enginePreparing: true });
      try {
        await engine.prepare();
      } catch (error) {
        set({ error: resolveError(error) });
      } finally {
        set({ enginePreparing: false });
      }
    }
  },

  addVariable: (draft) => {
    const { variables } = get();
    if (variables.some((v) => v.symbol === draft.symbol)) {
      return false;
    }
    set({
      variables: [
        ...variables,
        { ...draft, id: makeId(), exponents: normalizeExponents(draft.exponents) },
      ],
      result: null,
    });
    return true;
  },

  addLibraryVariable: (entry) => {
    const { variables } = get();
    if (variables.some((v) => v.symbol === entry.symbol)) return;
    set({
      variables: [
        ...variables,
        {
          id: makeId(),
          symbol: entry.symbol,
          latex: entry.latex,
          name: entry.name_en,
          exponents: normalizeExponents(entry.exponents),
        },
      ],
      result: null,
    });
  },

  removeVariable: (id) => {
    set({ variables: get().variables.filter((v) => v.id !== id), result: null });
  },

  clearVariables: () => set({ variables: [], result: null, error: null }),

  loadExample: (example) => {
    const variables: VariableDraft[] = example.variables.map((v: VariableIn) => ({
      id: makeId(),
      symbol: v.symbol,
      latex: v.latex,
      name: v.name,
      exponents: normalizeExponents(v.exponents),
    }));
    set({ variables, result: null, error: null });
  },

  solve: async () => {
    const { variables } = get();
    if (variables.length < 2) return;
    set({ loading: true, error: null });
    try {
      const payload: VariableIn[] = variables.map((v) => ({
        symbol: v.symbol,
        exponents: v.exponents,
        latex: v.latex,
        name: v.name,
      }));
      const result = await engine.solvePiGroups(payload);
      set({ result, loading: false });
    } catch (error) {
      set({ error: resolveError(error), loading: false, result: null });
    }
  },

  setError: (message) => set({ error: message }),
}));

/** Turn an unknown thrown value into a user-facing message. */
function resolveError(error: unknown): string {
  if (error instanceof ApiError) return error.message;
  if (error instanceof TypeError) return "network";
  return "generic";
}
