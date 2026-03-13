# Measure Validation Workflow

The measure validation template is a lightweight CSV file used as a source of truth for unit-test-like quality control of Power BI measures.

Primary template:

- `tests/measure-validation/templates/measure_validation_template.csv`

Generated supporting files:

- `tests/measure-validation/generated/measure_validation_candidates.csv`
- `tests/measure-validation/generated/report_measure_coverage.csv`

## What the template is for

The template stores validation cases for measures with enough context to support:

- manually authored scenarios
- AI-generated draft scenarios
- PBIP-aware inspection of semantic model metadata
- report-aware prioritization for measures used in important visuals
- later conversion into automated test scaffolding

The workflow intentionally separates:

- `draft` + `inferred`: machine-generated suggestions that still need review
- `active` + `human_reviewed`: reviewed scenarios that are in use
- `active` + `approved`: trusted scenarios with explicit human approval

## How developers use it

1. Run `python scripts/evaluate_pbip_for_testing.py` to inspect the current semantic model and report.
2. Run `python scripts/generate_measure_test_scenarios.py` to create fresh draft candidate rows and report coverage output.
3. Run `python scripts/generate_measure_validation_template.py` to merge draft candidates into the main template without overwriting reviewed rows.
4. Review generated rows, adjust business assumptions, and only then promote them from `draft` / `inferred` to reviewed states.

## How Codex should use it

When a prompt asks to inspect a PBIP dataset or report for testing:

- inspect the semantic model definition to discover measures, expressions, dependencies, and risky DAX patterns
- inspect the PBIR report definition to find report pages, visuals, and visible measure usage where possible
- generate meaningful draft scenarios with explicit `draft` and `inferred` markers
- preserve human-reviewed or approved rows during regeneration
- append new inferred rows instead of silently replacing trusted entries

## How PBIP evaluation feeds scenario generation

Semantic model inspection looks for:

- measures, owning tables, DAX expressions, descriptions, format strings, and display folders
- simple dependencies inferred from `'Table'[Column]` and `[Measure]` references
- risky logic patterns such as `DIVIDE`, `CALCULATE`, `ALL`, `ALLEXCEPT`, `REMOVEFILTERS`, time-intelligence functions, branching, and blank handling

Report inspection looks for:

- page names and visual names from PBIR JSON
- measure references present in visual query projections
- high-visibility usage based on executive/overview-style pages and card visuals

Scenario generation then uses that analysis to produce targeted cases such as:

- divide-by-zero checks for ratio measures
- negative-value checks for margin and variance measures
- filter-context checks for context-altering DAX
- regression and grand-total checks for report-visible measures
- formatting checks for percentage measures

## Known limitations

- TMDL parsing is intentionally lightweight and best-effort; it does not implement a full TMDL parser
- report usage detection depends on measure references being present in committed PBIR visual metadata
- generated scenarios are suggestions, not proofs; they still require human review
- expected values remain placeholders until populated from a trusted business reference
