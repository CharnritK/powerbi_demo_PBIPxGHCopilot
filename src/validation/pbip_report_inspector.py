"""Inspect PBIR report metadata to identify measure usage in visuals."""

from __future__ import annotations

import json
from pathlib import Path

from .validation_case_models import ReportInspectionResult, VisualMeasureUsage


HIGH_VISIBILITY_PAGE_TERMS = ("executive", "overview", "summary", "kpi")
HIGH_VISIBILITY_VISUAL_TYPES = {"cardVisual", "multiRowCard"}


def inspect_report_definition(report_definition_path: Path, dataset_name: str | None = None) -> ReportInspectionResult:
    issues: list[str] = []
    usages: list[VisualMeasureUsage] = []
    inferred_dataset_name = dataset_name or report_definition_path.parent.stem.replace(".Report", "")
    report_name = report_definition_path.parent.stem.replace(".Report", "")
    pages_root = report_definition_path / "pages"
    pages_json_path = pages_root / "pages.json"

    if not report_definition_path.exists():
        return ReportInspectionResult(inferred_dataset_name, report_name, report_definition_path, (), (f"Report path does not exist: {report_definition_path}",))
    if not pages_json_path.exists():
        return ReportInspectionResult(inferred_dataset_name, report_name, report_definition_path, (), (f"Missing pages metadata: {pages_json_path}",))

    try:
        pages_payload = json.loads(pages_json_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return ReportInspectionResult(inferred_dataset_name, report_name, report_definition_path, (), (f"Failed to read pages metadata: {exc}",))

    for page_id in pages_payload.get("pageOrder", []):
        page_path = pages_root / page_id / "page.json"
        visuals_root = pages_root / page_id / "visuals"
        page_name = page_id
        try:
            if page_path.exists():
                page_payload = json.loads(page_path.read_text(encoding="utf-8"))
                page_name = page_payload.get("displayName", page_name)
        except (OSError, json.JSONDecodeError) as exc:
            issues.append(f"Failed to parse page metadata for {page_id}: {exc}")
        if not visuals_root.exists():
            continue
        for visual_path in sorted(visuals_root.glob("*/visual.json")):
            usages.extend(_extract_visual_measure_usage(visual_path, inferred_dataset_name, report_name, page_id, page_name, issues))

    return ReportInspectionResult(
        dataset_name=inferred_dataset_name,
        report_name=report_name,
        definition_path=report_definition_path,
        visual_usages=tuple(usages),
        issues=tuple(issues),
    )


def _extract_visual_measure_usage(
    visual_path: Path,
    dataset_name: str,
    report_name: str,
    page_id: str,
    page_name: str,
    issues: list[str],
) -> list[VisualMeasureUsage]:
    try:
        payload = json.loads(visual_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        issues.append(f"Failed to parse visual metadata for {visual_path}: {exc}")
        return []

    visual_name = payload.get("name", visual_path.parent.name)
    visual_type = payload.get("visual", {}).get("visualType", "")
    query_state = payload.get("visual", {}).get("query", {}).get("queryState", {})
    usages: list[VisualMeasureUsage] = []
    for usage_role, section in query_state.items():
        projections = section.get("projections", []) if isinstance(section, dict) else []
        for projection in projections:
            field = projection.get("field", {})
            measure = field.get("Measure")
            if not measure:
                continue
            source_ref = measure.get("Expression", {}).get("SourceRef", {})
            table_name = source_ref.get("Entity", "")
            measure_name = measure.get("Property", "")
            usages.append(
                VisualMeasureUsage(
                    dataset_name=dataset_name,
                    report_name=report_name,
                    page_name=page_name,
                    visual_name=visual_name,
                    visual_type=visual_type,
                    table_name=table_name,
                    measure_name=measure_name,
                    usage_role=usage_role,
                    page_id=page_id,
                    visual_id=visual_name,
                    query_ref=projection.get("queryRef", ""),
                    is_high_visibility=_is_high_visibility(page_name, visual_type),
                )
            )
    return usages


def _is_high_visibility(page_name: str, visual_type: str) -> bool:
    page_lower = page_name.lower()
    return any(term in page_lower for term in HIGH_VISIBILITY_PAGE_TERMS) or visual_type in HIGH_VISIBILITY_VISUAL_TYPES
