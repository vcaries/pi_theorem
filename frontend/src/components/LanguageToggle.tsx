import { useTranslation } from "react-i18next";

import { setLanguage } from "@/i18n";
import type { Language } from "@/i18n";

/** A compact FR / EN language switcher. */
export function LanguageToggle() {
  const { i18n } = useTranslation();
  const current = (i18n.language?.startsWith("fr") ? "fr" : "en") as Language;

  return (
    <div className="inline-flex overflow-hidden rounded-xl border border-slate-200 text-xs font-semibold dark:border-slate-700">
      {(["fr", "en"] as const).map((lang) => (
        <button
          key={lang}
          type="button"
          onClick={() => setLanguage(lang)}
          className={
            current === lang
              ? "bg-brand-600 px-3 py-2 text-white"
              : "bg-white px-3 py-2 text-slate-600 hover:bg-slate-50 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700"
          }
        >
          {lang.toUpperCase()}
        </button>
      ))}
    </div>
  );
}
