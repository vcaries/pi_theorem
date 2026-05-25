# UI / UX design

The goal is to feel like **engineering software**: precise, calm, trustworthy —
not a flashy consumer app. Every visual decision serves clarity of the science.

## Design principles

1. **Math first.** Equations and the dimensional matrix are the heroes; chrome
   stays quiet around them.
2. **Immediate feedback.** Adding from the library or loading an example updates
   the workspace instantly; computing shows a clear loading and result state.
3. **No dead ends.** Empty states explain what to do next; errors are specific
   ("Add more variables", "Cannot reach the API") rather than generic.
4. **Bilingual & themable by default.** FR/EN and light/dark are first-class, not
   afterthoughts, and both persist across reloads.
5. **Accessible.** Semantic HTML, labelled controls, keyboard-operable, sufficient
   contrast in both themes.

## Layout

A two-column workspace on large screens, stacking on mobile:

- **Left (input):** the variable form, the live variable table, and the
  Compute / Clear actions; below it the **library browser** (chips by domain +
  search) and the **worked examples**.
- **Right (results, sticky):** summary chips (variables · rank · #Π), a one-line
  statement of the theorem result, the **dimensional matrix**, the **Π-group
  cards**, the product line, and export buttons.

The sticky results column keeps the answer in view while the user tweaks inputs.

## Visual language

- **Palette:** indigo (`brand`) as the primary, cyan (`accent`) for secondary
  emphasis, with slate neutrals. Semantic colours for success/error only.
- **Typography:** *Inter* for UI text, *JetBrains Mono* for symbols and matrix
  cells — a subtle "this is a technical tool" cue.
- **Surfaces:** soft rounded cards (`rounded-2xl`), 1px borders, gentle shadows;
  the same components recolour cleanly in dark mode.
- **Motion:** restrained. Result cards fade-and-rise with a small stagger; theme
  changes cross-fade. Nothing bounces or distracts.

## Components

| Component | Role |
| --- | --- |
| `Header` | Branding, language switch, theme toggle, source link. |
| `VariableForm` | Add a custom variable: symbol, optional name/LaTeX, 7 exponent inputs. |
| `VariableTable` | The working set, with per-variable dimensional formula (KaTeX) and delete. |
| `LibraryPanel` | Domain chips + search; click a variable to add it. |
| `ExamplesMenu` | Citeable preloaded cases; one-click load. |
| `DimensionMatrix` | The matrix with base-dimension rows and variable columns. |
| `PiGroupCard` | One dimensionless group (KaTeX) with copy-to-clipboard. |
| `ResultsPanel` | Orchestrates loading/error/empty/result states + exports. |

## Internationalisation

All copy lives in `src/i18n/{fr,en}.json`; components never hard-code strings.
Interpolated values (counts, rank) use i18next placeholders so grammar stays
correct in both languages. French is the default to match the author's audience.

## Theming

Dark mode uses Tailwind's `class` strategy: a `dark` class on `<html>` toggled by
`useTheme`, which respects a saved choice then the OS preference, and persists to
localStorage. Component styles declare both light and `dark:` variants.

## Accessibility checklist

- [x] All interactive elements are real buttons/inputs with labels or `aria-label`.
- [x] Visible focus rings (`focus-visible:ring`).
- [x] Color is never the only signal (icons + text accompany state).
- [x] Contrast meets WCAG AA in both themes.
- [ ] Full screen-reader pass and keyboard E2E (planned, Milestone 1).
