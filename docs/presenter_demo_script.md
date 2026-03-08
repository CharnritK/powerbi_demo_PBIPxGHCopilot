# Presenter Demo Script

## Short demo script

### Opening
"Today I’m showing a practical Power BI REST API demo package that compares service principal and delegated user authentication. The goal is not just to call the API, but to make the implementation easy to teach, easy to demo, and easy to reuse."

### Repo overview
"This repository is intentionally notebook-first. That gives non-developers a friendly entry point, while the reusable scripts still support technical teams."

### Notebook demo
"I’ll run the same notebook flow twice. First with service principal, which is app-only automation. Then with delegated user auth, which runs in user context. The key idea is that the interface stays simple while the authentication behavior changes underneath."

### PBIP/model section
"The sample model is a compact regional sales star schema. It is small enough to understand quickly, but realistic enough for report pages, DAX query examples, and an RLS discussion."

### Limitations section
"There are a few important caveats to say clearly. `executeQueries` is DAX only. Service principal is not the right choice for `executeQueries` on datasets with RLS or SSO. So for a smooth dual-auth demo, I keep the main model free of active RLS."

## Speaking points
- Notebook is the primary experience
- Scripts are the reusable engine
- Same business story, different auth contexts
- Main demo optimized for clarity, not edge-case coverage
- Advanced path can add RLS and deeper governance controls

## What-to-click-next checklist
1. Open `README.md`
2. Show folder tree
3. Open notebook
4. Show auth mode variable
5. Run workspace listing
6. Run dataset listing
7. Run DAX query
8. Show DataFrame result
9. Show optional chart
10. Open PBIP sample design doc
11. Close on auth comparison and limitations

## Possible audience Q&A

### Q1. Why not use only service principal?
Because service principal is excellent for unattended automation, but it is not a full replacement for user-context scenarios. It is also explicitly limited for `executeQueries` against RLS-enabled datasets.

### Q2. Why is the notebook the main entry point?
Because mixed audiences follow a notebook more easily than a script-only demo. It reduces friction without hiding the real implementation.

### Q3. Does delegated auth better represent end-user access?
Yes. It is the better fit when the execution should reflect the signed-in user's permissions and experience.

### Q4. Why not enable RLS in the main sample?
Because the goal of the main demo is to compare auth patterns with minimal failure risk. RLS is better shown as an advanced branch or second scenario.

### Q5. Is this repo production-ready?
It is production-style and reusable, but still a demo asset. Production solutions would usually add secret management, stronger testing, CI/CD, and tenant-specific controls.

## Caveats to say out loud
- "This is a teaching-focused sample, not a complete enterprise platform."
- "Tenant settings and permissions vary by environment."
- "PBIP is a strong source-control direction, but you should validate current feature status in your tenant and Desktop version."
- "The cleanest dual-auth demo path avoids active RLS in the main dataset."
