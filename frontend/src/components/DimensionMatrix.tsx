import { useTranslation } from "react-i18next";

import { Katex } from "@/lib/Katex";
import type { PiResultOut } from "@/types";

interface DimensionMatrixProps {
  result: PiResultOut;
  /** Map from variable symbol to its LaTeX rendering, for nice column headers. */
  latexBySymbol: Record<string, string>;
}

/** Renders the dimensional matrix with base-dimension rows and variable columns. */
export function DimensionMatrix({ result, latexBySymbol }: DimensionMatrixProps) {
  const { t } = useTranslation();

  return (
    <div>
      <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-200">
        {t("results.matrix")}
      </h3>
      <p className="mb-3 text-xs text-slate-400">{t("results.matrixHint")}</p>
      <div className="overflow-x-auto">
        <table className="border-collapse text-center font-mono text-sm">
          <thead>
            <tr>
              <th className="px-2 py-1.5" />
              {result.variables.map((symbol) => (
                <th
                  key={symbol}
                  className="px-3 py-1.5 text-brand-600 dark:text-brand-300"
                >
                  <Katex math={latexBySymbol[symbol] ?? symbol} />
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {result.matrix.map((row, rowIndex) => (
              <tr key={result.base_symbols[rowIndex]}>
                <th className="px-2 py-1.5 text-right font-semibold text-accent-600">
                  {result.base_symbols[rowIndex]}
                </th>
                {row.map((value, colIndex) => (
                  <td
                    key={colIndex}
                    className={
                      "border border-slate-100 px-3 py-1.5 dark:border-slate-800 " +
                      (value === 0 ? "text-slate-300 dark:text-slate-600" : "")
                    }
                  >
                    {value}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
