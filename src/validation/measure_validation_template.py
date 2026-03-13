"""CSV template helpers for measure validation workflows."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from .validation_case_models import ValidationCase


REQUIRED_TEMPLATE_COLUMNS = [
    "test_id",
    "status",
    "review_status",
    "dataset_name",
    "report_name",
    "page_name",
    "visual_name",
    "table_name",
    "measure_name",
    "dax_expression",
    "business_purpose",
    "scenario_type",
    "scenario_description",
    "filter_context",
    "input_assumptions",
    "expected_behavior",
    "expected_value",
    "expected_value_type",
    "comparison_rule",
    "priority",
    "risk_level",
    "source",
    "generated_by",
    "notes",
]

PROTECTED_REVIEW_STATUSES = {"human_reviewed", "approved"}


@dataclass(frozen=True)
class MeasureValidationTemplate:
    path: Path
    rows: list[ValidationCase]


def read_validation_template(path: Path) -> MeasureValidationTemplate:
    if not path.exists():
        return MeasureValidationTemplate(path=path, rows=[])
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        _validate_header(reader.fieldnames)
        rows = [ValidationCase.from_row(row) for row in reader]
    _ensure_unique_test_ids(rows)
    return MeasureValidationTemplate(path=path, rows=rows)


def write_validation_template(path: Path, rows: list[ValidationCase]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    _ensure_unique_test_ids(rows)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REQUIRED_TEMPLATE_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row.to_row())


def merge_validation_cases(existing_rows: list[ValidationCase], generated_rows: list[ValidationCase]) -> list[ValidationCase]:
    _ensure_unique_test_ids(existing_rows)
    _ensure_unique_test_ids(generated_rows)
    merged: dict[str, ValidationCase] = {row.test_id: row for row in existing_rows}
    for generated in generated_rows:
        current = merged.get(generated.test_id)
        if current and current.review_status in PROTECTED_REVIEW_STATUSES:
            continue
        merged[generated.test_id] = generated
    return sorted(merged.values(), key=lambda row: (row.measure_name.lower(), row.scenario_type, row.test_id))


def _validate_header(fieldnames: list[str] | None) -> None:
    if fieldnames is None:
        raise ValueError("CSV template is missing a header row.")
    missing = [column for column in REQUIRED_TEMPLATE_COLUMNS if column not in fieldnames]
    if missing:
        raise ValueError(f"CSV template is missing required columns: {', '.join(missing)}")


def _ensure_unique_test_ids(rows: list[ValidationCase]) -> None:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for row in rows:
        if row.test_id in seen:
            duplicates.add(row.test_id)
        seen.add(row.test_id)
    if duplicates:
        raise ValueError(f"Duplicate test_id values detected: {', '.join(sorted(duplicates))}")
