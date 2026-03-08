# Power BI REST API Demo for Microsoft Fabric Trial

This repository is a small, notebook-first demo for showing how an existing Microsoft Entra app registration can call the Power BI REST API from a local machine.

The demo supports two authentication paths:

- `Delegated user authentication` is the recommended demo path. It is simpler for presenters, works well in a Fabric Trial setup, and matches what non-admin users usually need.
- `Service principal authentication` is included as an optional, admin-dependent path for automation-oriented scenarios.

The goal is to make the following demo flow easy to run and easy to explain:

1. Sign in or acquire an app token
2. List workspaces
3. List datasets in a workspace
4. List reports in a workspace
5. Run a very small DAX query against a semantic model

## Why delegated auth comes first

For a simple Fabric Trial demo, delegated auth is usually the least fragile option:

- no client secret is required
- device code flow works even when a localhost redirect URI is not configured
- the caller sees exactly what their signed-in user account can access
- the permission story is easier to explain to a live audience

Service principal auth is still useful, but it depends on tenant admin settings, workspace role assignment, and dataset limitations that often break a quick demo.

## Repository Structure

```text
.
|-- README.md
|-- requirements.txt
|-- .env.example
|-- notebooks/
|   |-- 01_delegated_auth_demo.ipynb
|   `-- 02_service_principal_demo.ipynb
|-- src/
|   |-- auth/
|   |   |-- __init__.py
|   |   |-- delegated_auth.py
|   |   `-- service_principal_auth.py
|   |-- clients/
|   |   |-- __init__.py
|   |   `-- powerbi_client.py
|   |-- demos/
|   |   |-- __init__.py
|   |   |-- execute_dax_query.py
|   |   |-- list_datasets.py
|   |   |-- list_reports.py
|   |   `-- list_workspaces.py
|   `-- utils/
|       |-- __init__.py
|       |-- config.py
|       `-- logging_utils.py
`-- docs/
    |-- auth_decision_guide.md
    |-- setup_checklist.md
    `-- troubleshooting.md
```

## Quick Start

Estimated time: 5 to 10 minutes, plus any tenant admin tasks you still need to complete.

1. Create and activate a virtual environment.
2. Install Python dependencies.
3. Copy `.env.example` to `.env`.
4. Fill in your tenant, app, workspace, and dataset values.
5. Complete the manual portal prerequisites in [docs/setup_checklist.md](/C:/Point/2026/Speaker/PBIPxCopilot/powerbi_demo_PBIPxGHCopilot/docs/setup_checklist.md).
6. Start with the delegated notebook in [notebooks/01_delegated_auth_demo.ipynb](/C:/Point/2026/Speaker/PBIPxCopilot/powerbi_demo_PBIPxGHCopilot/notebooks/01_delegated_auth_demo.ipynb).

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python -m notebook notebooks\01_delegated_auth_demo.ipynb
```

If you want an installed kernel for the virtual environment:

```powershell
python -m ipykernel install --user --name powerbi-rest-demo --display-name "Python (powerbi-rest-demo)"
```

## Environment Variables

Keep all values local in `.env`. Do not commit secrets.

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

- `CLIENT_SECRET` is only needed for the service principal notebook and scripts.
- `REDIRECT_URI` is optional for the primary device code path.
- `IMPERSONATED_USER_NAME` is optional and should only be used when the dataset and identity scenario support it.

## Run the Demos

Notebook-first path:

- [notebooks/01_delegated_auth_demo.ipynb](/C:/Point/2026/Speaker/PBIPxCopilot/powerbi_demo_PBIPxGHCopilot/notebooks/01_delegated_auth_demo.ipynb)
- [notebooks/02_service_principal_demo.ipynb](/C:/Point/2026/Speaker/PBIPxCopilot/powerbi_demo_PBIPxGHCopilot/notebooks/02_service_principal_demo.ipynb)

Script examples:

```powershell
python -m src.demos.list_workspaces --auth-mode delegated
python -m src.demos.list_datasets --group-id <workspace-id> --auth-mode delegated
python -m src.demos.list_reports --group-id <workspace-id> --auth-mode delegated
python -m src.demos.execute_dax_query --group-id <workspace-id> --dataset-id <dataset-id> --auth-mode delegated
```

Optional service principal examples:

```powershell
python -m src.demos.list_workspaces --auth-mode service_principal
python -m src.demos.list_datasets --group-id <workspace-id> --auth-mode service_principal
```

## Admin-Required Service Principal Warning

Treat service principal auth as `admin-required / automation-oriented`.

It depends on:

- a client secret that you manage outside source control
- Power BI tenant settings that allow service principals to use the REST APIs
- possibly an allowed Entra security group, depending on tenant policy
- workspace membership for the service principal
- dataset-specific limitations, especially for `executeQueries` when RLS or SSO is enabled

If you only need a presentation-friendly Fabric Trial demo, start with delegated auth.

## Screenshot Placeholders

Add your own screenshots later in these spots:

> Screenshot placeholder: device code prompt and successful sign-in confirmation

> Screenshot placeholder: workspace table in the delegated notebook

> Screenshot placeholder: dataset / report list and DAX query output

> Screenshot placeholder: service principal warning callout or admin settings page

## Documentation

- [docs/setup_checklist.md](/C:/Point/2026/Speaker/PBIPxCopilot/powerbi_demo_PBIPxGHCopilot/docs/setup_checklist.md)
- [docs/auth_decision_guide.md](/C:/Point/2026/Speaker/PBIPxCopilot/powerbi_demo_PBIPxGHCopilot/docs/auth_decision_guide.md)
- [docs/troubleshooting.md](/C:/Point/2026/Speaker/PBIPxCopilot/powerbi_demo_PBIPxGHCopilot/docs/troubleshooting.md)

## Presenter Demo Script

What to click:

1. Open the repo root in VS Code or Jupyter.
2. Open [notebooks/01_delegated_auth_demo.ipynb](/C:/Point/2026/Speaker/PBIPxCopilot/powerbi_demo_PBIPxGHCopilot/notebooks/01_delegated_auth_demo.ipynb).
3. Run cells from top to bottom.
4. If needed, open [notebooks/02_service_principal_demo.ipynb](/C:/Point/2026/Speaker/PBIPxCopilot/powerbi_demo_PBIPxGHCopilot/notebooks/02_service_principal_demo.ipynb) to explain the automation path and its caveats.

What to run:

1. Load configuration
2. Acquire token
3. List workspaces
4. List datasets
5. List reports
6. Execute a tiny DAX query

What to say:

- "This notebook shows the same Power BI REST API pattern under two identities."
- "Delegated auth reflects the signed-in user and is the simplest path for a trial demo."
- "Service principal auth is better for unattended automation, but it depends on admin settings."
- "The data access result is shaped by workspace access, dataset permissions, and tenant policy."

What caveats to mention:

- tenant admin settings cannot be fixed in code
- service principal access may still be blocked even when the app registration exists
- `executeQueries` has identity caveats, especially with RLS and SSO
- a Fabric Trial workspace does not automatically remove all Power BI licensing requirements

## Validation Notes

The code is ready to run locally after you:

1. fill in `.env`
2. complete the admin and workspace prerequisites
3. confirm the target dataset supports the endpoints you want to show
