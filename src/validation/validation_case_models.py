"""Typed models for measure validation templates and PBIP inspection output."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


VALID_STATUSES = {"draft", "active", "deprecated"}
VALID_REVIEW_STATUSES = {"inferred", "human_reviewed", "approved"}
VALID_SOURCES = {"manual", "pbip_model_scan", "pbip_report_scan", "codex_generated"}
VALID_SCENARIO_TYPES = {
    "happy_path",
    "filter_context",
    "time_intelligence",
    "blank_handling",
    "divide_by_zero",
    "negative_values",
    "grand_total_behavior",
    "slicer_interaction",
    "rls_sensitive",
    "format_consistency",
    "regression",
}
VALID_PRIORITIES = {"high", "medium", "low"}
VALID_RISK_LEVELS = {"high", "medium", "low"}


@dataclass(frozen=True)
class MeasureDependency:
    dependency_type: str
    table_name: str | None
    object_name: str


@dataclass(frozen=True)
class MeasureMetadata:
    dataset_name: str
    table_name: str
    measure_name: str
    dax_expression: str
    description: str | None = None
    format_string: str | None = None
    display_folder: str | None = None
    source_file: Path | None = None
    dependencies: tuple[MeasureDependency, ...] = ()
    risk_flags: tuple[str, ...] = ()
    naming_patterns: tuple[str, ...] = ()


@dataclass(frozen=True)
class ModelInspectionResult:
    dataset_name: str
    definition_path: Path
    measures: tuple[MeasureMetadata, ...]
    tables: tuple[str, ...]
    columns_by_table: dict[str, tuple[str, ...]]
    issues: tuple[str, ...] = ()


@dataclass(frozen=True)
class VisualMeasureUsage:
    dataset_name: str
    report_name: str
    page_name: str
    visual_name: str
    visual_type: str
    table_name: str
    measure_name: str
    usage_role: str
    page_id: str | None = None
    visual_id: str | None = None
    query_ref: str | None = None
    is_high_visibility: bool = False


@dataclass(frozen=True)
class ReportInspectionResult:
    dataset_name: str
    report_name: str
    definition_path: Path
    visual_usages: tuple[VisualMeasureUsage, ...]
    issues: tuple[str, ...] = ()


@dataclass(frozen=True)
class ValidationCase:
    test_id: str
    status: str
    review_status: str
    dataset_name: str
    report_name: str
    page_name: str
    visual_name: str
    table_name: str
    measure_name: str
    dax_expression: str
    business_purpose: str
    scenario_type: str
    scenario_description: str
    filter_context: str
    input_assumptions: str
    expected_behavior: str
    expected_value: str
    expected_value_type: str
    comparison_rule: str
    priority: str
    risk_level: str
    source: str
    generated_by: str
    notes: str = ""

    def validate(self) -> None:
        if self.status not in VALID_STATUSES:
            raise ValueError(f"Invalid status '{self.status}' for test_id '{self.test_id}'.")
        if self.review_status not in VALID_REVIEW_STATUSES:
            raise ValueError(f"Invalid review_status '{self.review_status}' for test_id '{self.test_id}'.")
        if self.source not in VALID_SOURCES:
            raise ValueError(f"Invalid source '{self.source}' for test_id '{self.test_id}'.")
        if self.scenario_type not in VALID_SCENARIO_TYPES:
            raise ValueError(f"Invalid scenario_type '{self.scenario_type}' for test_id '{self.test_id}'.")
        if self.priority not in VALID_PRIORITIES:
            raise ValueError(f"Invalid priority '{self.priority}' for test_id '{self.test_id}'.")
        if self.risk_level not in VALID_RISK_LEVELS:
            raise ValueError(f"Invalid risk_level '{self.risk_level}' for test_id '{self.test_id}'.")
        if not self.test_id.strip():
            raise ValueError("test_id is required.")
        if not self.dataset_name.strip():
            raise ValueError(f"dataset_name is required for test_id '{self.test_id}'.")
        if not self.table_name.strip():
            raise ValueError(f"table_name is required for test_id '{self.test_id}'.")
        if not self.measure_name.strip():
            raise ValueError(f"measure_name is required for test_id '{self.test_id}'.")

    def to_row(self) -> dict[str, str]:
        self.validate()
        return {key: _stringify(value) for key, value in asdict(self).items()}

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> "ValidationCase":
        cleaned = {key: _stringify(value).strip() for key, value in row.items()}
        instance = cls(**cleaned)
        instance.validate()
        return instance


@dataclass(frozen=True)
class MeasureScenario:
    scenario_type: str
    scenario_description: str
    filter_context: str
    input_assumptions: str
    expected_behavior: str
    expected_value: str
    expected_value_type: str
    comparison_rule: str
    priority: str
    risk_level: str
    source: str
    generated_by: str
    notes: str = ""
    report_name: str = ""
    page_name: str = ""
    visual_name: str = ""


@dataclass
class ValidationGenerationResult:
    cases: list[ValidationCase]
    coverage_rows: list[dict[str, str]] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    return str(value)
