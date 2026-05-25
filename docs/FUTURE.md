# Future improvements

Longer-horizon ideas that would deepen the science, broaden reach, or sharpen the
showcase. Ordered roughly by leverage.

## Scientific depth

- **Automatic naming of known groups.** Detect Reynolds, Mach, Froude, Nusselt,
  Prandtl, Weber, Strouhal, etc. by matching computed groups against a catalogue,
  and label them in the UI.
- **Repeating-variable selection.** Let the user choose the *k* repeating
  variables; regenerate the basis so groups match a textbook convention.
- **Alternative bases.** Offer interactive recombination of the null-space basis
  (groups are only defined up to products of powers).
- **Consistency diagnostics.** Flag redundant variables, all-dimensionless inputs,
  and singular sub-systems with actionable hints.
- **Relation builder.** Given a target variable, express it (symbolically) as a
  function of the dimensionless groups and the others.

## Engineering & quality

- **Frontend test suite.** Vitest + Testing Library for components, Playwright for
  end-to-end flows (load Chen → compute → verify 8 groups).
- **Property-based tests** for the engine (Hypothesis): every returned group must
  be dimensionless; group count must equal `n − rank` for random valid inputs.
- **Performance budget & bundle analysis;** lazy-load KaTeX to cut first paint.
- **OpenTelemetry tracing** on the backend for a hosted demo.

## Reach & deployment

- **Pyodide build.** Compile the Python engine to run in the browser via
  WebAssembly. This yields a **fully static** demo deployable straight to
  `vcaries.github.io` — no server — while keeping the exact Python code as the
  engine. The decoupled architecture already isolates the engine, making this a
  contained effort (swap the API client for an in-browser call).
- **One-click deploys.** Render/Fly.io/Hugging Face Spaces recipes and a
  `deploy/` folder with infra-as-code.
- **PWA + offline.** Service worker so the tool works without a network.

## Product & UX

- **Problem gallery.** Save, name, share and reload problems; deep links encode
  the variable set in the URL.
- **Export bundle.** One click to download a PDF/Markdown report with the matrix,
  groups, and references — ideal for lab notebooks and papers.
- **Unit-aware entry.** Let users type SI units (e.g. `kg/m^3`) and derive the
  exponent vector automatically.
- **Community library.** Allow users to propose new library variables via a simple
  schema-validated PR flow.

## Showcase polish

- **Animated walkthrough GIFs** for the README (the brief calls for these).
- **A short "how it works" page** with the linear-algebra explanation and a live,
  editable matrix.
- **Benchmarks & correctness page** reproducing several published dimensionless
  analyses to build trust.
