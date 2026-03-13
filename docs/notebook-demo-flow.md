# Notebook Demo Flow

The measure validation showcase notebook lives at:

- `notebooks/03_measure_validation_showcase.ipynb`

## What it demonstrates

The notebook walks through a simple, presentation-friendly flow:

1. authenticate using the repo's existing Power BI auth configuration
2. list visible workspaces
3. choose a workspace and dataset
4. locate the measure validation template or generated candidate file
5. filter and select test cases
6. show the DAX query used for each selected case
7. execute the query and preview returned rows
8. summarize report context for the selected measures
9. save run artifacts under `test-results/`

## Inputs it expects

- valid local repo configuration for Power BI auth
- a workspace visible to the current identity
- a dataset in that workspace
- a measure validation template or generated candidate CSV when available

The notebook uses editable variables near the top of the flow instead of requiring widgets.

## Saved outputs

Each run writes a timestamped folder under:

- `test-results/<dataset-slug>/<timestamp>/`

Artifacts include:

- `run_summary.json`
- `selected_test_cases.csv`
- `executed_queries.sql.txt`
- `query_results/*.csv`
- `report/report_metadata.json`
- `report/report_summary.md`

## How to run

Typical local flow:

```powershell
pip install -r requirements.txt
python -m notebook notebooks/03_measure_validation_showcase.ipynb
```

Then run the notebook top-to-bottom and adjust the selection variables if you want a narrower demo.

## Known limitations

- the notebook is intentionally linear and does not provide a full UI
- filter context in the CSV is treated as descriptive text unless explicitly written as raw DAX with a `DAX:` prefix
- query execution still depends on real Power BI access and dataset permissions
- pass/fail is lightweight; many scenarios remain `needs_review` until a human defines trusted expected values
