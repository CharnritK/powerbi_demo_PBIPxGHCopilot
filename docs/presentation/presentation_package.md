# Presentation Package

## Goal

This repo package is meant to survive a live technical session without surprise setup detours. The main story is trustworthy enterprise BI delivery, not just calling an API.

- trust in production matters more than raw build speed
- delegated auth is the safest live demo path
- service principal auth is the optional automation comparison
- PBIP, PBIR, and TMDL connect the REST story to source control, validation guardrails, and inspectable artifacts
- AI-assisted tooling extends the existing Power BI toolbox with practical automation around metadata, documentation, and validation

## Canonical Demo Path

Use these assets in this order:

1. `docs/session_messaging.md`
2. `README.md`
3. `docs/setup_checklist.md`
4. `notebooks/01_delegated_auth_demo.ipynb`
5. `notebooks/02_service_principal_demo.ipynb` only if you want the admin-dependent comparison
6. `pbip/demo_dataset.pbip`
7. `docs/presenter_demo_script.md`

## Repo Surfaces

- `docs/session_messaging.md`: source of truth for title, abstract, opening hook, and scope boundaries
- `README.md`: single entry point for setup and demo flow
- `.env.example`: canonical config template
- `src/`: primary reusable Python implementation
- `scripts/`: compatibility helpers for workshop-style notebook flows
- `notebooks/`: speaker-facing entrypoints
- `pbip/`: local semantic model and report shell
- `docs/`: presenter notes, setup guidance, architecture, and showcase material

## Packaging Checklist

Before the session:

1. Rehearse the opening hook and session scope from `docs/session_messaging.md`.
2. Confirm `.env` is filled in from `.env.example`.
3. Verify delegated auth works with the presenter account.
4. Decide whether service principal is safe enough to show in that tenant.
5. Refresh the PBIP sample once in Power BI Desktop.
6. Capture any backup screenshots in `images/`.

## Minimum Demo Inventory

- `docs/session_messaging.md`
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
