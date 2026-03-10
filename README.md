# Enterprise BI Engineering: Building Trustworthy Power BI with PBIP/PBIR, GitHub Copilot & AI

This repo is tuned for a live speaker session and practical technical demos. The core question is not "Can we build it?" It is "Can we trust it in production?"

The repo frames Power BI as an engineering discipline by combining:

- a notebook-first, delegated-auth-first demo path for reliable live delivery
- PBIP, PBIR, and TMDL assets that are source-controlled, reviewable, and diffable
- a local semantic model sample that supports validation, report-structure inspection, and MCP demos
- lightweight Python entrypoints that show how BI developers can build practical tooling around REST APIs, documentation, and validation workflows

This is a developer-oriented session repo. It focuses on trustworthy enterprise BI delivery, validation guardrails, and AI-assisted tooling. It does not position AI as a replacement for reviewer judgment, and it does not claim full report-page UI regression testing.

## Core Story

- Version Control: Treat BI assets as source-controlled artifacts. PBIP, PBIR, and TMDL make semantic model and report changes easier to inspect and review.
- Guardrails: Validate before deployment. Schema checks, measure checks, deployment validation, and early risk detection matter more than raw build speed.
- Custom Toolbox: DAX Studio, ALM Toolkit, and Tabular Editor remain valuable. AI-assisted development extends that toolbox by making lightweight automations around Power BI REST APIs and metadata inspection more accessible.

The primary presentation path is delegated auth first, then an optional service principal comparison.

## Speaker Path

Start here for the lowest-friction live demo:

1. Read [`docs/session_messaging.md`](docs/session_messaging.md).
2. Read [`docs/setup_checklist.md`](docs/setup_checklist.md).
3. Fill in a local `.env` from [`.env.example`](.env.example).
4. Run [`notebooks/01_delegated_auth_demo.ipynb`](notebooks/01_delegated_auth_demo.ipynb).
5. Use [`notebooks/02_service_principal_demo.ipynb`](notebooks/02_service_principal_demo.ipynb) only if you want to show the automation identity path.
6. Use the PBIP sample under [`pbip/`](pbip/README.md) for the semantic model, source-control, and validation segment.

Older all-in-one notebook and `scripts/` helpers are still present for workshop variations. They now read the same canonical `.env` values as the split notebook flow.

## What the Demo Shows

- delegated auth as the safest presenter default and the cleanest path for user-context validation
- service principal auth as the optional automation comparison, with its tenant and dataset caveats kept explicit
- REST API metadata calls and a small DAX query as practical building blocks, not the whole story
- PBIP/PBIR/TMDL artifacts as structured inputs that tooling and reviewers can inspect
- AI-assisted tooling ideas such as drafting validation scenarios from metadata, improving documentation, and helping BI developers build small internal utilities

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

This sample anchors the source-control and trustworthy-delivery part of the story:

- PBIP/PBIR/TMDL make semantic model and report artifacts inspectable
- lightweight MCP operations show how model changes can be scripted and reviewed
- the sample model is small enough for a live demo, but realistic enough for measure checks, risk discussion, and deployment-validation framing

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

- [`docs/session_messaging.md`](docs/session_messaging.md)
- [`docs/setup_checklist.md`](docs/setup_checklist.md)
- [`docs/auth_decision_guide.md`](docs/auth_decision_guide.md)
- [`docs/architecture_flows.md`](docs/architecture_flows.md)
- [`docs/pbip_sample_design.md`](docs/pbip_sample_design.md)
- [`docs/troubleshooting.md`](docs/troubleshooting.md)
- [`docs/github_repo_showcase.md`](docs/github_repo_showcase.md)
- [`docs/presenter_demo_script.md`](docs/presenter_demo_script.md)

## Presenter Notes

Recommended live order:

1. Open `README.md` and state the trust-in-production framing.
2. Run the delegated notebook.
3. Show workspace, dataset, report, and DAX query results.
4. Explain why delegated auth is the safest live-demo default.
5. Open the service principal notebook only for caveats and automation framing.
6. Finish with the PBIP semantic model, structured artifacts, and AI-assisted tooling story.

Keep these caveats explicit:

- tenant admin settings cannot be fixed in code during the session
- service principal access depends on tenant policy and workspace membership
- `executeQueries` may fail for service principal auth on RLS or SSO-enabled datasets
- a Fabric Trial workspace does not remove every Power BI licensing dependency
