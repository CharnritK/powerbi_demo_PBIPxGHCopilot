# Architecture and Flow Content

## High-Level Engineering Narrative

Git-tracked PBIP/PBIR/TMDL artifacts
-> AI-assisted inspection of report and model metadata
-> lightweight validation or documentation scripts
-> delegated or service principal authentication
-> Power BI REST API and semantic model
-> evidence returned to notebook or CLI
-> higher confidence before deployment

## Demo-Sized Architecture

- Source-controlled artifacts: `pbip/demo_dataset.pbip`, `demo_dataset.Report/`, and `demo_dataset.SemanticModel/definition`
- Presenter surfaces: `README.md`, notebook demos, and speaker docs
- Reusable tooling layer: `src/` and compatibility `scripts/`
- Validation and analysis tasks: inspect report structure, draft realistic validation scenarios, validate schema and measures, improve documentation, and run small metadata or DAX checks
- Service boundary: Power BI REST API plus the target semantic model
- Trusted-tool context: DAX Studio, ALM Toolkit, and Tabular Editor remain valuable; the repo shows where AI-assisted tooling can sit beside them

## Delegated User Request Flow

1. Notebook or script loads tenant and client ID.
2. User signs in through device code or interactive browser flow.
3. MSAL public client acquires a delegated access token.
4. Power BI evaluates the signed-in user's workspace and dataset permissions.
5. The demo calls metadata endpoints and optionally `executeQueries`.
6. Results reflect real user context, which makes this the safest live-demo baseline.

## Service Principal Request Flow

1. Notebook or script loads tenant, client ID, and client secret.
2. MSAL confidential client acquires an app-only token.
3. Power BI validates tenant settings, allowed groups, and workspace membership.
4. The demo calls the same metadata endpoints where supported.
5. `executeQueries` is only attempted when the dataset does not hit unsupported RLS or SSO identity limitations.
6. This path is best framed as the automation comparison, not the default demo path.

## Why PBIR Matters in This Story

- PBIR stores report structure in files that tools can inspect.
- That makes it practical to inspect report structure and draft realistic validation scenarios from report metadata.
- PBIR helps reviewers and tooling see what visuals, pages, and fields are in scope.
- PBIR does not turn this repo into a full UI regression platform, and the docs should not claim that.

## AI-Assisted Tooling Loop

1. Inspect PBIR and TMDL artifacts from source control.
2. Propose realistic validation scenarios from report and model metadata.
3. Draft documentation, risk notes, or small validation scripts.
4. Run targeted REST API calls or semantic model checks.
5. Produce evidence that a reviewer can understand before deployment.

## Diagram Text Blocks for Slides

### Diagram 1 - Trust Pipeline

Git-tracked PBIP/PBIR/TMDL
-> AI-assisted inspection
-> validation scripts
-> REST API / semantic model
-> evidence for review

### Diagram 2 - Delegated Live Path

Presenter
-> delegated notebook
-> MSAL public client
-> user token
-> Power BI REST API
-> workspace + dataset
-> results in notebook

### Diagram 3 - Automation Comparison Path

Notebook or script
-> MSAL confidential client
-> app token
-> Power BI REST API
-> workspace access for service principal
-> metadata calls
-> optional query checks on supported datasets

### Diagram 4 - Metadata to Guardrail Flow

PBIR report structure + TMDL semantic model
-> inspect metadata
-> draft validation scenarios
-> run schema and measure checks
-> produce deployment evidence
