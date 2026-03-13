# Presentation Outline

## Current Repo State

This presentation should be grounded in the repository exactly as it exists today.

- The repo is intentionally split into `demo-enterprise/bi-repo/`, `demo-enterprise/data-engineer-repo/`, and `demo-enterprise/shared/` to simulate enterprise team boundaries without requiring multiple repositories.
- The committed Power BI sample lives under `demo-enterprise/bi-repo/powerbi/workspaces/regional-sales-trust-demo/pbip/`.
- The semantic model currently contains 6 tables and 7 published measures:
  `Total Sales`, `Total Cost`, `Gross Margin`, `Gross Margin %`, `Total Units`, `Order Count`, and `Average Order Value`.
- The report shell currently contains 3 pages:
  `Executive Overview`, `Regional Performance`, and `API Query Validation`.
- The repo contains 4 notebooks, 10 canonical CLI scripts under `scripts/cli/`, reusable modules under `src/`, and persisted measure-validation outputs under `test-results/`.
- The repo includes both delegated-user and service-principal auth modules, but this presentation package should use service principal as the primary live path because delegated auth is not working in the presenter environment.
- Current health checks that already pass in this repo:
  `python scripts/cli/validate_tmdl_semantic_model.py`
  `.venv\Scripts\python.exe -m pytest -q`

## Strongest Current Story

The strongest story this repo can tell today is not "Power BI plus AI is cool." It is:

**Power BI becomes much more professional and reusable when PBIP/PBIR/TMDL, repo structure, validation artifacts, and lightweight internal tooling are treated as first-class engineering assets.**

This repo is especially credible because it already contains:

- inspectable Power BI artifacts in source control
- a compact but real semantic model and report shell
- lightweight testing and validation assets
- a notebook-friendly demo surface backed by reusable code
- persisted run outputs that prove the workflow has already been exercised

## Presentation Strategy

- Proposed title:
  `Trustworthy Power BI Engineering with PBIP, Validation Guardrails, and Lightweight Automation`
- Target audience:
  Power BI developers, BI engineers, analytics engineers, reporting consultants, and technical leads who care about maintainability, validation, and source control.
- Core message:
  This repo shows a practical way to move Power BI work from desktop-only craftsmanship toward a more inspectable, testable, and reusable engineering workflow.
- Demo narrative:
  Start with the repo structure and enterprise boundaries, show why PBIP/PBIR/TMDL matter, then use service principal plus a small DAX probe and a PBIP-aware validation workflow to show how trust is built before deployment.
- Why this repo is interesting to Power BI developers:
  It does not stop at "Power BI in Git." It shows how source-controlled Power BI assets can feed documentation, validation, notebooks, and lightweight internal tooling.

## Key Takeaways

- PBIP, PBIR, and TMDL matter because they turn Power BI assets into inspectable source files.
- A clean repo structure makes BI ownership, upstream dependencies, and automation boundaries easier to explain and maintain.
- Validation can start with lightweight artifacts such as CSV templates, generated scenario candidates, and persisted run outputs.
- Notebooks work best as demo and operator surfaces when the reusable logic lives in `src/` and thin CLI entrypoints.
- Service principal is useful for this session because it works in the current presenter environment, but it still depends on tenant settings, workspace membership, and dataset features.

## Slide Outline

### Slide 1. Trustworthy Power BI Engineering

- Objective:
  Open with the production-trust problem and frame the repo as the main artifact.
- Key talking points:
  Power BI teams can build fast; the harder question is whether the model and report path are trustworthy in production.
  This session is grounded in one repo, not a theoretical architecture slide.
  Scope is semantic-model and report-structure validation, not full UI regression testing.
- On-screen visual:
  Title slide with three labeled anchors: `PBIP/PBIR/TMDL`, `Validation Workflow`, `Notebook Demo Surface`.
- Slide type:
  Talking slide.
- Visual direction:
  Clean hero slide, left-aligned title, three compact callout cards on the right, light background, one blue accent.

### Slide 2. Why Traditional Power BI Development Is Not Enough

- Objective:
  Frame the engineering problem the repo addresses.
- Key talking points:
  Desktop-only changes are hard to diff and review.
  Validation is often manual, late, and undocumented.
  Auth and environment issues can derail demos and real operations.
  Teams need inspectable artifacts and reusable validation, not only faster report building.
- On-screen visual:
  Two-column comparison: `Ad hoc BI workflow` vs `Engineered BI workflow`.
