# Task Playbooks

Common task patterns:

- Add Power BI REST automation: implement in `src/powerbi/`, expose via `scripts/cli/`, then add tests.
- Update semantic-model rules: edit TMDL or MCP helpers, run `validate_tmdl_semantic_model.py`, then update docs.
- Change notebook behavior: move reusable logic into `src/` first, then update the notebook.
- Update business rules: edit `docs/domain/`, `docs/data-model/`, and any affected measure docs together.
