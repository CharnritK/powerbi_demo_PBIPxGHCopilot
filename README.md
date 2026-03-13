# Enterprise BI Engineering Repository

This repository is a working Power BI and analytics engineering workspace. It is designed for BI developers, analytics engineers, solution architects, and AI coding agents who need source-controlled Power BI assets, reusable Python utilities, notebook-friendly execution, and practical documentation.

The business theme remains the same as the original demo: trustworthy Power BI delivery. The repo now treats that theme as an engineering operating model rather than a speaker-first package.

## What This Repo Owns

- Reusable Python modules for auth, Power BI REST access, semantic-model inspection, MCP helpers, and notebook bootstrap
- A source-controlled PBIP sample and local semantic model under [`powerbi/`](./powerbi)
- Demo and operator notebooks under [`notebooks/`](./notebooks)
- Enterprise-oriented documentation under [`docs/`](./docs)
- Lightweight unit tests under [`tests/`](./tests)
- Non-secret config templates under [`config/`](./config)

## What This Repo Does Not Own

- CI/CD pipelines or deployment automation
- Lakehouse, warehouse, or ingestion pipelines
- Report publishing processes across environments
- Enterprise identity secrets in source control

## Repository Layout

```text
.
|-- config/
|-- docs/
|-- notebooks/
|-- powerbi/
|-- references/
|-- scripts/
|-- src/
`-- tests/
```

Key source-of-truth locations:

- [`src/`](./src): reusable Python code
- [`powerbi/workspaces/regional-sales-trust-demo/pbip/`](./powerbi/workspaces/regional-sales-trust-demo/pbip): Power BI project assets
- [`docs/data-model/`](./docs/data-model): semantic model documentation
- [`docs/external-repos/`](./docs/external-repos): boundaries with upstream and downstream repos
- [`config/`](./config): example configuration contracts

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python -m notebook notebooks\01_delegated_auth_demo.ipynb
```

Development extras:

```powershell
pip install -r requirements-dev.txt
python -m pytest -q
```

## Configuration and Auth

Use `.env.example` as the canonical secret template. Non-secret defaults and naming rules live in [`config/`](./config).

Primary environment variables:

- `TENANT_ID`
- `CLIENT_ID`
- `CLIENT_SECRET`
- `WORKSPACE_ID`
- `DATASET_ID`
- `AUTH_MODE`
- `REDIRECT_URI`
- `USE_DEVICE_CODE`
- `TOKEN_CACHE_PATH`
- `REQUEST_TIMEOUT_SECONDS`

Legacy `PBI_*` aliases are still supported for compatibility with the older workshop flow.

See [`docs/operations/local-setup.md`](./docs/operations/local-setup.md) and [`docs/operations/auth-prerequisites.md`](./docs/operations/auth-prerequisites.md).

## Running the Repo

Canonical CLI entrypoints:

- `python scripts/cli/check_auth.py`
- `python scripts/cli/list_workspaces.py --auth-mode delegated`
- `python scripts/cli/list_datasets.py --group-id <workspace-id>`
- `python scripts/cli/list_reports.py --group-id <workspace-id>`
- `python scripts/cli/execute_dax_query.py --group-id <workspace-id> --dataset-id <dataset-id>`
- `python scripts/cli/export_metadata.py --group-id <workspace-id>`
- `python scripts/cli/generate_measure_docs.py`
- `python scripts/cli/validate_tmdl_semantic_model.py`

Compatibility wrappers remain under [`scripts/`](./scripts) and [`src/demos/`](./src/demos) so older demo paths still work.

## Power BI Assets

The Power BI sample lives under [`powerbi/workspaces/regional-sales-trust-demo/`](./powerbi/workspaces/regional-sales-trust-demo).

- `pbip/`: native PBIP, PBIR, and TMDL files
- `assets/data/`: committed sample CSVs used by the local semantic model
- `README.md`: local asset contract and safe-edit guidance

## Documentation

Start with [`docs/README.md`](./docs/README.md).

- Architecture: [`docs/architecture/`](./docs/architecture)
- Conventions: [`docs/conventions/`](./docs/conventions)
- Domain and KPIs: [`docs/domain/`](./docs/domain)
- Data model: [`docs/data-model/`](./docs/data-model)
- Operations: [`docs/operations/`](./docs/operations)
- External repo boundaries: [`docs/external-repos/`](./docs/external-repos)
- AI agent guidance: [`docs/ai/`](./docs/ai)
- Presentation assets: [`docs/presentation/`](./docs/presentation)

## Relationship to External Repositories

This repo assumes upstream curated data products and downstream BI/report collaboration, but it does not duplicate those repositories here.

- Data Engineering contract: [`docs/external-repos/data-engineering-repo-contract.md`](./docs/external-repos/data-engineering-repo-contract.md)
- BI Developer contract: [`docs/external-repos/bi-developer-repo-contract.md`](./docs/external-repos/bi-developer-repo-contract.md)

## Validation

Local validation currently focuses on:

- config loading and auth setup
- Power BI REST metadata calls
- DAX query execution
- TMDL semantic-model validation
- PBIP/MCP local demo workflows

Run:

```powershell
python -m compileall src scripts
python -m pytest -q
```