- Slide type:
  Talking slide.
- Visual direction:
  Before/after comparison with red flags on the left and disciplined practices on the right.

### Slide 3. What This Repo Is Actually For

- Objective:
  Explain the purpose and boundaries of the current repo without overclaiming.
- Key talking points:
  This repo is a teaching and demo repo, not a full production platform.
  It combines a mock BI repo, a mock Data Engineering repo, and shared contracts in one place.
  The Python code, notebooks, tests, and docs support live validation and local workflow demos.
- On-screen visual:
  Four summary cards:
  `4 notebooks`
  `10 CLI scripts`
  `1 committed PBIP sample`
  `Persisted test-results`
- Slide type:
  Talking slide.
- Visual direction:
  Simple metric cards with short captions and one small note that the structure is intentionally lightweight.

### Slide 4. Repo Architecture and Ownership Boundaries

- Objective:
  Show how the folder layout supports enterprise-style ownership and maintainability.
- Key talking points:
  `bi-repo` owns Power BI assets and BI-facing conventions.
  `data-engineer-repo` represents curated upstream ownership.
  `shared` captures the handoff contract.
  `src`, `scripts`, `notebooks`, `tests`, and `docs` support repeatable engineering workflows around the Power BI assets.
- On-screen visual:
  Repo tree with highlights on `demo-enterprise/`, `src/`, `scripts/cli/`, `notebooks/`, `tests/measure-validation/`, and `docs/`.
- Slide type:
  Demo transition slide.
- Visual direction:
  Repo tree on the left, ownership callouts on the right, thin arrows from Data Engineering to BI.

### Slide 5. PBIP, PBIR, and TMDL Make Power BI Inspectable

- Objective:
  Make the source-controlled Power BI story concrete.
- Key talking points:
  `Fact Sales.tmdl` shows real measure definitions and hidden raw columns.
  `relationships.tmdl` shows the star schema plus the optional security bridge.
  `pages.json` and page metadata show that report structure is inspectable too.
  The `DataRootFolder` parameter makes local sample data explicit, even though it is currently machine-local.
- On-screen visual:
  Split view with snippets from `Fact Sales.tmdl`, `relationships.tmdl`, and report page metadata.
- Slide type:
  Talking slide.
- Visual direction:
  60/40 code layout, zoomed snippets, thin callout boxes around `Total Sales`, `Gross Margin`, `Average Order Value`, and `Executive Overview`.

### Slide 6. Live Demo Part 1: Service Principal Auth and a Small DAX Probe

- Objective:
  Show the working auth path for this environment and prove that the repo can query a dataset.
- Key talking points:
  This demo uses service principal because it is the auth path that works reliably in the presenter environment.
  The notebook is an operator surface; the reusable auth and REST logic live under `src/`.
  A small DAX probe is enough to show connectivity and dataset reachability without turning the session into query tuning.
- On-screen visual:
  Screenshot or live view of `notebooks/02_service_principal_demo.ipynb` plus a small result table.
- Slide type:
  Demo transition slide.
- Visual direction:
  Large notebook screenshot with three callouts:
  `Acquire token`
  `List workspaces and datasets`
  `Run one DAX query`

### Slide 7. Live Demo Part 2: Measure Validation from Repo Metadata

- Objective:
  Show how the repo turns Power BI artifacts into reviewable validation work.
- Key talking points:
  The semantic model and PBIR report metadata are inspected to generate measure-validation candidates and report coverage.
  The CSV template is a reviewable source file, not hidden notebook state.
  The notebook saves run artifacts under `test-results/`, which gives the presenter a fallback evidence path.
- On-screen visual:
  Three-step flow:
  `PBIP + PBIR metadata -> validation CSVs -> saved run outputs`
- Slide type:
  Demo transition slide.
- Visual direction:
  Horizontal process diagram with one small screenshot each from the template CSV, coverage CSV, and `run_summary.json`.

### Slide 8. Engineering Practices Visible in the Repo

- Objective:
  Surface the reusable engineering patterns behind the demo.
- Key talking points:
  Reusable logic sits in `src/`; notebooks and CLI scripts are thin surfaces.
  Config loading has explicit precedence and supports both auth modes.
  Validation guardrails exist both at the semantic-model level and the measure-validation level.
  Unit tests focus on config, auth behavior, metadata handling, and measure-validation generation.
