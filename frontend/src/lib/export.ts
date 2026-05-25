/**
 * Client-side export helpers (JSON and LaTeX) for solver results.
 */
import type { PiResultOut } from "@/types";

/** Trigger a browser download of a text blob. */
function download(filename: string, content: string, mime: string): void {
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

/** Export the full result as a pretty-printed JSON file. */
export function exportJson(result: PiResultOut): void {
  download("pi-scope-result.json", JSON.stringify(result, null, 2), "application/json");
}

/** Export the dimensionless groups as a standalone LaTeX `align*` block. */
export function exportLatex(result: PiResultOut): void {
  const lines = result.groups.map((g) => `  ${g.latex} \\\\`).join("\n");
  const tex = `\\begin{align*}\n${lines}\n\\end{align*}\n`;
  download("pi-scope-groups.tex", tex, "text/x-tex");
}
