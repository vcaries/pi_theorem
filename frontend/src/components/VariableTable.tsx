import { Trash2 } from "lucide-react";
import { useTranslation } from "react-i18next";

import { Katex } from "@/lib/Katex";
import { BASE_DIMENSIONS } from "@/lib/baseDimensions";
import { dimensionToLatex } from "@/lib/format";
import { useAppStore } from "@/store/useAppStore";
import type { VariableDraft } from "@/types";

/** Editable list of the variables currently in the analysis. */
export function VariableTable() {
  const { t } = useTranslation();
  const variables = useAppStore((s) => s.variables);
  const removeVariable = useAppStore((s) => s.removeVariable);

  if (variables.length === 0) {
    return (
      <p className="rounded-xl border border-dashed border-slate-300 px-4 py-8 text-center text-sm text-slate-400 dark:border-slate-700">
        {t("input.empty")}
      </p>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse text-sm">
        <thead>
          <tr className="border-b border-slate-200 text-left text-xs uppercase tracking-wide text-slate-500 dark:border-slate-700">
            <th className="px-3 py-2">{t("input.symbol")}</th>
            <th className="px-3 py-2">{t("input.dimensions")}</th>
            {BASE_DIMENSIONS.map((dim) => (
              <th key={dim.symbol} className="px-2 py-2 text-center font-semibold">
                {dim.symbol}
              </th>
            ))}
            <th className="px-3 py-2 text-right">{t("input.actions")}</th>
          </tr>
        </thead>
        <tbody>
          {variables.map((variable: VariableDraft) => (
            <tr
              key={variable.id}
              className="border-b border-slate-100 last:border-0 hover:bg-slate-50 dark:border-slate-800 dark:hover:bg-slate-800/40"
            >
              <td className="px-3 py-2 font-mono font-medium">
                <Katex math={variable.latex || variable.symbol} />
              </td>
              <td className="px-3 py-2 text-slate-500">
                <Katex math={dimensionToLatex(variable.exponents)} />
              </td>
              {variable.exponents.map((exponent, index) => (
                <td
                  key={index}
                  className={
                    "px-2 py-2 text-center font-mono " +
                    (exponent === 0 ? "text-slate-300 dark:text-slate-600" : "")
                  }
                >
                  {exponent}
                </td>
              ))}
              <td className="px-3 py-2 text-right">
                <button
                  type="button"
                  onClick={() => removeVariable(variable.id)}
                  className="rounded-lg p-1.5 text-slate-400 transition hover:bg-rose-50 hover:text-rose-500 dark:hover:bg-rose-950/40"
                  title={t("input.delete")}
                  aria-label={t("input.delete")}
                >
                  <Trash2 size={16} />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
