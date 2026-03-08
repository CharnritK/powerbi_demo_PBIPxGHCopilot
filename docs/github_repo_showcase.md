# GitHub Repo Showcase Walkthrough

## What the repo should communicate

The repo should feel like a practical consulting accelerator:

- speaker-friendly notebooks at the front
- reusable Python code underneath
- a small explainable dataset
- PBIP assets that support a source-control and MCP story
- presenter notes that reduce live-demo risk

## Which files matter during the demo

### For the presenter

- `README.md`
- `notebooks/01_delegated_auth_demo.ipynb`
- `notebooks/02_service_principal_demo.ipynb`
- `docs/pbip_sample_design.md`
- `docs/architecture_flows.md`

### For developers

- `src/`
- `scripts/`
- `.env.example`
- `pyproject.toml`

### For Power BI developers

- `docs/pbip_sample_design.md`
- `data/*.csv`
- `pbip/README.md`

## Suggested walk-through order

1. Start at `README.md`.
2. Show the repo tree.
3. Open the delegated notebook.
4. Run workspace, dataset, and report listing.
5. Run a DAX query.
6. Contrast with the service principal notebook only if needed.
7. Open the PBIP design doc.
8. Close with architecture and auth trade-offs.

## Audience-specific focus

### Business audience

Focus on:

- what problem this solves
- why notebook-first is easier to trust
- what is and is not supported
- why auth choice matters for governance

### Developer audience

Focus on:

- reusable auth modules in `src/`
- environment-driven config
- clear API boundaries
- graceful error handling
- easy extension paths

### Power BI audience

Focus on:

- semantic model design
- PBIP source control
- DAX query mapping
- RLS implications
- workspace and dataset permissions
