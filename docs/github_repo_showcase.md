# GitHub Repo Showcase Walkthrough

## What the repo looks like
The repo should feel like a realistic consulting accelerator:
- business-friendly notebook at the front
- reusable Python scripts underneath
- small sample data for explainability
- PBIP design guidance for the Power BI audience
- presenter notes and architecture writeups for enablement

## Which files matter during the demo

### For the presenter
- `README.md`
- `notebooks/powerbi_rest_api_demo.ipynb`
- `docs/pbip_sample_design.md`
- `docs/architecture_flows.md`

### For developers
- `scripts/*.py`
- `config/.env.example`
- `requirements.txt`

### For Power BI developers
- `docs/pbip_sample_design.md`
- `data/*.csv`
- `pbip/README.md`

## Suggested walk-through order
1. Start at `README.md`
2. Show the repo tree
3. Open the notebook
4. Run workspace and dataset listing
5. Run a DAX query
6. Open the PBIP design doc
7. Close with architecture and auth trade-offs

## Audience-specific focus

### Business audience
Focus on:
- what problem this solves
- why notebook-first is easier to trust
- what is and is not supported
- why auth choice matters for governance

### Developer audience
Focus on:
- reusable auth modules
- environment-driven config
- clear API boundaries
- graceful error handling
- easy extension path

### Power BI audience
Focus on:
- semantic model design
- PBIP source-control story
- DAX query mapping
- RLS implications
- workspace and dataset permissions
