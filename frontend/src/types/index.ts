/**
 * Shared TypeScript types mirroring the backend API contract
 * (see `backend/app/models/schemas.py`).
 */

/** Number of SI base dimensions: M, L, T, Θ, I, N, J. */
export const NB_BASE_DIMENSIONS = 7;

/** A variable as sent to the solver endpoint. */
export interface VariableIn {
  symbol: string;
  exponents: number[];
  latex?: string | null;
  name?: string | null;
}

/** A single dimensionless group returned by the solver. */
export interface PiGroupOut {
  index: number;
  exponents: number[];
  latex: string;
  ascii: string;
}

/** Full solver response. */
export interface PiResultOut {
  variables: string[];
  base_symbols: string[];
  matrix: number[][];
  rank: number;
  n_variables: number;
  n_groups: number;
  groups: PiGroupOut[];
  product_latex: string | null;
}

/** Metadata for one SI base dimension. */
export interface BaseDimensionInfo {
  symbol: string;
  name: string;
  si_unit: string;
  label_en: string;
  label_fr: string;
}

/** A predefined library variable. */
export interface VariableLibraryEntry {
  symbol: string;
  name_en: string;
  name_fr: string;
  si_unit: string;
  exponents: number[];
  latex: string;
  description_en?: string | null;
  description_fr?: string | null;
}

/** A library category (physics domain). */
export interface LibraryCategory {
  id: string;
  name_en: string;
  name_fr: string;
  variables: VariableLibraryEntry[];
}

/** Response of GET /api/library. */
export interface LibraryResponse {
  base_dimensions: BaseDimensionInfo[];
  categories: LibraryCategory[];
}

/** A preloaded worked example. */
export interface WorkedExample {
  id: string;
  title_en: string;
  title_fr: string;
  description_en: string;
  description_fr: string;
  reference?: string | null;
  variables: VariableIn[];
}

/**
 * A variable being edited in the UI. `exponents` is always a fixed-length
 * array of 7 numbers aligned with the SI base dimensions.
 */
export interface VariableDraft {
  id: string;
  symbol: string;
  latex?: string | null;
  name?: string | null;
  exponents: number[];
}
