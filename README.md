# Power BI REST API and PBIP Modeling Demo

This repo is tuned for a live speaker session. It combines:

- a notebook-first Power BI REST API demo
- a local PBIP semantic model for Power BI Modeling MCP demos
- lightweight Python entrypoints that presenters can explain without extra setup noise

The primary presentation path is delegated auth first, then an optional service principal comparison.

## Speaker Path

Start here for the lowest-friction live demo:

1. Read [`docs/setup_checklist.md`](docs/setup_checklist.md).
2. Fill in a local `.env` from [`.env.example`](.env.example).
3. Run [`notebooks/01_delegated_auth_demo.ipynb`](notebooks/01_delegated_auth_demo.ipynb).
4. Use [`notebooks/02_service_principal_demo.ipynb`](notebooks/02_service_principal_demo.ipynb) only if you want to show the automation identity path.
5. Use the PBIP sample under [`pbip/`](pbip/README.md) for the local semantic model segment.

Older all-in-one notebook and `scripts/` helpers are still present for workshop variations. They now read the same canonical `.env` values as the split notebook flow.

## Repo Layout

```text
.
|-- README.md
|-- .env.example
|-- pyproject.toml
|-- requirements.txt
|-- requirements-dev.txt
|-- config/
|   `-- settings.example.json
|-- data/
|-- docs/
|-- notebooks/
|   |-- 01_delegated_auth_demo.ipynb
|   |-- 02_service_principal_demo.ipynb
|   `-- powerbi_rest_api_demo.ipynb
|-- pbip/
|   |-- README.md
|   |-- demo_dataset.pbip
|   |-- demo_dataset.Report/
|   `-- demo_dataset.SemanticModel/
|-- scripts/
|-- src/
`-- tests/
```

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python -m notebook notebooks\01_delegated_auth_demo.ipynb
```

If you want the development extras:

```powershell
pip install -r requirements-dev.txt
```

If you want a named notebook kernel:

```powershell
python -m ipykernel install --user --name powerbi-rest-demo --display-name "Python (powerbi-rest-demo)"
```

## Configuration

The canonical config contract is the root `.env` file. Use these names:

```dotenv
TENANT_ID=
CLIENT_ID=
CLIENT_SECRET=
WORKSPACE_ID=
DATASET_ID=
DAX_QUERY=EVALUATE ROW("Demo", 1)
IMPERSONATED_USER_NAME=
AUTH_MODE=delegated
REDIRECT_URI=http://localhost
USE_DEVICE_CODE=true
LOG_LEVEL=INFO
TOKEN_CACHE_PATH=.local/msal_token_cache.bin
REQUEST_TIMEOUT_SECONDS=60
```

Notes:

- `AUTH_MODE=delegated` is the recommended speaker default.
- `CLIENT_SECRET` is only required for service principal demos.
- `config/settings.example.json` is an optional local template for script-heavy workflows.
- Legacy `PBI_*` variable names are still accepted for compatibility, but the docs and examples use the canonical names above.

## Run the Demo Flows

Notebook-first:

- [`notebooks/01_delegated_auth_demo.ipynb`](notebooks/01_delegated_auth_demo.ipynb)
- [`notebooks/02_service_principal_demo.ipynb`](notebooks/02_service_principal_demo.ipynb)

Python CLI examples:

```powershell
python -m src.demos.list_workspaces --auth-mode delegated
python -m src.demos.list_datasets --group-id <workspace-id> --auth-mode delegated
python -m src.demos.list_reports --group-id <workspace-id> --auth-mode delegated
python -m src.demos.execute_dax_query --group-id <workspace-id> --dataset-id <dataset-id> --auth-mode delegated
```

Optional service principal comparison:

```powershell
python -m src.demos.list_workspaces --auth-mode service_principal
python -m src.demos.list_datasets --group-id <workspace-id> --auth-mode service_principal
```

## PBIP Modeling MCP

The repo already includes a local PBIP sample at `pbip/demo_dataset.pbip`.

```powershell
python scripts\setup_powerbi_modeling_mcp.py
python scripts\demo_dataset_mcp_smoke_test.py
```

Typical MCP prompt:

```text
Open semantic model from PBIP folder '<repo-root>\pbip\demo_dataset.SemanticModel\definition'
```

What the smoke test covers:

- confirms the `DataRootFolder` Power Query parameter exists
- rewrites CSV partitions to use that parameter
- adds a small set of demo measures
- exports the semantic model back to the PBIP TMDL folder
- reopens the PBIP file in Power BI Desktop and validates the refreshed result

If you move the repo later, update `DataRootFolder` once instead of editing every table query.

## Documentation

- [`docs/setup_checklist.md`](docs/setup_checklist.md)
- [`docs/auth_decision_guide.md`](docs/auth_decision_guide.md)
- [`docs/pbip_sample_design.md`](docs/pbip_sample_design.md)
- [`docs/troubleshooting.md`](docs/troubleshooting.md)
- [`docs/github_repo_showcase.md`](docs/github_repo_showcase.md)
- [`docs/presenter_demo_script.md`](docs/presenter_demo_script.md)

## Presenter Notes

Recommended live order:

1. Open `README.md` and the repo tree.
2. Run the delegated notebook.
3. Show workspace, dataset, report, and DAX query results.
4. Explain why delegated auth is the safest live-demo default.
5. Open the service principal notebook only for caveats and automation framing.
6. Finish with the PBIP semantic model and MCP workflow.

Keep these caveats explicit:

- tenant admin settings cannot be fixed in code during the session
- service principal access depends on tenant policy and workspace membership
- `executeQueries` may fail for service principal auth on RLS or SSO-enabled datasets
- a Fabric Trial workspace does not remove every Power BI licensing dependency
