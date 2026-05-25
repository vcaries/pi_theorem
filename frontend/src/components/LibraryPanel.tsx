import { Plus, Search } from "lucide-react";
import { useMemo, useState } from "react";
import { useTranslation } from "react-i18next";

import { Katex } from "@/lib/Katex";
import { useAppStore } from "@/store/useAppStore";
import type { VariableLibraryEntry } from "@/types";

/** Searchable, domain-organised browser of predefined library variables. */
export function LibraryPanel() {
  const { t, i18n } = useTranslation();
  const isFr = i18n.language?.startsWith("fr");
  const library = useAppStore((s) => s.library);
  const addLibraryVariable = useAppStore((s) => s.addLibraryVariable);
  const variables = useAppStore((s) => s.variables);

  const categories = library?.categories ?? [];
  const [activeId, setActiveId] = useState<string>("");
  const [query, setQuery] = useState("");

  const activeCategory = useMemo(() => {
    if (categories.length === 0) return null;
    return categories.find((c) => c.id === activeId) ?? categories[0];
  }, [categories, activeId]);

  const visibleVariables = useMemo(() => {
    if (!activeCategory) return [] as VariableLibraryEntry[];
    const normalized = query.trim().toLowerCase();
    if (!normalized) return activeCategory.variables;
    return activeCategory.variables.filter((v) =>
      [v.symbol, v.name_en, v.name_fr].some((field) =>
        field.toLowerCase().includes(normalized),
      ),
    );
  }, [activeCategory, query]);

  const isAdded = (symbol: string) => variables.some((v) => v.symbol === symbol);

  if (categories.length === 0) {
    return null;
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-2">
        {categories.map((category) => {
          const selected = activeCategory?.id === category.id;
          return (
            <button
              key={category.id}
              type="button"
              onClick={() => setActiveId(category.id)}
              className={
                "rounded-full px-3 py-1.5 text-xs font-semibold transition " +
                (selected
                  ? "bg-brand-600 text-white shadow-sm"
                  : "bg-slate-100 text-slate-600 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700")
              }
            >
              {isFr ? category.name_fr : category.name_en}
            </button>
          );
        })}
      </div>

      <div className="relative">
        <Search
          size={16}
          className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
        />
        <input
          className="text-input pl-9"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={t("library.search")}
        />
      </div>

      <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
        {visibleVariables.map((entry) => {
          const added = isAdded(entry.symbol);
          return (
            <button
              key={entry.symbol}
              type="button"
              disabled={added}
              onClick={() => addLibraryVariable(entry)}
              title={isFr ? entry.description_fr ?? "" : entry.description_en ?? ""}
              className={
                "group flex items-center justify-between gap-2 rounded-xl border px-3 py-2 text-left text-sm transition " +
                (added
                  ? "cursor-not-allowed border-slate-200 bg-slate-50 opacity-60 dark:border-slate-800 dark:bg-slate-800/50"
                  : "border-slate-200 bg-white hover:border-brand-300 hover:bg-brand-50/50 dark:border-slate-700 dark:bg-slate-800 dark:hover:border-brand-700 dark:hover:bg-slate-700/60")
              }
            >
              <span className="flex min-w-0 items-baseline gap-2">
                <Katex math={entry.latex} className="text-base" />
                <span className="truncate text-xs text-slate-500">
                  {isFr ? entry.name_fr : entry.name_en}
                </span>
              </span>
              {!added && (
                <Plus
                  size={15}
                  className="shrink-0 text-slate-300 transition group-hover:text-brand-500"
                />
              )}
            </button>
          );
        })}
        {visibleVariables.length === 0 && (
          <p className="col-span-full py-4 text-center text-sm text-slate-400">
            {t("library.noResults")}
          </p>
        )}
      </div>
    </div>
  );
}
