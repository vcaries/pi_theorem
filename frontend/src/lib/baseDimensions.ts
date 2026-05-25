/**
 * Canonical SI base dimensions, mirrored from the backend
 * (`app/core/dimensions.py`). Kept locally so the input form works even before
 * the library endpoint has loaded.
 */
export interface BaseDimensionMeta {
  symbol: string;
  unit: string;
  labelEn: string;
  labelFr: string;
}

export const BASE_DIMENSIONS: BaseDimensionMeta[] = [
  { symbol: "M", unit: "kg", labelEn: "Mass", labelFr: "Masse" },
  { symbol: "L", unit: "m", labelEn: "Length", labelFr: "Longueur" },
  { symbol: "T", unit: "s", labelEn: "Time", labelFr: "Temps" },
  { symbol: "Θ", unit: "K", labelEn: "Temperature", labelFr: "Température" },
  { symbol: "I", unit: "A", labelEn: "Current", labelFr: "Courant" },
  { symbol: "N", unit: "mol", labelEn: "Substance", labelFr: "Matière" },
  { symbol: "J", unit: "cd", labelEn: "Luminosity", labelFr: "Luminosité" },
];
