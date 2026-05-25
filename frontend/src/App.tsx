import { Calculator, Eraser, FlaskConical, Library, Loader2, Sparkles } from "lucide-react";
import { useEffect } from "react";
import { useTranslation } from "react-i18next";

import { ExamplesMenu } from "@/components/ExamplesMenu";
import { Footer } from "@/components/Footer";
import { Header } from "@/components/Header";
import { LibraryPanel } from "@/components/LibraryPanel";
import { ResultsPanel } from "@/components/ResultsPanel";
import { VariableForm } from "@/components/VariableForm";
import { VariableTable } from "@/components/VariableTable";
import { useTheme } from "@/hooks/useTheme";
import { useAppStore } from "@/store/useAppStore";

/** Reusable titled section card. */
function SectionCard({
  icon,
  title,
  subtitle,
  children,
}: {
  icon: React.ReactNode;
  title: string;
  subtitle?: string;
  children: React.ReactNode;
}) {
  return (
    <section className="card p-5 sm:p-6">
      <div className="mb-4 flex items-start gap-3">
        <span className="mt-0.5 flex h-9 w-9 items-center justify-center rounded-xl bg-brand-50 text-brand-600 dark:bg-brand-900/40 dark:text-brand-300">
          {icon}
        </span>
        <div>
          <h2 className="text-base font-bold tracking-tight">{title}</h2>
          {subtitle && <p className="text-xs text-slate-500">{subtitle}</p>}
        </div>
      </div>
      {children}
    </section>
  );
}

export default function App() {
  const { t } = useTranslation();
  const { theme, toggleTheme } = useTheme();

  const variables = useAppStore((s) => s.variables);
  const solve = useAppStore((s) => s.solve);
  const clearVariables = useAppStore((s) => s.clearVariables);
  const loadInitialData = useAppStore((s) => s.loadInitialData);
  const enginePreparing = useAppStore((s) => s.enginePreparing);

  useEffect(() => {
    void loadInitialData();
  }, [loadInitialData]);

  const canSolve = variables.length >= 2;

  return (
    <div className="min-h-screen">
      <Header theme={theme} onToggleTheme={toggleTheme} />

      <main className="mx-auto max-w-6xl px-4 py-8">
        {enginePreparing && (
          <div className="mb-6 flex items-center gap-3 rounded-xl border border-brand-200 bg-brand-50 px-4 py-3 text-sm text-brand-800 dark:border-brand-900/60 dark:bg-brand-950/40 dark:text-brand-200">
            <Loader2 size={16} className="animate-spin shrink-0" />
            {t("engine.preparing")}
          </div>
        )}

        {/* Hero */}
        <div className="animate-fade-in mb-8 max-w-3xl">
          <span className="inline-flex items-center gap-1.5 rounded-full bg-brand-50 px-3 py-1 text-xs font-semibold text-brand-700 dark:bg-brand-900/40 dark:text-brand-200">
            <Sparkles size={13} />
            Vaschy–Buckingham
          </span>
          <h1 className="mt-3 text-3xl font-extrabold tracking-tight sm:text-4xl">
            {t("app.tagline")}
          </h1>
          <p className="mt-3 text-slate-500">{t("app.intro")}</p>
        </div>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
          {/* Input column */}
          <div className="space-y-6 lg:col-span-7">
            <SectionCard
              icon={<FlaskConical size={18} />}
              title={t("input.title")}
              subtitle={t("input.subtitle")}
            >
              <VariableForm />
              <div className="mt-5">
                <VariableTable />
              </div>
              <div className="mt-5 flex flex-wrap items-center gap-3 border-t border-slate-100 pt-5 dark:border-slate-800">
                <button
                  type="button"
                  onClick={() => void solve()}
                  disabled={!canSolve}
                  className="btn-primary"
                >
                  <Calculator size={16} />
                  {t("results.compute")}
                </button>
                <button
                  type="button"
                  onClick={clearVariables}
                  disabled={variables.length === 0}
                  className="btn-ghost"
                >
                  <Eraser size={15} />
                  {t("input.clear")}
                </button>
              </div>
            </SectionCard>

            <SectionCard
              icon={<Library size={18} />}
              title={t("library.title")}
              subtitle={t("library.subtitle")}
            >
              <LibraryPanel />
            </SectionCard>

            <SectionCard
              icon={<FlaskConical size={18} />}
              title={t("examples.title")}
              subtitle={t("examples.subtitle")}
            >
              <ExamplesMenu />
            </SectionCard>
          </div>

          {/* Results column */}
          <div className="lg:col-span-5">
            <div className="lg:sticky lg:top-20">
              <SectionCard icon={<Calculator size={18} />} title={t("results.title")}>
                <ResultsPanel />
              </SectionCard>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