- On-screen visual:
  Layered diagram:
  `Docs and conventions`
  `Notebooks and CLI`
  `src/ reusable modules`
  `PBIP assets and test-results`
- Slide type:
  Talking slide.
- Visual direction:
  Layer stack with short labels and one small note that the repo intentionally avoids a fake enterprise platform story.

### Slide 9. Enterprise Relevance and Auth Limitations

- Objective:
  Translate the repo into enterprise value while staying honest about limits.
- Key talking points:
  The repo makes ownership boundaries, reviewability, and validation visible.
  The service-principal path is useful for automation-oriented demos and internal tools.
  Limitation note:
  tenant settings, workspace membership, and dataset features such as RLS or SSO can block `executeQueries`.
  This repo is not pretending to include CI/CD, orchestration, or full production hardening.
- On-screen visual:
  Benefits checklist on the left and a caution box on the right.
- Slide type:
  Talking slide.
- Visual direction:
  Balanced two-column slide with a muted warning panel for the service-principal limitation note.

### Slide 10. What the Audience Can Reuse

- Objective:
  Close with practical reuse ideas and a clear next step.
- Key talking points:
  Start by committing PBIP/PBIR/TMDL artifacts.
  Add a lightweight validation template and persist demo or test outputs.
  Keep notebooks as guided surfaces and move reusable logic into code modules.
  Use service principal only where tenant policy and dataset features allow it.
- On-screen visual:
  Three-step adoption path:
  `Commit assets`
  `Add guardrails`
  `Build small tooling`
- Slide type:
  Talking slide.
- Visual direction:
  Minimal summary slide with a bold final callout and enough white space for a strong close.

## Repo-to-Deck Mapping

| Repo artifact | What it demonstrates | Slide | Live or mention |
|---|---|---:|---|
| `README.md` | repo purpose, layout, validation commands | 3 | Live |
| `docs/architecture/repo-architecture.md` | source-of-truth folders and execution surfaces | 4 | Live |
| `docs/external-repos/data-engineering-repo-contract.md` | enterprise ownership boundary | 4, 9 | Mention |
| `demo-enterprise/bi-repo/powerbi/workspaces/regional-sales-trust-demo/pbip/` | Power BI assets in source control | 5 | Live |
| `.../Fact Sales.tmdl` | measures, hidden raw columns, business-friendly naming | 5 | Live |
| `.../relationships.tmdl` | star schema and security bridge | 5 | Live |
| `.../demo_dataset.Report/definition/pages/pages.json` | report structure as inspectable metadata | 5 | Live |
| `notebooks/02_service_principal_demo.ipynb` | working demo auth path and DAX probe | 6 | Live |
| `src/config/loader.py` | config precedence and maintainability | 8 | Mention |
| `tests/measure-validation/templates/measure_validation_template.csv` | reviewable validation source file | 7 | Live |
| `tests/measure-validation/generated/report_measure_coverage.csv` | report-aware validation prioritization | 7 | Live |
| `test-results/demo-dataset/2026-03-14_001534/run_summary.json` | persisted evidence of executed validation | 7 | Live |
| `test-results/demo-dataset/2026-03-14_001534/report/report_summary.md` | link between API reports and local PBIP measure usage | 7 | Live |
| `tests/unit/test_measure_validation_generation.py` | lightweight automated coverage of the workflow | 8 | Mention |

## Final Recommendation

- Recommended final presentation title:
  `Trustworthy Power BI Engineering with PBIP, Validation Guardrails, and Lightweight Automation`
- One-sentence abstract:
  A practical walkthrough of a Power BI repo that uses PBIP/PBIR/TMDL, reviewable validation artifacts, and lightweight automation to make BI work easier to inspect, validate, and reuse.
- Top 3 demo moments:
  Opening the committed PBIP/TMDL assets and showing real measures in `Fact Sales.tmdl`
  Running or showing the service-principal notebook as the working auth path for this presenter environment
  Walking from generated validation CSVs into the saved `test-results` package
- Top 3 repo strengths to emphasize on stage:
  inspectable Power BI artifacts in source control
  practical validation workflow instead of vague quality claims
  clear ownership boundaries between BI, upstream data work, and supporting engineering code
- Top 3 risks or confusions to avoid:
  do not overstate service principal as universally easier than delegated auth
  do not imply the repo already includes CI/CD or full UI regression testing
  do not spend live time debugging auth when persisted run outputs already prove the workflow
