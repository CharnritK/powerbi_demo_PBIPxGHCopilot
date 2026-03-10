# GitHub Repo Showcase Walkthrough

## What the Repo Should Communicate

The repo should feel like a practical enterprise BI engineering demo:

- notebook-first for a presenter-friendly live path
- source-controlled Power BI artifacts, not just screenshots or binaries
- validation guardrails before deployment
- lightweight Python tooling that is small enough to explain live
- AI-assisted development as a way to extend the toolbox, not replace trusted tools
- honest scope: semantic model and deployment validation, not full UI regression testing

## Which Files Matter During the Demo

### For Narrative and Session Framing

- `docs/session_messaging.md`
- `README.md`
- `docs/presenter_demo_script.md`

### For the Live Demo Path

- `notebooks/01_delegated_auth_demo.ipynb`
- `notebooks/02_service_principal_demo.ipynb`
- `docs/auth_decision_guide.md`
- `docs/setup_checklist.md`

### For the Engineering Story

- `docs/pbip_sample_design.md`
- `docs/architecture_flows.md`
- `pbip/`
- `src/`
- `scripts/`

## Suggested Walk-Through Order

1. Start at `docs/session_messaging.md` or summarize it verbally.
2. Open `README.md`.
3. Show the repo tree.
4. Open the delegated notebook.
5. Run workspace, dataset, and report listing.
6. Run a small DAX query.
7. Explain why delegated auth is the trusted live default.
8. Contrast with the service principal notebook only if needed.
9. Open the PBIP design doc.
10. Open the architecture flow doc.
11. Close on validation guardrails and AI-assisted tooling.

## Key Talking Points While Browsing the Repo

- Start with the production-trust question, not with AI novelty.
- Point out that PBIP, PBIR, and TMDL turn BI assets into inspectable artifacts.
- Explain that PBIR matters because tools can inspect report structure and draft realistic validation scenarios.
- Show that notebooks are the teaching surface, while `src/` and `scripts/` are the reusable engineering layer.
- Mention that DAX Studio, ALM Toolkit, and Tabular Editor still matter; this repo shows how AI-assisted development can extend that toolbox.
- Keep the focus on semantic model and deployment validation rather than page-level UI testing claims.

## Audience-Specific Focus

### Developer Audience

Focus on:

- reusable auth modules in `src/`
- environment-driven config
- small CLI entrypoints that can grow into internal tooling
- validation and documentation opportunities around metadata and REST APIs

### Power BI Audience

Focus on:

- semantic model design
- PBIP source control
- PBIR as a structured report artifact
- RLS implications and auth trade-offs
- why validation should happen before deployment

### Mixed Audience

Focus on:

- why trust matters more than raw build speed
- why the delegated notebook is the safest live path
- how AI lowers the barrier to build practical internal tools without overclaiming magic
