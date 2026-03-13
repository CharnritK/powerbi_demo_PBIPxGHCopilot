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
4. Optional: if your team prefers the loader fallback under `config/`, copy `config/.env.example` to `config/.env` instead of using a repo-root `.env`

Notes:

- `.env.example` at the repo root is the canonical template.
- The loader checks the repo-root `.env` first, then `config/.env` if the repo-root file is absent.
- Legacy `PBI_*` environment variable aliases still work, but new examples use canonical names.

Primary local commands:

```powershell
python scripts/cli/check_auth.py
python scripts/cli/list_workspaces.py --auth-mode delegated
python scripts/cli/validate_tmdl_semantic_model.py
python -m notebook notebooks/01_delegated_auth_demo.ipynb
```

PBIP sample check:

- open `demo-enterprise/bi-repo/powerbi/workspaces/regional-sales-trust-demo/pbip/demo_dataset.pbip`
- compute the local sample-data path with `Resolve-Path .\demo-enterprise\bi-repo\powerbi\workspaces\regional-sales-trust-demo\assets\data`
- if `DataRootFolder` still points at the originally committed machine path, update it in Power BI Desktop or through the documented MCP/local workflow before refresh
- set `DataRootFolder` to the absolute path of `demo-enterprise/bi-repo/powerbi/workspaces/regional-sales-trust-demo/assets/data` on your machine
- re-run `python scripts/cli/validate_tmdl_semantic_model.py` after any structural semantic-model edit; note that this validator does not rewrite or verify local machine paths
