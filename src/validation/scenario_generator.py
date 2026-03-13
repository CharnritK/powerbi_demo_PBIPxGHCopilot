"""Generate draft measure validation scenarios from PBIP model and report metadata."""

from __future__ import annotations

import hashlib
from typing import Iterable

from .validation_case_models import (
    MeasureMetadata,
    MeasureScenario,
    ModelInspectionResult,
    ReportInspectionResult,
    ValidationCase,
    ValidationGenerationResult,
    VisualMeasureUsage,
)


def build_measure_validation_candidates(
    model_result: ModelInspectionResult,
    report_result: ReportInspectionResult | None = None,
    existing_cases: Iterable[ValidationCase] | None = None,
) -> ValidationGenerationResult:
    existing_cases = list(existing_cases or [])
    report_usages = list(report_result.visual_usages if report_result else [])
    usages_by_measure: dict[tuple[str, str], list[VisualMeasureUsage]] = {}
    for usage in report_usages:
        usages_by_measure.setdefault((usage.table_name, usage.measure_name), []).append(usage)

    cases: list[ValidationCase] = []
    coverage_rows: list[dict[str, str]] = []
    issues = list(model_result.issues)
    if report_result:
        issues.extend(report_result.issues)

    for measure in model_result.measures:
        usages = usages_by_measure.get((measure.table_name, measure.measure_name), [])
        coverage_rows.extend(_build_coverage_rows(measure, usages))
        scenarios = _base_scenarios_for_measure(measure, usages)
        cases.extend(_materialize_cases(measure, scenarios))

    issues.extend(_find_coverage_gaps(model_result, existing_cases, cases, report_usages))
    return ValidationGenerationResult(cases=cases, coverage_rows=coverage_rows, issues=issues)


def _build_coverage_rows(measure: MeasureMetadata, usages: list[VisualMeasureUsage]) -> list[dict[str, str]]:
    if not usages:
        return [
            {
                "dataset_name": measure.dataset_name,
                "report_name": "",
                "page_name": "",
                "visual_name": "",
                "visual_type": "",
                "table_name": measure.table_name,
                "measure_name": measure.measure_name,
                "usage_role": "",
                "is_high_visibility": "false",
                "priority_hint": "low",
            }
        ]
    return [
        {
            "dataset_name": usage.dataset_name,
            "report_name": usage.report_name,
            "page_name": usage.page_name,
            "visual_name": usage.visual_name,
            "visual_type": usage.visual_type,
            "table_name": usage.table_name,
            "measure_name": usage.measure_name,
            "usage_role": usage.usage_role,
            "is_high_visibility": str(usage.is_high_visibility).lower(),
            "priority_hint": "high" if usage.is_high_visibility else "medium",
        }
        for usage in usages
    ]


