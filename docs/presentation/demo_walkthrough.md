# Demo Walkthrough

## Demo Goal

Show the audience that this repo is not just a folder of Power BI files. It is a small but credible engineering workflow built around:

- source-controlled Power BI artifacts
- lightweight automation and notebooks
- reviewable validation assets
- persisted evidence under `test-results/`

## Demo Rules for This Session

- Use service principal as the only primary live auth path.
- Mention delegated auth only once:
  it exists in the repo, but it is not working in the current presenter environment.
- Do not turn the session into auth troubleshooting.
- Treat Power BI Desktop as optional.
  Only open the PBIP in Desktop if it is already pre-opened and stable.
- Do not use `generate_measure_docs.py` in the live flow.
  The current extractor does not pull `///` comments into descriptions yet.

## Exact Open Order

### 1. Open `README.md`

- Why first:
  It anchors the session in the repo's actual purpose and layout.
- What to say:
  "This repo is a presentation-friendly enterprise demo. It keeps BI ownership, upstream data ownership, notebooks, scripts, and Power BI assets in one place so the workflow is easy to explain."
- Where to zoom:
  `demo-enterprise/`, `notebooks/`, `scripts/`, `src/`, `tests/`, `docs/`
- Keep it understandable:
  Stay at the level of purpose, not implementation detail.
- Fallback:
  None needed.

### 2. Show the top-level repo tree

- Why second:
  The audience should see the shape before the details.
- What to say:
  "This is not only a notebook demo. The notebooks are the presenter surface. The engineering work sits underneath in source code, tests, docs, and Power BI project files."
- Where to zoom:
  `demo-enterprise/`
  `src/`
  `scripts/cli/`
  `notebooks/`
  `tests/measure-validation/`
- Keep it understandable:
  Highlight only the folders that matter to the talk.
- Fallback:
  If the IDE tree is cluttered, use the tree screenshot prepared for the deck.

### 3. Open `docs/architecture/repo-architecture.md`

- Why third:
  It explains source-of-truth folders and execution surfaces in one screen.
- What to say:
  "The repo is explicit about what is authoritative, what is runnable, and what is reference-only. That is a maintainability signal, not just a documentation choice."
- Where to zoom:
  `src/`
  `demo-enterprise/.../pbip/`
  `scripts/cli/`
  `notebooks/`
- Keep it understandable:
  Do not read the whole page. Use it as a framing slide.
- Fallback:
  Summarize verbally if the page is already familiar from the deck.

### 4. Open `demo-enterprise/bi-repo/powerbi/workspaces/regional-sales-trust-demo/pbip/`

- Why fourth:
  This is where the Power BI story becomes concrete.
- What to say:
  "This is the main Power BI artifact area. The project, semantic model, and report shell are committed, diffable files."
- Where to zoom:
  `demo_dataset.pbip`
  `demo_dataset.SemanticModel`
  `demo_dataset.Report`
- Keep it understandable:
  Avoid opening too many files at once.
- Fallback:
  Use the repo-to-deck screenshot if the tree is slow or collapsed.

### 5. Open `Fact Sales.tmdl`

- Why fifth:
  It is the clearest example of inspectable measures plus hidden raw columns.
- What to say:
  "This file shows the exact pattern many teams want but do not always achieve consistently: hidden raw columns, business-facing measures, and readable DAX that a reviewer can inspect in Git."
- Where to zoom:
  `Total Sales`
  `Gross Margin`
  `Gross Margin %`
  `Average Order Value`
  hidden raw columns such as `Sales Amount` and `Cost Amount`
- Keep it understandable:
  Stop at 2 or 3 measures. Do not scroll through the entire table.
- Fallback:
  Use a pre-cropped screenshot on the slide if font size becomes unreadable.

### 6. Open `relationships.tmdl`

- Why sixth:
  It confirms this is a real star-schema-style model, not a placeholder repo.
- What to say:
  "The model is small, but it has the core structure a Power BI developer expects: fact-to-dimension relationships plus an optional security bridge."
- Where to zoom:
  the `Fact Sales` relationships to `Dim Date`, `Dim Region`, `Dim Product`, and `Dim Channel`
  the `Security Region Access` relationship to `Dim Region`
- Keep it understandable:
  Call it a compact demo model, not an enterprise-scale model.
- Fallback:
  If scrolling is awkward, summarize the relationship set verbally.

### 7. Open report page metadata: `pages.json`, then `Executive Overview`

- Why seventh:
  It shows that report structure is inspectable too, not only the semantic model.
- What to say:
  "PBIR matters because report structure becomes readable enough for tooling to inspect. That is how the validation workflow later connects measures to pages and visuals."
- Where to zoom:
  the three page names in `pages.json`
  `Executive Overview` in `page.json`
- Keep it understandable:
  Do not dive into raw `visual.json` unless someone asks.
- Fallback:
  Use the saved `report_summary.md` later as the practical proof of report-aware metadata.

### 8. Open `notebooks/02_service_principal_demo.ipynb`

- Why eighth:
  This is the primary live auth path for the current presenter environment.
