/**
 * Thin React wrapper around KaTeX for rendering LaTeX math.
 *
 * Rendering is memoised on the input string; invalid LaTeX degrades gracefully
 * to the raw source instead of throwing (KaTeX `throwOnError: false`).
 */
import katex from "katex";
import { useMemo } from "react";

interface KatexProps {
  /** The LaTeX source to render. */
  math: string;
  /** Render in display (block, centered) mode rather than inline. */
  display?: boolean;
  className?: string;
}

export function Katex({ math, display = false, className }: KatexProps) {
  const html = useMemo(
    () =>
      katex.renderToString(math, {
        displayMode: display,
        throwOnError: false,
        output: "htmlAndMathml",
      }),
    [math, display],
  );

  return <span className={className} dangerouslySetInnerHTML={{ __html: html }} />;
}
