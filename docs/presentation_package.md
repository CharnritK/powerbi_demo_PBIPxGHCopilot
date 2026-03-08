# Presentation Package

## Goal

This repo package is meant to survive a live session without surprise setup detours. The main story is:

- delegated auth for the safest live demo path
- service principal auth as the automation comparison
- a local PBIP model to connect the REST story to semantic model source control and MCP tooling

## Canonical Demo Path

Use these assets in this order:

1. `README.md`
2. `docs/setup_checklist.md`
3. `notebooks/01_delegated_auth_demo.ipynb`
4. `notebooks/02_service_principal_demo.ipynb` only if you want the admin-dependent comparison
5. `pbip/demo_dataset.pbip`
6. `docs/presenter_demo_script.md`

## Repo Surfaces

- `README.md`: single entry point for setup and demo flow
- `.env.example`: canonical config template
- `src/`: primary reusable Python implementation
- `scripts/`: compatibility helpers for workshop-style notebook flows
- `notebooks/`: speaker-facing entrypoints
- `pbip/`: local semantic model and report shell
- `docs/`: presenter notes, setup guidance, and showcase material

## Packaging Checklist

Before the session:

1. Confirm `.env` is filled in from `.env.example`.
2. Verify delegated auth works with the presenter account.
3. Decide whether service principal is safe enough to show in that tenant.
4. Refresh the PBIP sample once in Power BI Desktop.
5. Capture any backup screenshots in `images/`.

## Minimum Demo Inventory

- `README.md`
- `.env.example`
- `requirements.txt`
- `notebooks/01_delegated_auth_demo.ipynb`
- `notebooks/02_service_principal_demo.ipynb`
- `src/`
- `pbip/`
- `docs/setup_checklist.md`
- `docs/troubleshooting.md`

## Optional Extras

- `notebooks/powerbi_rest_api_demo.ipynb` for an all-in-one workshop path
- screenshots in `images/`
- architecture slides and presenter notes under `docs/`
