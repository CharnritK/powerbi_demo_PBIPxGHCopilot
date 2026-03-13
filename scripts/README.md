# Scripts

Canonical runnable scripts live in `scripts/cli/`.

Use `scripts/helpers/` for local convenience helpers that are not core business logic.

Top-level `scripts/*.py` files are compatibility wrappers or retained MCP utilities for older demo flows. New work should target `scripts/cli/` and `src/`.

Measure validation entrypoints currently live at the top level so they are easy to call during the demo:

- `python scripts/evaluate_pbip_for_testing.py`
- `python scripts/generate_measure_test_scenarios.py`
- `python scripts/generate_measure_validation_template.py`

Notebook-oriented demo helpers live in `scripts/helpers/`, including:

- `notebook_bootstrap.py`
- `notebook_display.py`
- `measure_validation_demo.py`
- `result_writer.py`
