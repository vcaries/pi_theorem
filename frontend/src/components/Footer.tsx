import { useTranslation } from "react-i18next";

/** Minimal footer with attribution. */
export function Footer() {
  const { t } = useTranslation();
  return (
    <footer className="mx-auto max-w-6xl px-4 py-8 text-center text-xs text-slate-400">
      <p>
        {t("footer.builtBy")} · {t("footer.engine")}
      </p>
    </footer>
  );
}
