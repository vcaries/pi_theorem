import { BookOpen, Play } from "lucide-react";
import { useTranslation } from "react-i18next";

import { useAppStore } from "@/store/useAppStore";

/** List of preloaded, citeable worked examples (e.g. the Chen 1990 case). */
export function ExamplesMenu() {
  const { t, i18n } = useTranslation();
  const isFr = i18n.language?.startsWith("fr");
  const examples = useAppStore((s) => s.examples);
  const loadExample = useAppStore((s) => s.loadExample);

  if (examples.length === 0) return null;

  return (
    <ul className="space-y-2">
      {examples.map((example) => (
        <li
          key={example.id}
          className="rounded-xl border border-slate-200 p-3 transition hover:border-brand-300 dark:border-slate-700 dark:hover:border-brand-700"
        >
          <div className="flex items-start justify-between gap-3">
            <div className="min-w-0">
              <p className="flex items-center gap-2 text-sm font-semibold">
                <BookOpen size={15} className="shrink-0 text-brand-500" />
                {isFr ? example.title_fr : example.title_en}
              </p>
              <p className="mt-1 text-xs text-slate-500">
                {isFr ? example.description_fr : example.description_en}
              </p>
              {example.reference && (
                <p className="mt-1 text-[11px] italic text-slate-400">
                  {t("examples.reference")}: {example.reference}
                </p>
              )}
            </div>
            <button
              type="button"
              onClick={() => loadExample(example)}
              className="btn-ghost shrink-0 !py-1.5 !text-xs"
            >
              <Play size={13} />
              {t("examples.load")}
            </button>
          </div>
        </li>
      ))}
    </ul>
  );
}
