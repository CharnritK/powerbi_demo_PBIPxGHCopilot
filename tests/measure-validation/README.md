# Measure Validation

This folder holds a lightweight, CSV-first workflow for unit-test-like validation of Power BI measures.

Files:

- `templates/measure_validation_template.csv`: primary template file that developers and Codex update
- `templates/measure_validation_template.example.csv`: minimal example row showing intended usage
- `generated/measure_validation_candidates.csv`: generated draft scenarios inferred from PBIP artifacts
- `generated/report_measure_coverage.csv`: report usage coverage extracted from PBIR metadata
- `fixtures/sample_validation_cases.csv`: sample rows used by unit tests

Rules:

- generated rows must stay `draft` and `inferred` until a human reviews them
- approved or human-reviewed rows are preserved during merge/update
- report-aware scenarios should be prioritized above low-risk unused measures
