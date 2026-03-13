from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from src.common.paths import default_report_definition_path
from src.powerbi.datasets import list_datasets
from src.powerbi.execute_queries import execute_dax_query
from src.powerbi.reports import list_reports
from src.powerbi.workspaces import list_workspaces
from src.validation.measure_validation_template import read_validation_template
from src.validation.pbip_report_inspector import inspect_report_definition
@dataclass(frozen=True)
class TemplateSelection:
    path: Path | None
    source: str
    note: str


def get_workspaces_frame(client) -> pd.DataFrame:
    return pd.DataFrame(list_workspaces(client))


def get_datasets_frame(client, workspace_id: str) -> pd.DataFrame:
    return pd.DataFrame(list_datasets(client, workspace_id))


def get_reports_frame(client, workspace_id: str) -> pd.DataFrame:
    return pd.DataFrame(list_reports(client, workspace_id))


def pick_row(frame: pd.DataFrame, preferred_name: str = "", index: int = 0, name_column: str = "name") -> dict[str, Any] | None:
    if frame.empty:
        return None
    if preferred_name and name_column in frame.columns:
        mask = frame[name_column].fillna("").str.contains(preferred_name, case=False, regex=False)
        matches = frame[mask]
        if not matches.empty:
            return matches.iloc[0].to_dict()
    safe_index = min(max(index, 0), len(frame) - 1)
    return frame.iloc[safe_index].to_dict()


def locate_validation_template(repo_root: Path, dataset_name: str) -> TemplateSelection:
    slug = _slugify(dataset_name)
    template_candidates = [
        repo_root / "tests" / "measure-validation" / "templates" / f"{slug}_measure_validation_template.csv",
        repo_root / "tests" / "measure-validation" / "templates" / "measure_validation_template.csv",
        repo_root / "tests" / "measure-validation" / "generated" / f"{slug}_measure_validation_candidates.csv",
        repo_root / "tests" / "measure-validation" / "generated" / "measure_validation_candidates.csv",
    ]
    for path in template_candidates:
        if not path.exists():
            continue
        template = read_validation_template(path)
        if not template.rows:
            if path.name == "measure_validation_template.csv":
                return TemplateSelection(path=path, source="shared_template", note="Template exists but does not yet contain dataset rows.")
            continue
        dataset_rows = [row for row in template.rows if row.dataset_name.lower() == dataset_name.lower()]
        if dataset_rows:
            source = "generated_candidates" if "generated" in path.parts else "template"
            return TemplateSelection(path=path, source=source, note=f"Loaded {len(dataset_rows)} row(s) for dataset '{dataset_name}'.")
        if path.name == "measure_validation_template.csv":
            shared_path = path
    if 'shared_path' in locals():
        return TemplateSelection(path=shared_path, source="shared_template", note="Using shared template with no dataset-specific rows yet.")
    return TemplateSelection(path=None, source="missing", note="No dataset-specific or shared measure validation template was found.")


def load_validation_cases(path: Path | None, dataset_name: str) -> pd.DataFrame:
    if path is None or not path.exists():
        return pd.DataFrame()
    rows = read_validation_template(path).rows
    frame = pd.DataFrame([case.to_row() for case in rows])
    if frame.empty:
        return frame
    dataset_mask = frame["dataset_name"].str.lower() == dataset_name.lower()
    filtered = frame[dataset_mask].copy()
    return filtered if not filtered.empty else frame


def filter_validation_cases(
    frame: pd.DataFrame,
    status: str = "",
    review_status: str = "",
    priority: str = "",
    measure_name: str = "",
    scenario_type: str = "",
) -> pd.DataFrame:
    if frame.empty:
        return frame
    filtered = frame.copy()
    filters = {
        "status": status,
        "review_status": review_status,
        "priority": priority,
        "scenario_type": scenario_type,
    }
    for column, value in filters.items():
        if value:
            filtered = filtered[filtered[column].str.lower() == value.lower()]
    if measure_name:
        filtered = filtered[filtered["measure_name"].str.contains(measure_name, case=False, regex=False)]
    return filtered.reset_index(drop=True)


def select_test_cases(frame: pd.DataFrame, selected_test_ids: list[str] | None = None, limit: int = 5) -> pd.DataFrame:
    if frame.empty:
        return frame
    if selected_test_ids:
        selected = frame[frame["test_id"].isin(selected_test_ids)].copy()
        if not selected.empty:
            return selected.reset_index(drop=True)
    return frame.head(limit).reset_index(drop=True)