def _base_scenarios_for_measure(measure: MeasureMetadata, usages: list[VisualMeasureUsage]) -> list[MeasureScenario]:
    scenarios: list[MeasureScenario] = []
    primary_usage = usages[0] if usages else None
    business_purpose = measure.description or f"Validate business meaning for {measure.measure_name}."
    priority = _derive_priority(measure, usages)
    risk_level = _derive_risk_level(measure, usages)
    source = "pbip_report_scan" if usages else "pbip_model_scan"
    generated_by = "scenario_generator"
    report_name = primary_usage.report_name if primary_usage else ""
    page_name = primary_usage.page_name if primary_usage else ""
    visual_name = primary_usage.visual_name if primary_usage else ""

    scenarios.append(
        MeasureScenario(
            scenario_type="happy_path",
            scenario_description=f"Validate {measure.measure_name} under an expected business slice.",
            filter_context="Use a representative filter slice from the business domain.",
            input_assumptions=business_purpose,
            expected_behavior="The measure returns a stable value that matches the known business interpretation.",
            expected_value="Reference business-approved sample result",
            expected_value_type="example_numeric",
            comparison_rule="equals_or_matches_reference",
            priority=priority,
            risk_level=risk_level,
            source=source,
            generated_by=generated_by,
            notes="Draft scenario inferred from semantic model metadata.",
            report_name=report_name,
            page_name=page_name,
            visual_name=visual_name,
        )
    )

    expr_upper = measure.dax_expression.upper()
    if "DIVIDE(" in expr_upper:
        scenarios.append(
            MeasureScenario(
                scenario_type="divide_by_zero",
                scenario_description=f"Verify {measure.measure_name} handles zero or blank denominator safely.",
                filter_context="Apply a slice where the denominator measure resolves to zero or blank.",
                input_assumptions="A ratio should not throw an error or present misleading infinite output.",
                expected_behavior="The measure returns BLANK or the defined safe fallback instead of an error.",
                expected_value="BLANK or explicit fallback",
                expected_value_type="semantic_result",
                comparison_rule="safe_divide_behavior",
                priority="high",
                risk_level="high",
                source=source,
                generated_by=generated_by,
                notes="Generated because the DAX expression uses DIVIDE.",
                report_name=report_name,
                page_name=page_name,
                visual_name=visual_name,
            )
        )
    if "YTD" in measure.measure_name.upper() or any(flag == "time_intelligence" for flag in measure.risk_flags):
        scenarios.append(
            MeasureScenario(
                scenario_type="time_intelligence",
                scenario_description=f"Validate {measure.measure_name} across a year boundary.",
                filter_context="Compare the last period of one year to the first period of the next year.",
                input_assumptions="Time-intelligence logic should reset or roll correctly at the calendar boundary.",
                expected_behavior="The measure respects the intended year-to-date boundary and does not leak prior-year totals.",
                expected_value="Boundary-aware result",
                expected_value_type="semantic_result",
                comparison_rule="time_boundary_correct",
                priority="high",
                risk_level="high",
                source=source,
                generated_by=generated_by,
                notes="Generated because the measure looks like time intelligence.",
                report_name=report_name,
                page_name=page_name,
                visual_name=visual_name,
            )
        )
    if "MARGIN" in measure.measure_name.upper() or "VARIANCE" in measure.measure_name.upper() or "VAR" in measure.measure_name.upper():
        scenarios.append(
            MeasureScenario(
                scenario_type="negative_values",
                scenario_description=f"Validate {measure.measure_name} when costs exceed sales or the base value is negative.",
                filter_context="Use a slice where the underlying numerator can produce a negative result.",
                input_assumptions="Variance and margin metrics need explicit sign behavior validation.",
                expected_behavior="The measure preserves the correct sign and does not clamp negative results unexpectedly.",
                expected_value="Negative numeric result allowed",
                expected_value_type="numeric_sign",
                comparison_rule="sign_preserved",
                priority="high",
                risk_level="high",
                source=source,
                generated_by=generated_by,
                notes="Generated because the measure name suggests margin or variance logic.",
                report_name=report_name,
                page_name=page_name,
                visual_name=visual_name,
            )
        )
    if any(flag in {"calculate_logic", "filter_removal"} for flag in measure.risk_flags):
        scenarios.append(
            MeasureScenario(
                scenario_type="filter_context",
                scenario_description=f"Validate {measure.measure_name} under targeted filter context changes.",
                filter_context="Apply and remove the main dimensional filters used by the report.",
                input_assumptions="CALCULATE and filter-removal logic can change totals in non-obvious ways.",
                expected_behavior="The measure follows documented filter semantics and ignores or keeps filters as intended.",
                expected_value="Context-sensitive result",
                expected_value_type="semantic_result",
                comparison_rule="filter_semantics_correct",
                priority="high",
                risk_level="high",
                source=source,
                generated_by=generated_by,
                notes="Generated because the expression changes filter context.",
                report_name=report_name,
                page_name=page_name,
                visual_name=visual_name,
            )
        )
    if "%" in measure.measure_name or (measure.format_string or "").endswith("%"):
        scenarios.append(
            MeasureScenario(
                scenario_type="format_consistency",
                scenario_description=f"Validate {measure.measure_name} formatting and semantic percentage range.",
                filter_context="Use a representative slice from a report visual.",
                input_assumptions="Percentage measures should render consistently and preserve business meaning.",
                expected_behavior="The measure stays in a sensible percentage range and uses the intended format string.",
                expected_value="0-100% aligned output",
                expected_value_type="formatted_numeric",
                comparison_rule="format_and_range_valid",
                priority=priority,
                risk_level=risk_level,
                source=source,
                generated_by=generated_by,
                notes="Generated because the measure is formatted or named like a percentage.",
                report_name=report_name,
                page_name=page_name,
                visual_name=visual_name,
            )
        )
    if usages:
        scenarios.append(
            MeasureScenario(
                scenario_type="regression",
                scenario_description=f"Protect {measure.measure_name} behavior for the report visual currently using it.",
                filter_context=f"Recreate the context of {primary_usage.page_name} / {primary_usage.visual_name}.",
                input_assumptions="Measures used in visible report visuals should be protected against accidental regression.",
                expected_behavior="The measure remains stable for the referenced page and visual after semantic-model changes.",
                expected_value="No unintended visual regression",
                expected_value_type="report_behavior",
                comparison_rule="visual_regression_free",
                priority="high" if primary_usage.is_high_visibility else priority,
                risk_level=risk_level,
                source="pbip_report_scan",
                generated_by=generated_by,
                notes="Generated from report usage metadata and still requires human review.",
                report_name=report_name,
                page_name=page_name,
                visual_name=visual_name,
            )
        )
        if primary_usage.visual_type in {"lineChart", "barChart", "columnChart", "cardVisual"}:
            scenarios.append(
                MeasureScenario(
                    scenario_type="grand_total_behavior",
                    scenario_description=f"Validate total behavior for {measure.measure_name} in its report visual context.",
                    filter_context=f"Compare row-level or point-level values to the aggregate total on {primary_usage.page_name}.",
                    input_assumptions="Visual totals for non-additive measures can mislead unless explicitly validated.",
                    expected_behavior="Totals align with the intended business rule rather than accidental aggregation.",
                    expected_value="Business-approved total behavior",
                    expected_value_type="semantic_result",
                    comparison_rule="total_behavior_correct",
                    priority=priority,
                    risk_level=risk_level,
                    source="pbip_report_scan",
                    generated_by=generated_by,
                    notes="Generated because the measure is used in a chart or card visual.",
                    report_name=report_name,
                    page_name=page_name,
                    visual_name=visual_name,
                )
            )
    return _dedupe_scenarios(scenarios)


