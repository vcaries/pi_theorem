/**
 * Typed API client for the Pi-Scope backend.
 *
 * The base URL comes from `VITE_API_URL`; in development it defaults to `/api`,
 * which the Vite dev server proxies to the FastAPI backend (see vite.config.ts).
 */
import type {
  LibraryResponse,
  PiResultOut,
  VariableIn,
  WorkedExample,
} from "@/types";

const BASE_URL = import.meta.env.VITE_API_URL ?? "/api";

/** Error thrown when the API returns a non-2xx response. */
export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

/**
 * Perform a JSON request and parse the response, surfacing FastAPI error
 * details (the `detail` field) as an {@link ApiError}.
 */
async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });

  if (!response.ok) {
    let detail = `Request failed with status ${response.status}`;
    try {
      const body = await response.json();
      if (typeof body?.detail === "string") {
        detail = body.detail;
      } else if (Array.isArray(body?.detail) && body.detail[0]?.msg) {
        detail = body.detail[0].msg;
      }
    } catch {
      /* response had no JSON body; keep the default message */
    }
    throw new ApiError(detail, response.status);
  }

  return (await response.json()) as T;
}

/** Compute the dimensionless Pi groups for a set of variables. */
export function solvePiGroups(
  variables: VariableIn[],
  integerize = true,
): Promise<PiResultOut> {
  return request<PiResultOut>("/pi/solve", {
    method: "POST",
    body: JSON.stringify({ variables, integerize }),
  });
}

/** Fetch the base dimensions and the curated variable library. */
export function fetchLibrary(): Promise<LibraryResponse> {
  return request<LibraryResponse>("/library");
}

/** Fetch all preloaded worked examples. */
export function fetchExamples(): Promise<WorkedExample[]> {
  return request<WorkedExample[]>("/examples");
}
