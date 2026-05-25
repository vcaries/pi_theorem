import { Plus } from "lucide-react";
import { useState } from "react";
import { useTranslation } from "react-i18next";

import { BASE_DIMENSIONS } from "@/lib/baseDimensions";
import { useAppStore } from "@/store/useAppStore";
import { NB_BASE_DIMENSIONS } from "@/types";

const EMPTY_EXPONENTS = Array<number>(NB_BASE_DIMENSIONS).fill(0);

/** Form for adding a single custom variable with its dimensional exponents. */
export function VariableForm() {
  const { t, i18n } = useTranslation();
  const isFr = i18n.language?.startsWith("fr");
  const addVariable = useAppStore((s) => s.addVariable);

  const [symbol, setSymbol] = useState("");
  const [name, setName] = useState("");
  const [latex, setLatex] = useState("");
  const [exponents, setExponents] = useState<number[]>(EMPTY_EXPONENTS);
  const [localError, setLocalError] = useState<string | null>(null);

  const updateExponent = (index: number, value: string) => {
    const parsed = value === "" || value === "-" ? 0 : Number(value);
    if (Number.isNaN(parsed)) return;
    setExponents((prev) => prev.map((e, i) => (i === index ? parsed : e)));
  };

  const reset = () => {
    setSymbol("");
    setName("");
    setLatex("");
    setExponents(EMPTY_EXPONENTS);
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    const trimmed = symbol.trim();
    if (!trimmed) {
      setLocalError(t("input.symbolRequired"));
      return;
    }
    const ok = addVariable({
      symbol: trimmed,
      name: name.trim() || null,
      latex: latex.trim() || null,
      exponents,
    });
    if (!ok) {
      setLocalError(t("input.duplicate"));
      return;
    }
    setLocalError(null);
    reset();
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
        <div>
          <label className="field-label" htmlFor="var-symbol">
            {t("input.symbol")}
          </label>
          <input
            id="var-symbol"
            className="text-input font-mono"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
            placeholder="rho"
          />
        </div>
        <div>
          <label className="field-label" htmlFor="var-name">
            {t("input.name")}
          </label>
          <input
            id="var-name"
            className="text-input"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Density"
          />
        </div>
        <div>
          <label className="field-label" htmlFor="var-latex">
            {t("input.latex")}
          </label>
          <input
            id="var-latex"
            className="text-input font-mono"
            value={latex}
            onChange={(e) => setLatex(e.target.value)}
            placeholder="\rho"
          />
        </div>
      </div>

      <div>
        <span className="field-label">{t("input.dimensions")}</span>
        <div className="grid grid-cols-4 gap-2 sm:grid-cols-7">
          {BASE_DIMENSIONS.map((dim, index) => (
            <label key={dim.symbol} className="flex flex-col items-center gap-1">
              <span
                className="text-sm font-semibold text-brand-600 dark:text-brand-300"
                title={`${isFr ? dim.labelFr : dim.labelEn} (${dim.unit})`}
              >
                {dim.symbol}
              </span>
              <input
                type="number"
                step="1"
                inputMode="numeric"
                className="text-input !px-1 text-center font-mono"
                value={exponents[index] === 0 ? "" : exponents[index]}
                onChange={(e) => updateExponent(index, e.target.value)}
                placeholder="0"
              />
            </label>
          ))}
        </div>
      </div>

      {localError && (
        <p className="text-sm font-medium text-rose-500">{localError}</p>
      )}

      <button type="submit" className="btn-primary w-full sm:w-auto">
        <Plus size={16} />
        {t("input.add")}
      </button>
    </form>
  );
}