def build_test_case_query(test_case: dict[str, Any]) -> str:
    measure_name = test_case["measure_name"]
    filter_context = str(test_case.get("filter_context", "")).strip()
    lines = [
        f"-- test_id: {test_case['test_id']}",
        f"-- measure: {test_case['table_name']}[{measure_name}]",
    ]
    if filter_context:
        lines.append(f"-- intended_filter_context: {filter_context}")
    if filter_context.startswith("DAX:"):
        dax_filter = filter_context.removeprefix("DAX:").strip()
        lines.extend(
            [
                "EVALUATE",
                "CALCULATETABLE(",
                f'    ROW("Measure", "{measure_name}", "Value", [{measure_name}]),',
                f"    {dax_filter}",
                ")",
            ]
        )
    else:
        lines.extend(
            [
                "EVALUATE",
                f'ROW("Measure", "{measure_name}", "Value", [{measure_name}])',
            ]
        )
    return "\n".join(lines)


def execute_validation_case(client, workspace_id: str, dataset_id: str, test_case: dict[str, Any]) -> dict[str, Any]:
    dax_query = build_test_case_query(test_case)
    try:
        rows = execute_dax_query(client, workspace_id, dataset_id, dax_query=dax_query)
        outcome = infer_outcome(test_case, rows)
        error = ""
    except Exception as exc:  # noqa: BLE001
        rows = []
        outcome = "error"
        error = str(exc)
    return {
        "test_id": test_case["test_id"],
        "measure_name": test_case["measure_name"],
        "scenario_type": test_case["scenario_type"],
        "expected_behavior": test_case["expected_behavior"],
        "expected_value": test_case["expected_value"],
        "dax_query": dax_query,
        "rows": rows,
        "row_count": len(rows),
        "outcome": outcome,
        "error": error,
    }


def infer_outcome(test_case: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "needs_review"
    expected_value = str(test_case.get("expected_value", "")).strip()
    if not expected_value or expected_value.lower().startswith(("reference", "business-approved", "blank or", "boundary", "context-", "0-100%", "negative", "no unintended", "business-approved")):
        return "needs_review"
    first_row = rows[0]
    first_value = next(iter(first_row.values()), None)
    return "pass" if str(first_value) == expected_value else "needs_review"


def build_execution_summary_frame(results: list[dict[str, Any]]) -> pd.DataFrame:
    columns = ["test_id", "measure_name", "scenario_type", "row_count", "outcome", "error"]
    return pd.DataFrame([{column: result.get(column) for column in columns} for result in results])


def build_report_context(repo_root: Path, workspace_reports: pd.DataFrame, dataset_id: str, dataset_name: str, selected_measures: list[str]) -> dict[str, Any]:
    api_reports = pd.DataFrame()
    if not workspace_reports.empty and "datasetId" in workspace_reports.columns:
        api_reports = workspace_reports[workspace_reports["datasetId"] == dataset_id].copy()
    local_report_rows: list[dict[str, Any]] = []
    local_report_path = default_report_definition_path()
    if local_report_path.exists() and dataset_name.lower() == "demo_dataset":
        report_result = inspect_report_definition(local_report_path, dataset_name=dataset_name)
        for usage in report_result.visual_usages:
            if usage.measure_name in selected_measures:
                local_report_rows.append(asdict(usage))
    return {
        "api_reports": api_reports.to_dict(orient="records") if not api_reports.empty else [],
        "local_measure_usage": local_report_rows,
        "selected_measure_count": len(selected_measures),
    }


def build_report_summary_markdown(report_context: dict[str, Any]) -> str:
    lines = ["# Report Summary", ""]
    api_reports = report_context.get("api_reports", [])
    local_usage = report_context.get("local_measure_usage", [])
    if api_reports:
        lines.append("## Workspace Reports")
        for report in api_reports:
            lines.append(f"- {report.get('name')} ({report.get('id')})")
        lines.append("")
    else:
        lines.append("No workspace report metadata was returned for the selected dataset.")
        lines.append("")
    if local_usage:
        lines.append("## Local PBIP Measure Usage")
        for usage in local_usage:
            lines.append(f"- {usage['page_name']} / {usage['visual_name']} -> {usage['table_name']}[{usage['measure_name']}]")
    else:
        lines.append("No local PBIP measure usage was available for the selected measures.")
    return "\n".join(lines)


def validation_cases_to_rows(frame: pd.DataFrame) -> list[dict[str, Any]]:
    return frame.to_dict(orient="records") if not frame.empty else []


def _slugify(value: str) -> str:
    return "".join(character.lower() if character.isalnum() else "-" for character in value).strip("-")
