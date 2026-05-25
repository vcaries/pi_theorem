import { Download, FileJson, FunctionSquare, Loader2 } from "lucide-react";
import { useMemo } from "react";
import { useTranslation } from "react-i18next";

import { DimensionMatrix } from "@/components/DimensionMatrix";
import { PiGroupCard } from "@/components/PiGroupCard";
import { Katex } from "@/lib/Katex";
import { exportJson, exportLatex } from "@/lib/export";
import { useAppStore } from "@/store/useAppStore";

/** Right-hand panel showing the dimensional matrix and the dimensionless groups. */
export function ResultsPanel() {
  const { t } = useTranslation();
  const result = useAppStore((s) => s.result);
  const loading = useAppStore((s) => s.loading);
  const error = useAppStore((s) => s.error);
  const variables = useAppStore((s) => s.variables);

  // Build a symbol -> LaTeX map so the matrix can render pretty column headers.
  const latexBySymbol = useMemo(() => {
    const map: Record<string, string> = {};
    for (const v of variables) {
      if (v.latex) map[v.symbol] = v.latex;
    }
    return map;
  }, [variables]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center gap-3 py-16 text-slate-400">
        <Loader2 size={28} className="animate-spin text-brand-500" />
        <p className="text-sm">{t("results.computing")}</p>
      </div>
    );
  }

  if (error) {
    const message =
      error === "network"
        ? t("errors.network")
        : error === "generic"
          ? t("errors.generic")
          : error;
    return (
      <div className="rounded-xl border border-rose-200 bg-rose-50 px-4 py-6 text-center text-sm text-rose-600 dark:border-rose-900/60 dark:bg-rose-950/40 dark:text-rose-300">
        {message}
      </div>
    );
  }

  if (!result) {
    return (
      <p className="rounded-xl border border-dashed border-slate-300 px-4 py-12 text-center text-sm text-slate-400 dark:border-slate-700">
        {t("results.empty")}
      </p>
    );
  }

  return (
    <div className="space-y-6">
      {/* Summary chips */}
      <div className="flex flex-wrap gap-2 text-xs font-semibold">
        <span className="rounded-full bg-brand-50 px-3 py-1 text-brand-700 dark:bg-brand-900/40 dark:text-brand-200">
          {result.n_variables} variables
        </span>
        <span className="rounded-full bg-accent-500/10 px-3 py-1 text-accent-600">
          rank {result.rank}
        </span>
        <span className="rounded-full bg-emerald-50 px-3 py-1 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-200">
          {result.n_groups} Π
        </span>
      </div>

      <p className="text-sm text-slate-500">
        {t("results.theorem", {
          n: result.n_variables,
          k: result.rank,
          p: result.n_groups,
        })}
      </p>

      <DimensionMatrix result={result} latexBySymbol={latexBySymbol} />

      <div>
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-200">
            {t("results.groups")}
          </h3>
          <div className="flex gap-2">
            <button type="button" onClick={() => exportJson(result)} className="btn-ghost !py-1.5 !text-xs">
              <FileJson size={14} />
              {t("results.exportJson")}
            </button>
            <button type="button" onClick={() => exportLatex(result)} className="btn-ghost !py-1.5 !text-xs">
              <Download size={14} />
              {t("results.exportLatex")}
            </button>
          </div>
        </div>

        <div className="space-y-3">
          {result.groups.map((group, index) => (
            <PiGroupCard key={group.index} group={group} order={index} />
          ))}
        </div>
      </div>

      {result.product_latex && (
        <div>
          <h3 className="mb-2 flex items-center gap-2 text-sm font-semibold text-slate-700 dark:text-slate-200">
            <FunctionSquare size={15} className="text-brand-500" />
            {t("results.product")}
          </h3>
          <div className="card overflow-x-auto px-5 py-4">
            <Katex math={result.product_latex} display />
          </div>
        </div>
      )}
    </div>
  );
}
