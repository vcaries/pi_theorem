# Legacy

These are the **original** files of the project, preserved for provenance and to
show the project's evolution from a desktop script to a full web application:

- `pi_theorem.py` — the original SymPy engine (printed Π terms to stdout).
- `gui.py` — the original PyQt5 desktop GUI.
- `preset_variables.yaml` — the original flat list of preset variables.

They are **not** used by the web application. The modern, structured successor of
`pi_theorem.py` lives in [`../backend/app/core/`](../backend/app/core/), and the
preset variables have grown into the curated, domain-organised library at
[`../backend/app/data/library.yaml`](../backend/app/data/library.yaml).

To run the old desktop tool:

```bash
pip install pyqt5 sympy pyyaml
python gui.py
```
