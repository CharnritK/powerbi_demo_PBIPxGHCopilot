# Migration Summary

Major moves:

- `pbip/` -> `powerbi/workspaces/regional-sales-trust-demo/pbip/`
- `data/` -> `powerbi/workspaces/regional-sales-trust-demo/assets/data/`
- presentation and speaker docs -> `docs/presentation/`
- legacy root notebook removed; legacy all-in-one notebook retained as `notebooks/90_legacy_powerbi_rest_api_demo.ipynb`

Major additions:

- canonical `src/config`, `src/powerbi`, `src/mcp`, `src/semantic_model`, and `src/notebooksupport`
- canonical CLI entrypoints under `scripts/cli/`
- structured docs for architecture, conventions, domain, data model, operations, AI, and external repo contracts
- example YAML config templates and unit tests

Compatibility shims:

- top-level `scripts/*.py`
- `src/utils/*`
- `src/clients/*`
- `src/auth/*_auth.py`
- `src/demos/*`

Human review still needed:

- confirm final external repo names and ownership contacts
- confirm whether legacy `PBI_*` aliases should remain after one transition cycle
- confirm whether the solution folder name should stay `regional-sales-trust-demo`
