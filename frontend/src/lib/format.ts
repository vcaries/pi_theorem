/**
 * Small formatting helpers shared across components.
 */
import { BASE_DIMENSIONS } from "@/lib/baseDimensions";

/**
 * Render an exponent vector as a LaTeX dimensional formula.
 *
 * @example dimensionToLatex([1, -1, -2]) // "M\\,L^{-1}\\,T^{-2}"
 */
export function dimensionToLatex(exponents: number[]): string {
  const parts: string[] = [];
  exponents.forEach((exponent, index) => {
    if (exponent === 0 || index >= BASE_DIMENSIONS.length) return;
    const symbol = BASE_DIMENSIONS[index].symbol;
    parts.push(exponent === 1 ? symbol : `${symbol}^{${exponent}}`);
  });
  return parts.length > 0 ? parts.join("\\,") : "1";
}
