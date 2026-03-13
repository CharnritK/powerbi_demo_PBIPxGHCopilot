from __future__ import annotations

import csv
from pathlib import Path

import pytest

from src.validation.measure_validation_template import REQUIRED_TEMPLATE_COLUMNS, merge_validation_cases, read_validation_template
from src.validation.validation_case_models import ValidationCase


REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_PATH = REPO_ROOT / "tests" / "measure-validation" / "templates" / "measure_validation_template.csv"
FIXTURE_PATH = REPO_ROOT / "tests" / "measure-validation" / "fixtures" / "sample_validation_cases.csv"


def test_template_schema_matches_required_columns() -> None:
    with TEMPLATE_PATH.open("r", encoding="utf-8", newline="") as handle:
        header = next(csv.reader(handle))
    assert header == REQUIRED_TEMPLATE_COLUMNS


def test_fixture_rows_are_parsable() -> None:
    template = read_validation_template(FIXTURE_PATH)
    assert len(template.rows) == 2
    assert all(isinstance(row, ValidationCase) for row in template.rows)


def test_invalid_status_is_rejected(tmp_path: Path) -> None:
    bad_csv = tmp_path / "invalid.csv"
    bad_csv.write_text(
        ",".join(REQUIRED_TEMPLATE_COLUMNS)
        + "\n"
        + "mv_bad,wrong,inferred,demo_dataset,,,,Fact Sales,Total Sales,SUM('Fact Sales'[Sales Amount]),Purpose,happy_path,Desc,Context,Assumption,Behavior,1,numeric,equals,high,medium,manual,human,\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="Invalid status"):
        read_validation_template(bad_csv)


def test_duplicate_test_id_is_flagged(tmp_path: Path) -> None:
    dup_csv = tmp_path / "duplicate.csv"
    dup_csv.write_text(
        ",".join(REQUIRED_TEMPLATE_COLUMNS)
        + "\n"
        + "mv_dup,draft,inferred,demo_dataset,,,,Fact Sales,Total Sales,SUM('Fact Sales'[Sales Amount]),Purpose,happy_path,Desc,Context,Assumption,Behavior,1,numeric,equals,high,medium,manual,human,\n"
        + "mv_dup,draft,inferred,demo_dataset,,,,Fact Sales,Total Cost,SUM('Fact Sales'[Cost Amount]),Purpose,happy_path,Desc,Context,Assumption,Behavior,1,numeric,equals,medium,low,manual,human,\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="Duplicate test_id"):
        read_validation_template(dup_csv)


def test_merge_preserves_reviewed_rows() -> None:
    existing = read_validation_template(FIXTURE_PATH).rows
    generated = [
        ValidationCase(
            test_id="mv_sample_total_sales_reviewed",
            status="draft",
            review_status="inferred",
            dataset_name="demo_dataset",
            report_name="demo_dataset",
            page_name="Executive Overview",
            visual_name="f965bb9fbe20448b0e05",
            table_name="Fact Sales",
            measure_name="Total Sales",
            dax_expression="SUM('Fact Sales'[Sales Amount])",
            business_purpose="Generated change that should not overwrite reviewed row",
            scenario_type="regression",
            scenario_description="Generated scenario",
            filter_context="Any",
            input_assumptions="Any",
            expected_behavior="Any",
            expected_value="Any",
            expected_value_type="semantic_result",
            comparison_rule="equals",
            priority="high",
            risk_level="high",
            source="codex_generated",
            generated_by="scenario_generator",
            notes="Should be ignored because reviewed row already exists.",
        )
    ]
    merged = merge_validation_cases(existing, generated)
    row = next(item for item in merged if item.test_id == "mv_sample_total_sales_reviewed")
    assert row.review_status == "approved"
    assert row.scenario_type == "happy_path"
