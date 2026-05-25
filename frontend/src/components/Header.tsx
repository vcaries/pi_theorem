import { Github } from "lucide-react";
import { useTranslation } from "react-i18next";

import { LanguageToggle } from "@/components/LanguageToggle";
import { ThemeToggle } from "@/components/ThemeToggle";
import type { Theme } from "@/hooks/useTheme";

interface HeaderProps {
  theme: Theme;
  onToggleTheme: () => void;
}

/** Sticky top bar with branding and the global controls. */
export function Header({ theme, onToggleTheme }: HeaderProps) {
  const { t } = useTranslation();

  return (
    <header className="sticky top-0 z-20 border-b border-slate-200/70 bg-white/80 backdrop-blur dark:border-slate-800/70 dark:bg-slate-950/80">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3">
        <div className="flex items-center gap-3">
          <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-600 text-xl font-bold text-white shadow-sm">
            Π
          </span>
          <div className="leading-tight">
            <h1 className="text-lg font-bold tracking-tight">{t("app.title")}</h1>
            <p className="hidden text-xs text-slate-500 sm:block dark:text-slate-400">
              {t("app.tagline")}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <LanguageToggle />
          <ThemeToggle theme={theme} onToggle={onToggleTheme} />
          <a
            href="https://github.com/vcaries"
            target="_blank"
            rel="noreferrer"
            className="btn-ghost !px-2.5"
            title={t("nav.github")}
            aria-label={t("nav.github")}
          >
            <Github size={18} />
          </a>
        </div>
      </div>
    </header>
  );
}
