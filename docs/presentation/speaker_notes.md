# Speaker Notes

## Slide 1. Trustworthy Power BI Engineering

Power BI teams already know how to build reports. The harder question is whether we can trust the workflow in production. This talk uses one repo to show a more engineering-oriented way to work with Power BI. The focus is not AI novelty. The focus is inspectable assets, validation, and reuse.

Transition:
If trust is the goal, then the usual desktop-only workflow is not enough.

## Slide 2. Why Traditional Power BI Development Is Not Enough

Traditional Power BI work often breaks down when more people, more environments, and more change are involved. Changes are hard to diff. Validation is manual. Problems appear late. The point of this repo is to show a small but practical alternative: treat Power BI assets and validation work as source-controlled engineering artifacts.

Transition:
So the next question is what this repo actually contains, and what it does not pretend to contain.

## Slide 3. What This Repo Is Actually For

This repo is intentionally a teaching and demo repo. It is not pretending to be a full platform. But it is also not a toy folder of screenshots. It contains a committed PBIP sample, reusable Python modules, notebooks, tests, validation assets, and saved outputs. That makes it a good session artifact because the audience can see both the developer workflow and the Power BI assets in one place.

Transition:
The layout matters because a lot of the enterprise story is really about ownership boundaries and maintainability.

## Slide 4. Repo Architecture and Ownership Boundaries

The repo simulates a realistic split between BI ownership and upstream data ownership. The BI side owns the Power BI project, semantic model, measures, and BI-facing docs. The mock Data Engineering side represents curated upstream ownership. Then the shared contract explains the handoff. Around that, `src`, `scripts`, `notebooks`, `tests`, and `docs` support a repeatable workflow.

Transition:
Once the layout is clear, the key thing to show is that the Power BI assets themselves are inspectable.

## Slide 5. PBIP, PBIR, and TMDL Make Power BI Inspectable

This is where the story becomes concrete. `Fact Sales.tmdl` shows the measures directly in source control. `relationships.tmdl` shows the model structure. The report metadata shows named pages and inspectable structure on the report side. That is what makes Git review, tooling, and validation realistic. It is no longer only a binary desktop artifact.

Transition:
Now that the Power BI assets are visible, I can show the working live path for this environment.

## Slide 6. Live Demo Part 1: Service Principal Auth and a Small DAX Probe

For this session I am using service principal because it is the auth path that works reliably in my current presenter environment. It also fits the automation part of the story. The notebook is only the operator surface. The reusable logic sits underneath in the repo code. I only need a small DAX query here. The goal is to prove the repo can connect, list assets, and probe the dataset without spending time on auth troubleshooting.

Transition:
Connectivity is only the first step. The more interesting question is what the repo does with that access.

## Slide 7. Live Demo Part 2: Measure Validation from Repo Metadata

This is the part I want the audience to remember. The repo inspects the semantic model and the report metadata, generates reviewable validation candidates, and saves a result package. That means validation is not hidden in notebook state or in somebody's memory. It becomes a source-controlled workflow with evidence under `test-results`.

Transition:
Underneath that demo surface, there are a few engineering patterns worth calling out because they are reusable outside this repo.

## Slide 8. Engineering Practices Visible in the Repo

The notebooks are intentionally thin. The reusable logic lives in `src`. The CLI scripts are small entrypoints. Config precedence is explicit. There are validation guardrails both for the semantic model and for the measure-validation workflow. And the unit tests focus on the behaviors that matter for this repo. None of this is flashy, but it is exactly the kind of structure that makes BI work easier to maintain.

Transition:
That is also why this repo is relevant to enterprise teams, even though it stays intentionally lightweight.

## Slide 9. Enterprise Relevance and Auth Limitations

The enterprise value here is not scale for its own sake. It is clarity. You can see ownership boundaries. You can review Power BI artifacts. You can add validation before deployment. For this talk, service principal is the practical live path, but it comes with one short limitation note: tenant settings, workspace membership, and dataset features such as RLS or SSO can block `executeQueries`. So the repo is useful, but it is honest about where environment policy still matters.

Transition:
The best close is to turn that into a short list of things the audience can actually reuse.

## Slide 10. What the Audience Can Reuse

If I had to reduce this repo to a few reusable ideas, they would be these. Commit PBIP, PBIR, and TMDL assets. Add lightweight validation artifacts that humans can review. Keep notebooks as guided surfaces and move reusable logic into code. And when you use service principal, treat it as an environment-dependent automation path, not as magic. That is enough to make Power BI work feel more like engineering and less like hidden desktop state.

Closing line:
Power BI becomes easier to trust when the assets, the workflow, and the validation evidence all live in places the team can inspect.
