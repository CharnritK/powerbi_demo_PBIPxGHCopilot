# Presenter Demo Script

## Short script

### Opening

"Today I'm showing a practical Power BI REST API demo package that compares delegated user access with service principal automation. The goal is not just to call the API, but to make the implementation easy to teach, easy to demo, and easy to reuse."

### Repo overview

"This repository is intentionally notebook-first. That gives non-developers a friendly entry point, while the reusable Python modules and helper scripts still support technical teams."

### Notebook demo

"I'll start with delegated auth because it is the safest live-demo path. Then I'll optionally show the service principal notebook to explain the automation story and the admin dependencies."

### PBIP/model section

"The sample model is a compact regional sales star schema. It is small enough to understand quickly, but realistic enough for report pages, DAX query examples, and an RLS discussion."

### Limitations section

"There are a few important caveats to say clearly. `executeQueries` is DAX only. Service principal is not the right choice for `executeQueries` on datasets with RLS or SSO. So for a smooth demo, I keep the main model free of active RLS and start with delegated auth."

## Speaking points

- Delegated notebook is the primary live path.
- Service principal is a comparison path, not the default.
- `src/` holds the reusable engine.
- Same business story, different identity contexts.
- The main demo is optimized for clarity, not edge-case coverage.

## What-to-click-next checklist

1. Open `README.md`.
2. Show the folder tree.
3. Open `notebooks/01_delegated_auth_demo.ipynb`.
4. Acquire a delegated token.
5. Run workspace listing.
6. Run dataset and report listing.
7. Run the DAX query.
8. Show the result table.
9. Open `notebooks/02_service_principal_demo.ipynb` only if you want to cover automation caveats.
10. Open the PBIP sample design doc.
11. Close on auth comparison and limitations.

## Possible audience Q&A

### Q1. Why not use only service principal?

Because service principal is excellent for unattended automation, but it is not a full replacement for user-context scenarios. It is also explicitly limited for `executeQueries` against RLS-enabled datasets.

### Q2. Why is the notebook the main entry point?

Because mixed audiences follow a notebook more easily than a script-only demo. It reduces friction without hiding the real implementation.

### Q3. Does delegated auth better represent end-user access?

Yes. It is the better fit when execution should reflect the signed-in user's permissions and experience.

### Q4. Why not enable RLS in the main sample?

Because the goal of the main demo is to compare auth patterns with minimal failure risk. RLS is better shown as an advanced branch or second scenario.

### Q5. Is this repo production-ready?

It is production-style and reusable, but still a demo asset. Production solutions would usually add secret management, stronger testing, CI/CD, and tenant-specific controls.

## Caveats to say out loud

- "This is a teaching-focused sample, not a complete enterprise platform."
- "Tenant settings and permissions vary by environment."
- "PBIP is a strong source-control direction, but you should validate current feature status in your tenant and Desktop version."
- "The cleanest demo path starts with delegated auth and avoids active RLS in the main dataset."
