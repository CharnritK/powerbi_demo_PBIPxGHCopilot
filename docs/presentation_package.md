# 1. Assumptions

- The audience is mixed: business stakeholders, BI developers, analytics engineers, and consultants.
- The primary presentation goal is education and implementation clarity, not exhaustive platform coverage.
- The main demo should be low-friction and resilient in a live session.
- The demo uses a small regional sales scenario because it is business-friendly and easy to explain.
- The notebook is the primary entry point, and scripts are the reusable technical engine.
- The repo package is intended for GitHub and live presentation.
- Tenant settings, workspace permissions, licensing, and feature availability can vary by environment.

# 2. Suggested end-to-end demo concept

Name: **Power BI REST API Auth Demo**

Story:
A BI team wants one demo package that shows how a notebook can become a simple front end for Power BI REST API operations while still supporting reusable scripts for developers. The same workflow is shown under two identities:
- service principal for automation
- delegated user for user-context execution

Demo sequence:
1. Open the repo and show that it is organized for both presenters and developers
2. Open the notebook and select auth mode
3. List visible workspaces
4. List datasets in a workspace
5. Execute a DAX query
6. Show a simple table and chart
7. Explain why the same interface behaves differently depending on auth choice
8. Close with prerequisites, RLS implications, and known limitations

# 3. Recommended repo structure

```text
powerbi-rest-auth-demo/
├─ README.md
├─ requirements.txt
├─ config/
│  └─ .env.example
├─ data/
│  ├─ dim_channel.csv
│  ├─ dim_date.csv
│  ├─ dim_product.csv
│  ├─ dim_region.csv
│  ├─ fact_sales.csv
│  └─ security_region_access.csv
├─ docs/
│  ├─ architecture_flows.md
│  ├─ github_repo_showcase.md
│  ├─ pbip_sample_design.md
│  ├─ presentation_package.md
│  ├─ presenter_demo_script.md
│  ├─ presenter_notes_th.md
│  └─ visual_ux_recommendations.md
├─ images/
│  └─ .gitkeep
├─ notebooks/
│  └─ powerbi_rest_api_demo.ipynb
├─ pbip/
│  └─ README.md
├─ scripts/
│  ├─ auth_delegated_user.py
│  ├─ auth_service_principal.py
│  ├─ config_loader.py
│  ├─ execute_dax_query.py
│  ├─ list_datasets.py
│  ├─ list_workspaces.py
│  └─ powerbi_client.py
└─ tests/
   └─ README.md
```

Purpose:
- `/docs` = presentation and explanation assets
- `/notebooks` = guided demo interface
- `/scripts` = reusable technical engine
- `/pbip` = PBIP design guidance
- `/data` = sample CSVs for the semantic model
- `/images` = screenshots and slide images
- `/config` = environment and config templates
- `/tests` = optional validation assets

# 4. README.md draft

See the full file at `README.md`.

# 5. Sample PBIP design

See the full design at `docs/pbip_sample_design.md`.

# 6. Sample data design

The sample data lives under `/data`.

Core tables:
- `fact_sales.csv`
- `dim_date.csv`
- `dim_region.csv`
- `dim_product.csv`
- `dim_channel.csv`
- `security_region_access.csv`

Example rows:
- Fact row: `1001,20260105,1,101,1,6,7200,4200`
- Region row: `1,North,Thailand,Anan Wong`
- Product row: `101,Power BI Starter,Analytics Package,1200,700`

# 7. Python scripts

Scripts provided:
- `scripts/auth_service_principal.py`
- `scripts/auth_delegated_user.py`
- `scripts/config_loader.py`
- `scripts/list_workspaces.py`
- `scripts/list_datasets.py`
- `scripts/execute_dax_query.py`
- `scripts/powerbi_client.py`

# 8. Notebook design + notebook content

Primary notebook:
- `notebooks/powerbi_rest_api_demo.ipynb`

Flow:
1. Introduction
2. Prerequisites
3. Load config
4. Select auth mode
5. List workspaces
6. Choose workspace
7. List datasets
8. Choose dataset
9. Run DAX query
10. Show results table
11. Show optional chart
12. Final summary

# 9. Auth comparison table

| Topic | Service Principal | Delegated User |
|---|---|---|
| Best for | Automation, backend jobs, app-owned execution | User-context tooling, demos, analyst utilities |
| Identity | Application identity | Signed-in user identity |
| Setup | Tenant enablement + workspace access | App registration + delegated scopes + user access |
| RLS story | Not appropriate for `executeQueries` on RLS-enabled datasets | Better fit when access should reflect user context |
| Demo fit | Great for admin-free automation story | Great for explaining real user access |
| Secret handling | Needs secret/cert management | No client secret for public client flow |

Presenter explanation:
Service principal is your clean automation path. Delegated auth is your clean user-context path. They can share the same notebook interface, but they do not have the same security and RLS behavior.

# 10. Architecture / flow content

See `docs/architecture_flows.md`.

# 11. GitHub repo showcase walkthrough

See `docs/github_repo_showcase.md`.

# 12. Presenter demo script

See `docs/presenter_demo_script.md`.

# 13. Thai presenter notes

See `docs/presenter_notes_th.md`.

# 14. Visual / UX recommendations

See `docs/visual_ux_recommendations.md`.

# 15. Final checklist of files to generate

Required:
- README.md
- requirements.txt
- config/.env.example
- notebooks/powerbi_rest_api_demo.ipynb
- scripts/*.py
- docs/*.md
- data/*.csv
- images/ screenshots during final packaging

Optional polished extras:
- backup screenshots for each notebook step
- architecture diagram PNG/SVG
- slide-ready repo tree image
- second notebook for RLS extension

# A. Minimum viable demo package

- README.md
- one notebook
- service principal auth script
- delegated auth script
- workspace listing script
- dataset listing script
- DAX query script
- sample CSV data
- PBIP design doc
- presenter notes

# B. Polished showcase package

Everything in the minimum package, plus:
- backup screenshots
- architecture visuals
- Thai presenter notes
- repo walkthrough doc
- visual/UX recommendation doc
- tests placeholder
- refined README and speaking script

# C. Prioritized implementation order

1. Create sample data
2. Build semantic model and report manually in Power BI Desktop
3. Save real PBIP from Desktop
4. Implement config loader and auth scripts
5. Implement workspace / dataset / DAX scripts
6. Build notebook on top of scripts
7. Write README and architecture docs
8. Prepare presenter notes and screenshots
9. Add optional RLS extension scenario
