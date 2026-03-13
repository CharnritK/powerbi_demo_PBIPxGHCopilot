# Presenter Demo Script

## Short Script

### Opening

"In enterprise BI, the hardest question is not 'Can we build it?' We already can. The real question is 'Can we trust it in production?'

Today I want to show how Power BI is evolving into a more engineering-driven discipline, using PBIP, PBIR, GitHub Copilot, and validation practices to build BI that teams can actually trust.

What makes this exciting is that AI does not just help us build reports faster. It also helps developers build their own tools. It lowers the barrier to build practical automations around REST APIs, validation checks, documentation, and scenario drafting."

### Repo Overview

"This repository is intentionally notebook-first because that keeps the live path easy to follow. But it is not only a notebook demo. The notebooks are the presenter surface, while `src/`, `scripts/`, and the PBIP sample show the engineering artifacts underneath."

### Why Trust Matters

"AI can make BI faster, but speed is no longer the hardest question. In enterprise delivery, the harder question is whether the model, report, and deployment path are trustworthy enough for production."

### Notebook Demo

"I start with delegated auth because it is the safest live-demo path and the closest fit to real user-context access. That gives me a predictable demo and a credible baseline for validation."

### Service Principal Comparison

"I only show service principal after the delegated flow is already working. It is useful for automation-oriented scenarios, but it is not the default path, and its tenant and dataset limitations are part of the lesson."

### PBIP and Model Section

"The PBIP sample is where the engineering story becomes concrete. PBIP, PBIR, and TMDL give us structured artifacts that Git, reviewers, and tools can inspect. That is what makes source control, validation checks, and AI-assisted tooling practical instead of theoretical."

### AI-Assisted Toolbox Section

"I am not replacing tools like DAX Studio, ALM Toolkit, or Tabular Editor. I am showing how AI-assisted development extends that toolbox by making it easier for BI developers to build small internal tools around metadata inspection, documentation, validation, and REST APIs."

### Limitations Section

"This session focuses on semantic model and deployment validation. It does not claim full report-page UI regression testing. AI can inspect report structure and help draft realistic validation scenarios, but it does not replace business intent, approval processes, or reviewer judgment."

## Speaking Points

- Trust in production matters more than raw build speed.
- Delegated auth is the primary live-demo path.
- Service principal is a comparison path, not the default.
- PBIR matters because it gives tools a structured report artifact to inspect.
- Validation guardrails belong before deployment, not after a complaint.
- AI extends the toolbox; it does not replace existing trusted tools or human ownership.

## What-to-Click-Next Checklist

1. Open `docs/presentation/session_messaging.md`.
2. Open `README.md`.
3. Show the folder tree.
4. Open `notebooks/01_delegated_auth_demo.ipynb`.
5. Acquire a delegated token.
6. Run workspace listing.
7. Run dataset and report listing.
8. Run the DAX query.
9. Explain why that small query is a useful validation probe, not the whole testing story.
10. Open `notebooks/02_service_principal_demo.ipynb` only if you want to cover automation caveats.
11. Open `docs/data-model/semantic-model-overview.md`.
12. Open `docs/architecture/integration-map.md`.
13. Close on validation guardrails and AI-assisted custom tooling.

## Possible Audience Q&A

### Q1. Why not use only service principal?

Because service principal is useful for unattended automation, but it is not a full replacement for user-context scenarios. It is also explicitly limited for `executeQueries` against some RLS-enabled or SSO-enabled datasets.

### Q2. Why is delegated auth the default path?

Because it is the least fragile live-demo option, it maps cleanly to real user permissions, and it makes troubleshooting more honest.

### Q3. Why does PBIR matter in this session?

Because report structure becomes inspectable. That gives AI-assisted tooling and internal scripts something structured to analyze when drafting realistic validation scenarios.

### Q4. Are you replacing DAX Studio, ALM Toolkit, or Tabular Editor?

No. Those tools remain valuable. The point is that AI-assisted development makes it easier for BI teams to add their own lightweight internal tooling alongside them.

### Q5. Is this repo doing full UI regression testing?

No. The focus is semantic model and deployment validation, plus report-structure-aware scenario drafting. It is not pixel-level report-page regression testing.

### Q6. Is this repo production-ready?

It is production-style and reusable, but still a demo asset. Production solutions would normally add secret management, stronger automated tests, CI/CD enforcement, and tenant-specific operational controls.

## Caveats to Say Out Loud

- "This is a teaching-focused sample, not a fake enterprise platform."
- "The session focuses on semantic model and deployment validation, not report-page UI regression testing."
- "AI-assisted tooling can inspect structure and draft scenarios, but it does not understand business intent on its own."
- "Tenant settings and permissions vary by environment."
- "The cleanest live-demo path starts with delegated auth and avoids active RLS in the main dataset."
