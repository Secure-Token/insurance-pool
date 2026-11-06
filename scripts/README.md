# ST Evaluation Scripts

## Scope
`run_evaluation.py` is a **mock pipeline smoke test**. It checks fixture discovery, result shape/schema validation, and metric computation. It does **not** evaluate an LLM or demonstrate semantic accuracy.

## Expected layout
Place this folder at the repository root as `scripts/`:

```text
scripts/
  run_evaluation.py
  README.md
rules/
  evaluation_schema.json
  examples/
    positive/case.json
    negative/case.json
    ambiguous/case.json
    contradictory/case.json
```

Each fixture must include explicit ground truth:
- `expected_failure: true|false`, or
- `expected_label: FAILURE|NO_FAILURE` (aliases documented in the script).

## Run
Install the optional validator:
```bash
python -m pip install jsonschema
```

Run from repository root:
```bash
python scripts/run_evaluation.py
```

Custom paths:
```bash
python scripts/run_evaluation.py --examples rules/examples --schema rules/evaluation_schema.json --output scripts/evaluation_report.json
```

## Important
The current examples may use a `case.json` fixture format. Add `expected_failure` to each case before running. The runner skips fixtures without explicit ground truth; it will not infer labels from folder names.
