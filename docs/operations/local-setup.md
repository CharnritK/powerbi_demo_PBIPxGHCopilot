# Local Setup

Prerequisites:

- Python 3.10+
- Power BI Desktop
- VS Code plus the Power BI Modeling MCP extension if you want local MCP workflows

Install:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Configure:

1. Copy `.env.example` to `.env`
2. Fill in `TENANT_ID`, `CLIENT_ID`, `WORKSPACE_ID`, and `DATASET_ID`
3. Add `CLIENT_SECRET` only if you need service principal auth

Primary local commands:

```powershell
python scripts/cli/check_auth.py
python scripts/cli/list_workspaces.py --auth-mode delegated
python scripts/cli/validate_tmdl_semantic_model.py
python -m notebook notebooks/01_delegated_auth_demo.ipynb
```

PBIP sample check:

- open `powerbi/workspaces/regional-sales-trust-demo/pbip/demo_dataset.pbip`
- confirm `DataRootFolder` resolves to `powerbi/workspaces/regional-sales-trust-demo/assets/data`
