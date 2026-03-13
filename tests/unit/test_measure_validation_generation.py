from __future__ import annotations

from pathlib import Path

from src.validation.measure_validation_template import read_validation_template
from src.validation.pbip_model_inspector import inspect_semantic_model
from src.validation.pbip_report_inspector import inspect_report_definition
from src.validation.scenario_generator import build_measure_validation_candidates


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFINITION = (
    REPO_ROOT
    / "demo-enterprise"
    / "bi-repo"
    / "powerbi"
    / "workspaces"
    / "regional-sales-trust-demo"
    / "pbip"
    / "demo_dataset.SemanticModel"
    / "definition"
)
REPORT = (
    REPO_ROOT
    / "demo-enterprise"
    / "bi-repo"
    / "powerbi"
    / "workspaces"
    / "regional-sales-trust-demo"
    / "pbip"
    / "demo_dataset.Report"
    / "definition"
)
FIXTURE = REPO_ROOT / "tests" / "measure-validation" / "fixtures" / "sample_validation_cases.csv"


def test_scenario_generator_produces_output_for_committed_pbip() -> None:
    model_result = inspect_semantic_model(DEFINITION)
    report_result = inspect_report_definition(REPORT, dataset_name=model_result.dataset_name)
    generated = build_measure_validation_candidates(model_result, report_result)
    assert len(model_result.measures) >= 6
    assert len(report_result.visual_usages) >= 3
    assert generated.cases
    assert any(case.scenario_type == "divide_by_zero" for case in generated.cases)
    assert any(case.page_name == "Executive Overview" for case in generated.cases)


def test_existing_reviewed_cases_can_be_used_during_gap_analysis() -> None:
    existing = read_validation_template(FIXTURE).rows
    model_result = inspect_semantic_model(DEFINITION)
    report_result = inspect_report_definition(REPORT, dataset_name=model_result.dataset_name)
    generated = build_measure_validation_candidates(model_result, report_result, existing)
    assert generated.coverage_rows
    assert any(row["measure_name"] == "Total Sales" for row in generated.coverage_rows)
