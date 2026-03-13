# Enterprise Demo Repository

This repository is a presentation-friendly demo that shows how BI and Data Engineering work would usually be split across separate repositories in an enterprise environment.

For demo purposes only, everything stays in one repo under [`demo-enterprise/`](./demo-enterprise):

- [`demo-enterprise/bi-repo/`](./demo-enterprise/bi-repo): BI developer responsibilities, including the Power BI project, semantic model, report shell, and BI-facing docs
- [`demo-enterprise/data-engineer-repo/`](./demo-enterprise/data-engineer-repo): a lightweight mock Data Engineering repo with notebooks, SQL, jobs, config, and placeholder transformation code
- [`demo-enterprise/shared/`](./demo-enterprise/shared): simple contracts and integration notes between the two areas

The existing Python utilities, notebooks, config templates, and tests remain in this repo because they support the live demo and local validation.

## Repository Layout

```text
.
|-- config/
|-- demo-enterprise/
|-- docs/
|-- notebooks/
|-- references/
|-- scripts/
|-- src/
`-- tests/
```

Key locations:

- [`demo-enterprise/bi-repo/powerbi/workspaces/regional-sales-trust-demo/pbip/`](./demo-enterprise/bi-repo/powerbi/workspaces/regional-sales-trust-demo/pbip): committed PBIP, PBIR, and TMDL files
- [`demo-enterprise/data-engineer-repo/`](./demo-enterprise/data-engineer-repo): mock upstream engineering structure for storytelling
- [`docs/architecture.md`](./docs/architecture.md): simple view of the demo architecture
- [`docs/enterprise-setup.md`](./docs/enterprise-setup.md): explains why the repo is organized this way
- [`docs/integration-overview.md`](./docs/integration-overview.md): describes the handoff between Data Engineering and BI

## Demo Story

In a real enterprise setup:

1. Data Engineering prepares curated tables or views.
2. BI developers consume those curated assets in a semantic model.
3. Reports, measures, and presentation logic are owned by the BI side.

This repository simulates that split without introducing actual multi-repo complexity, CI/CD, or working data pipelines.

## Power BI Demo Assets

The Power BI sample now lives under [`demo-enterprise/bi-repo/powerbi/workspaces/regional-sales-trust-demo/`](./demo-enterprise/bi-repo/powerbi/workspaces/regional-sales-trust-demo).

- `pbip/`: native Power BI project files
- `assets/data/`: committed CSV sample data used by the local semantic model
- `README.md`: guidance for opening and validating the demo model

If you open the PBIP on a different machine, update the semantic model `DataRootFolder` parameter to your local absolute path for `demo-enterprise/bi-repo/powerbi/workspaces/regional-sales-trust-demo/assets/data`.

## Supporting Code

The repo still includes:

- reusable Python modules under [`src/`](./src)
- CLI and helper scripts under [`scripts/`](./scripts)
- demo notebooks under [`notebooks/`](./notebooks)
- lightweight tests under [`tests/`](./tests)
- non-secret config templates under [`config/`](./config)

## Validation

```powershell
python -m compileall src scripts
python -m pytest -q
python scripts\cli\validate_tmdl_semantic_model.py
```
