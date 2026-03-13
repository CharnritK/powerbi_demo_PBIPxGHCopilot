# Repo Presentation Gap Analysis

## Current Repo State

The repo is already strong enough for a practical 10 to 15 minute conference presentation.

- Power BI assets are committed under `demo-enterprise/bi-repo/powerbi/workspaces/regional-sales-trust-demo/pbip/`.
- The semantic model contains 6 tables and 7 published measures.
- The report shell contains 3 pages, with the strongest visible content on `Executive Overview`.
- The repo includes 4 notebooks, 10 canonical CLI scripts, reusable modules under `src/`, and measure-validation templates plus generated CSVs under `tests/measure-validation/`.
- A saved measure-validation run already exists under `test-results/demo-dataset/2026-03-14_001534/`.
- The semantic-model validator passes, and the unit test suite passes in `.venv`.

## Strongest Story

The strongest story is that this repo turns Power BI work into an inspectable engineering workflow.

The best sequence is:

1. show source-controlled PBIP, PBIR, and TMDL artifacts
2. show a working service-principal notebook path for this presenter environment
3. show validation artifacts and persisted outputs that prove the workflow leaves evidence

That story is practical, credible, and easy for Power BI developers to reuse.

## Gaps and Minimal Additions

| Gap | Why it matters for the presentation | Minimal addition recommended | Priority |
|---|---|---|---|
| Presentation assets are fragmented across English docs, Thai docs, and an older `.pptx` | It is harder to tell which material is current and which material is legacy | Use the new English presentation package as the single current entry point and label older assets as legacy/reference only | Must-have |
| `expressions.tmdl` stores `DataRootFolder` as a machine-local absolute path | A live refresh or Desktop open can fail on another machine even when the repo is otherwise healthy | Add a visible presenter note in the setup and demo package; do not rely on Power BI Desktop refresh during the talk unless pre-checked | Must-have |
| Service-principal demo depends on tenant settings, workspace membership, and dataset features | The auth path can still fail even if the repo code is fine | Keep a short limitation note on one slide, validate the presenter app before the talk, and keep `test-results` ready as fallback evidence | Must-have |
| The report shell is minimal, and only the first page is visually populated enough for a clean story | If the speaker browses too deep into the report files, the repo can feel more skeletal than it actually is | Keep the live report discussion focused on `Executive Overview` and the report metadata, not on every page | Nice-to-have |
| `generate_measure_docs.py` currently produces blank descriptions because the extractor does not read `///` comments | It weakens the documentation-generation story if shown live | Do not use measure-doc generation in the presentation until the extractor is updated to read the existing comment style | Nice-to-have |
| There are no committed offline screenshots for notebook and auth steps | Live demo fragility is higher than necessary | Capture 3 to 4 backup screenshots outside source control before the session | Nice-to-have |
| The repo intentionally does not include CI/CD or deployment orchestration | Some audiences may assume the repo is missing a "final step" | State clearly that the repo is about inspectability and validation readiness, not a full delivery platform | Nice-to-have |

## Recommendation

No large rebuild is needed.

The repo is already presentation-ready if the talk stays focused on:

- source-controlled Power BI artifacts
- service principal as the practical live auth path for this environment
- PBIP-aware validation workflow
- persisted run outputs as evidence

## Do Not Add Before the Talk

- Do not add a fake CI/CD layer just to make the deck look more enterprise.
- Do not expand the report shell unless there is a very targeted reason.
- Do not rewrite auth guidance across the whole repo.
  The presentation package can override the live-demo preference without changing the repo's broader historical documentation.
