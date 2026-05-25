/**
 * i18next initialisation with full French / English support.
 *
 * The active language is persisted in localStorage so the user's choice
 * survives reloads. French is the default to match the author's audience.
 */
import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import en from "./en.json";
import fr from "./fr.json";

export type Language = "fr" | "en";

const STORAGE_KEY = "pi-scope-language";

/** Read the persisted language, falling back to French. */
function getInitialLanguage(): Language {
  if (typeof window === "undefined") return "fr";
  const stored = window.localStorage.getItem(STORAGE_KEY);
  return stored === "en" || stored === "fr" ? stored : "fr";
}

void i18n.use(initReactI18next).init({
  resources: {
    en: { translation: en },
    fr: { translation: fr },
  },
  lng: getInitialLanguage(),
  fallbackLng: "en",
  interpolation: { escapeValue: false },
});

/** Switch the active language and persist the choice. */
export function setLanguage(language: Language): void {
  void i18n.changeLanguage(language);
  window.localStorage.setItem(STORAGE_KEY, language);
}

export default i18n;
