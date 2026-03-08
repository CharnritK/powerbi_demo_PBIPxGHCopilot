# Tests

This repo is demo-first, so automated coverage is still light.

Useful local checks:

- `python -m compileall src scripts`
- `python -m src.demos.list_workspaces --auth-mode delegated`
- `python scripts\demo_dataset_mcp_smoke_test.py`

Future improvements:

- unit tests for config loading and auth-mode normalization
- mocked API tests for workspace, dataset, report, and DAX query calls
- notebook smoke execution in CI
