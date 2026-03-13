# Draft Slide Content

## Slide 1. Trustworthy Power BI Engineering

- Title:
  `Trustworthy Power BI Engineering with PBIP, Validation Guardrails, and Lightweight Automation`
- Subtitle:
  `A practical repo walkthrough for Power BI developers`
- On-slide points:
  `One repo`
  `Inspectable Power BI assets`
  `Validation evidence, not only claims`
- Callout:
  `Scope: semantic-model and report-structure validation, not full UI regression testing`

## Slide 2. Why Traditional Power BI Development Is Not Enough

- Title:
  `Why Traditional Power BI Development Is Not Enough`
- Left column:
  `Desktop-only changes are hard to review`
  `Validation is often manual and late`
  `Auth and environment issues derail repeatability`
- Right column:
  `Source-controlled assets`
  `Reviewable validation artifacts`
  `Reusable notebooks and tooling`
- Footer:
  `The problem is not only speed. It is trust.`

## Slide 3. What This Repo Is Actually For

- Title:
  `What This Repo Is Actually For`
- Body:
  `Presentation-friendly enterprise BI demo`
  `PBIP sample + notebooks + CLI scripts + reusable code`
  `Validation workflow with saved outputs`
- Metric strip:
  `4 notebooks`
  `10 CLI scripts`
  `1 committed PBIP sample`
  `29 passing tests in .venv`

## Slide 4. Repo Architecture and Ownership Boundaries

- Title:
  `Repo Architecture and Ownership Boundaries`
- Left side:
  repo tree snippet with
  `demo-enterprise/bi-repo`
  `demo-enterprise/data-engineer-repo`
  `demo-enterprise/shared`
  `src`
  `notebooks`
  `tests/measure-validation`
- Right side:
  `BI owns semantic model, measures, report shell`
  `Data Engineering owns curated upstream data story`
  `Shared folder explains the handoff`

## Slide 5. PBIP, PBIR, and TMDL Make Power BI Inspectable

- Title:
  `PBIP, PBIR, and TMDL Make Power BI Inspectable`
- Body:
  `Measures are readable in TMDL`
  `Relationships are visible in source control`
  `Report pages are inspectable through PBIR metadata`
- Code callouts:
  `Fact Sales[Total Sales]`
  `Fact Sales[Gross Margin]`
  `Executive Overview`
  `Security Region Access`

## Slide 6. Live Demo Part 1: Service Principal and a Small DAX Probe

- Title:
  `Live Demo Part 1: Service Principal and a Small DAX Probe`
- Body:
  `Use service principal because it works in the current presenter environment`
  `Notebook is the operator surface`
  `One small DAX query is enough to prove connectivity`
- Small note:
  `Automation-oriented identity pattern`

## Slide 7. Live Demo Part 2: Measure Validation from Repo Metadata

- Title:
  `Live Demo Part 2: Measure Validation from Repo Metadata`
- Flow:
  `PBIP + PBIR metadata`
  `Generated validation candidates and report coverage`
  `Saved run artifacts under test-results`
- Callout:
  `Validation cases are reviewable files, not hidden notebook state`

## Slide 8. Engineering Practices Visible in the Repo

- Title:
  `Engineering Practices Visible in the Repo`
- Body:
  `Reusable logic in src`
  `Thin CLI entrypoints and notebooks`
  `Config precedence and auth abstraction`
  `Semantic-model and validation guardrails`
  `Focused unit tests`
- Footer:
  `Small repo, but strong engineering signals`

## Slide 9. Enterprise Relevance and Auth Limitations

- Title:
  `Enterprise Relevance and Auth Limitations`
- Left side:
  `Clear ownership boundaries`
  `Reviewable Power BI artifacts`
  `Validation before deployment`
- Right-side caution box:
  `Service principal limitation`
  `Tenant settings, workspace membership, and dataset features such as RLS or SSO can block executeQueries`
- Footer:
  `Useful for enterprise workflows, but honest about environment constraints`

## Slide 10. What the Audience Can Reuse

- Title:
  `What the Audience Can Reuse`
- Three steps:
  `Commit PBIP, PBIR, and TMDL assets`
  `Add lightweight validation artifacts`
  `Keep notebooks thin and reusable logic in code`
- Closing line:
  `Power BI becomes easier to trust when the assets, workflow, and evidence are all inspectable`
