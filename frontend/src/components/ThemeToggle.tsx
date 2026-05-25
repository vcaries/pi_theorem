import { Moon, Sun } from "lucide-react";
import { useTranslation } from "react-i18next";

import type { Theme } from "@/hooks/useTheme";

interface ThemeToggleProps {
  theme: Theme;
  onToggle: () => void;
}

/** A round icon button that switches between light and dark themes. */
export function ThemeToggle({ theme, onToggle }: ThemeToggleProps) {
  const { t } = useTranslation();
  return (
    <button
      type="button"
      onClick={onToggle}
      title={t("nav.theme")}
      aria-label={t("nav.theme")}
      className="btn-ghost !px-2.5"
    >
      {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
    </button>
  );
}