- What to say:
  "I am using service principal here because it is the path that works reliably in my environment today. It also fits the automation story of the repo."
- Where to zoom:
  `Load config`
  `Acquire a service principal token`
  `List workspaces`
  `Optional DAX query`
- Keep it understandable:
  If you run cells, only run enough to show token acquisition, workspace visibility, dataset visibility, and one small query result.
- Fallback:
  If auth fails, stop immediately and switch to the saved validation outputs.

### 9. Open `notebooks/03_measure_validation_showcase.ipynb`

- Why ninth:
  This notebook connects the Power BI assets to validation artifacts and saved results.
- What to say:
  "This is the most reusable part of the story. The repo inspects the semantic model and report metadata, selects validation cases, executes them, and saves a result package."
- Where to zoom:
  `Configure the Demo`
  `Discover Workspaces and Datasets`
  `Load the Measure Validation Template`
  `Execute Selected Test Cases`
  `Save a Demo-Friendly Result Package`
- Keep it understandable:
  Do not run the whole notebook if time is tight.
  Use it to explain the workflow, then pivot to committed outputs.
- Fallback:
  Use the saved outputs in the next steps as the primary evidence.

### 10. Open `tests/measure-validation/templates/measure_validation_template.csv`

- Why tenth:
  It proves the validation source file is reviewable and not hidden in notebook state.
- What to say:
  "This is a lightweight but credible pattern. The validation cases are stored as a CSV that BI developers can review, update, and preserve over time."
- Where to zoom:
  `status`
  `review_status`
  `measure_name`
  `scenario_type`
  `page_name`
  `visual_name`
- Keep it understandable:
  Show only a few rows and explain the `draft` plus `inferred` pattern.
- Fallback:
  If the file view is cramped, show the example template instead.

### 11. Open `tests/measure-validation/generated/report_measure_coverage.csv`

- Why eleventh:
  It shows how PBIR metadata influences validation prioritization.
- What to say:
  "The useful detail here is not the CSV itself. It is that the repo can tell which measures are used in visible report visuals and raise their validation priority."
- Where to zoom:
  `page_name`
  `visual_name`
  `measure_name`
  `is_high_visibility`
  `priority_hint`
- Keep it understandable:
  Tie the rows back to `Executive Overview`.
- Fallback:
  If needed, skip directly to `report_summary.md` in the saved run.

### 12. Open `test-results/demo-dataset/2026-03-14_001534/run_summary.json`

- Why twelfth:
  This is the best fallback evidence for the live demo.
- What to say:
  "Even if I do not run everything live, this repo already contains a saved result package from a real run. That matters because the workflow leaves behind evidence."
- Where to zoom:
  `selected_case_count`
  `executed_case_count`
  `execution_outcomes`
- Keep it understandable:
  Focus on the structure and the fact that the result is persisted.
- Fallback:
  None needed. This is already the fallback path.

### 13. Open `test-results/demo-dataset/2026-03-14_001534/report/report_summary.md`

- Why last:
  It closes the loop between workspace metadata and local PBIP measure usage.
- What to say:
  "This is the final proof point: the repo links API-visible report metadata with local PBIP report structure and selected measures."
- Where to zoom:
  `Workspace Reports`
  `Local PBIP Measure Usage`
- Keep it understandable:
  End here. This is a clean closing artifact.
- Fallback:
  None needed.

## What Each Surface Should Demonstrate

- PBIP and TMDL files:
  show inspectable Power BI assets, relationships, measures, and report structure.
- Notebooks:
  show the operator-friendly workflow and the working service-principal demo path.
- Generated CSVs:
  show that validation is reviewable and tied to report usage.
- Saved `test-results` artifacts:
  show durable proof without relying on a perfect live run.
- Scripts and `src/`:
  mention them as the reusable layer underneath the notebooks, but do not live-code them in a 10 to 15 minute slot.

## How To Keep the Demo Understandable

- Open one file at a time.
- Stay at the behavior level, not the implementation-detail level.
- Use the semantic model to explain Power BI engineering, not to teach TMDL syntax.
- Use the notebooks to explain workflow, not to perform every step live.
- Use the saved outputs as evidence, not as an apology for not running everything.

## Fallback Plan

If any live auth or notebook step fails:

1. Stop immediately.
2. Say:
   "The live environment is the fragile part, not the repo structure. I will switch to the saved run package so we stay on the engineering story."
3. Open:
   `test-results/demo-dataset/2026-03-14_001534/run_summary.json`
4. Then open:
   `test-results/demo-dataset/2026-03-14_001534/report/report_summary.md`
5. Finish by pointing back to:
   `tests/measure-validation/templates/measure_validation_template.csv`
   and
   `tests/measure-validation/generated/report_measure_coverage.csv`

## Short Auth Note for the Presenter

Use this wording once and move on:

> "For this session I am using service principal because it is the auth path that works reliably in my presenter environment. It is also the better fit for the automation part of the story. The short limitation note is that tenant settings, workspace membership, and dataset features such as RLS or SSO can still block `executeQueries`."
