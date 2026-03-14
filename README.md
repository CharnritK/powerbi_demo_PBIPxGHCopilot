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
- [`docs/measure-validation.md`](./docs/measure-validation.md): PBIP-aware measure validation template workflow

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
- persisted notebook demo outputs under [`test-results/`](./test-results)
- lightweight tests under [`tests/`](./tests)
- non-secret config templates under [`config/`](./config)

## Presentation Demo Flow

The current presentation package lives under [`docs/presentation/`](./docs/presentation/).

Primary files:

- [`docs/presentation/presentation_outline.md`](./docs/presentation/presentation_outline.md)
- [`docs/presentation/demo_walkthrough.md`](./docs/presentation/demo_walkthrough.md)
- [`docs/presentation/speaker_notes.md`](./docs/presentation/speaker_notes.md)
- [`docs/presentation/repo_presentation_gap_analysis.md`](./docs/presentation/repo_presentation_gap_analysis.md)
- [`docs/presentation/draft_slide_content.md`](./docs/presentation/draft_slide_content.md)

For the current presenter environment, the canonical live-demo path uses **service principal** auth rather than delegated auth.

Canonical live order:

1. `README.md`
2. top-level repo tree
3. `docs/architecture/repo-architecture.md`
4. `demo-enterprise/bi-repo/powerbi/workspaces/regional-sales-trust-demo/pbip/`
5. `demo-enterprise/bi-repo/powerbi/workspaces/regional-sales-trust-demo/pbip/demo_dataset.SemanticModel/definition/tables/Fact Sales.tmdl`
6. `demo-enterprise/bi-repo/powerbi/workspaces/regional-sales-trust-demo/pbip/demo_dataset.SemanticModel/definition/relationships.tmdl`
7. `demo-enterprise/bi-repo/powerbi/workspaces/regional-sales-trust-demo/pbip/demo_dataset.Report/definition/pages/pages.json`
8. `notebooks/02_service_principal_demo.ipynb`
9. `notebooks/03_measure_validation_showcase.ipynb`
10. `tests/measure-validation/templates/measure_validation_template.csv`
11. `tests/measure-validation/generated/report_measure_coverage.csv`
12. `test-results/demo-dataset/2026-03-14_001534/`

Short limitation note:
service principal is the practical working demo path for this session, but tenant settings, workspace membership, and dataset features such as RLS or SSO can still block `executeQueries`.

## Validation

```powershell
python -m compileall src scripts
python -m pytest -q
python -m jupyter nbconvert --to notebook --execute notebooks/03_measure_validation_showcase.ipynb --output 03_measure_validation_showcase.executed.ipynb --output-dir tmp/jupyter-notebook
python scripts\cli\validate_tmdl_semantic_model.py
python scripts\evaluate_pbip_for_testing.py
python scripts\generate_measure_test_scenarios.py
python scripts\generate_measure_validation_template.py
```
