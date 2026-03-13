# Test Results

Notebook and script-driven measure validation runs save outputs here.

Expected structure:

```text
test-results/
`-- <dataset-name>/
    `-- <run-timestamp>/
        |-- run_summary.json
        |-- selected_test_cases.csv
        |-- executed_queries.sql.txt
        |-- query_results/
        |-- screenshots/
        `-- report/
            |-- report_metadata.json
            `-- report_summary.md
```

Notes:

- `screenshots/` is created for consistency even when no screenshots are captured
- outputs are demo-friendly artifacts, not a full test platform
- review generated results before treating any scenario as approved
