# Repo Architecture

This repo separates reusable code, runnable surfaces, Power BI assets, and documentation so both humans and AI agents can navigate it quickly.

Source-of-truth folders:

- `src/`: reusable Python
- `demo-enterprise/bi-repo/powerbi/workspaces/regional-sales-trust-demo/pbip/`: Power BI project assets
- `config/`: example configuration contracts
- `docs/data-model/`: semantic model rules and assumptions
- `docs/external-repos/`: ownership boundaries with other repos

Execution surfaces:

- `scripts/cli/`: canonical CLI entrypoints
- `notebooks/`: guided execution and demo notebooks
- `scripts/*.py` and `src/demos/*`: compatibility shims for older flows

Reference-only folders:

- `docs/presentation/`
- `references/`

Editing model:

- Put business logic in `src/`.
- Keep CLI argument parsing and notebook display code out of `src/`.
- Keep Power BI artifacts under `demo-enterprise/bi-repo/powerbi/`, never under `src/`.