def _materialize_cases(measure: MeasureMetadata, scenarios: list[MeasureScenario]) -> list[ValidationCase]:
    business_purpose = measure.description or f"Validate {measure.measure_name} business behavior."
    cases: list[ValidationCase] = []
    for scenario in scenarios:
        digest_source = "|".join(
            [
                measure.dataset_name,
                scenario.report_name,
                scenario.page_name,
                scenario.visual_name,
                measure.table_name,
                measure.measure_name,
                scenario.scenario_type,
                scenario.scenario_description,
            ]
        )
        digest = hashlib.sha1(digest_source.encode("utf-8")).hexdigest()[:10]
        cases.append(
            ValidationCase(
                test_id=f"mv_{digest}",
                status="draft",
                review_status="inferred",
                dataset_name=measure.dataset_name,
                report_name=scenario.report_name,
                page_name=scenario.page_name,
                visual_name=scenario.visual_name,
                table_name=measure.table_name,
                measure_name=measure.measure_name,
                dax_expression=measure.dax_expression,
                business_purpose=business_purpose,
                scenario_type=scenario.scenario_type,
                scenario_description=scenario.scenario_description,
                filter_context=scenario.filter_context,
                input_assumptions=scenario.input_assumptions,
                expected_behavior=scenario.expected_behavior,
                expected_value=scenario.expected_value,
                expected_value_type=scenario.expected_value_type,
                comparison_rule=scenario.comparison_rule,
                priority=scenario.priority,
                risk_level=scenario.risk_level,
                source=scenario.source,
                generated_by=scenario.generated_by,
                notes=scenario.notes,
            )
        )
    return cases


def _derive_priority(measure: MeasureMetadata, usages: list[VisualMeasureUsage]) -> str:
    if usages and any(usage.is_high_visibility for usage in usages):
        return "high"
    if usages:
        return "high"
    if any(flag in {"divide_logic", "calculate_logic", "time_intelligence", "variance_logic", "ranking_logic"} for flag in measure.risk_flags):
        return "high"
    if measure.dependencies:
        return "medium"
    return "low"


def _derive_risk_level(measure: MeasureMetadata, usages: list[VisualMeasureUsage]) -> str:
    if any(flag in {"divide_logic", "calculate_logic", "time_intelligence", "variance_logic", "ranking_logic"} for flag in measure.risk_flags):
        return "high"
    if usages:
        return "medium"
    return "low"


def _dedupe_scenarios(scenarios: list[MeasureScenario]) -> list[MeasureScenario]:
    seen: set[tuple[str, str, str, str]] = set()
    unique: list[MeasureScenario] = []
    for scenario in scenarios:
        key = (scenario.scenario_type, scenario.scenario_description, scenario.page_name, scenario.visual_name)
        if key in seen:
            continue
        seen.add(key)
        unique.append(scenario)
    return unique


def _find_coverage_gaps(
    model_result: ModelInspectionResult,
    existing_cases: list[ValidationCase],
    generated_cases: list[ValidationCase],
    report_usages: list[VisualMeasureUsage],
) -> list[str]:
    covered_measures = {(row.table_name, row.measure_name) for row in existing_cases + generated_cases}
    issues: list[str] = []
    for usage in report_usages:
        key = (usage.table_name, usage.measure_name)
        if key not in covered_measures:
            issues.append(
                f"Coverage gap: report-critical measure '{usage.table_name}[{usage.measure_name}]' on page '{usage.page_name}' has no validation case."
            )
    for measure in model_result.measures:
        key = (measure.table_name, measure.measure_name)
        if key not in covered_measures:
            issues.append(f"Coverage gap: model measure '{measure.table_name}[{measure.measure_name}]' has no validation case.")
    return issues
