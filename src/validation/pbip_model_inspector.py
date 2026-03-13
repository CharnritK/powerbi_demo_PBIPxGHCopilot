"""Inspect PBIP/TMDL semantic model artifacts for measure validation workflows."""

from __future__ import annotations

from pathlib import Path
import re

from .validation_case_models import MeasureDependency, MeasureMetadata, ModelInspectionResult


MEASURE_START_RE = re.compile(r"^\s*measure\s+'?([^'=]+?)'?\s*=\s*(.+)$")
COLUMN_RE = re.compile(r"^\s*column\s+'?([^'\r\n]+?)'?(?:\s*$|\s)")
ATTRIBUTE_RE = re.compile(r"^\s*(formatString|displayFolder):\s*(.+)$")
BRACKET_DEPENDENCY_RE = re.compile(r"\[([^\]]+)\]")
TABLE_COLUMN_DEP_RE = re.compile(r"'([^']+)'\[([^\]]+)\]")


def inspect_semantic_model(definition_path: Path) -> ModelInspectionResult:
    tables_path = definition_path / "tables"
    issues: list[str] = []
    measures: list[MeasureMetadata] = []
    columns_by_table: dict[str, tuple[str, ...]] = {}
    table_names: list[str] = []
    dataset_name = definition_path.parent.stem.replace(".SemanticModel", "")

    if not definition_path.exists():
        return ModelInspectionResult(dataset_name, definition_path, (), (), {}, (f"Definition path does not exist: {definition_path}",))
    if not tables_path.exists():
        return ModelInspectionResult(dataset_name, definition_path, (), (), {}, (f"Tables path does not exist: {tables_path}",))

    for table_path in sorted(tables_path.glob("*.tmdl")):
        table_names.append(table_path.stem)
        try:
            content = table_path.read_text(encoding="utf-8")
        except OSError as exc:
            issues.append(f"Failed to read {table_path}: {exc}")
            continue
        columns_by_table[table_path.stem] = tuple(_extract_columns(content))
        measures.extend(_extract_measure_metadata(dataset_name, table_path, content))

    return ModelInspectionResult(
        dataset_name=dataset_name,
        definition_path=definition_path,
        measures=tuple(measures),
        tables=tuple(table_names),
        columns_by_table=columns_by_table,
        issues=tuple(issues),
    )


def _extract_columns(content: str) -> list[str]:
    return [match.group(1).strip() for match in COLUMN_RE.finditer(content)]


def _extract_measure_metadata(dataset_name: str, table_path: Path, content: str) -> list[MeasureMetadata]:
    measures: list[MeasureMetadata] = []
    table_name = table_path.stem
    pending_description: str | None = None
    active: dict[str, str | None] | None = None

    for raw_line in content.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("///"):
            pending_description = stripped.removeprefix("///").strip()
            continue

        measure_match = MEASURE_START_RE.match(raw_line)
        if measure_match:
            if active:
                measures.append(_build_measure(dataset_name, table_name, table_path, active))
            active = {
                "name": measure_match.group(1).strip(),
                "expression": measure_match.group(2).strip(),
                "description": pending_description,
                "format_string": "",
                "display_folder": "",
            }
            pending_description = None
            continue

        if active:
            attr_match = ATTRIBUTE_RE.match(raw_line)
            if attr_match:
                if attr_match.group(1) == "formatString":
                    active["format_string"] = attr_match.group(2).strip()
                if attr_match.group(1) == "displayFolder":
                    active["display_folder"] = attr_match.group(2).strip()
                continue
            if stripped.startswith(("measure ", "column ", "partition ", "table ")):
                measures.append(_build_measure(dataset_name, table_name, table_path, active))
                active = None

    if active:
        measures.append(_build_measure(dataset_name, table_name, table_path, active))
    return measures


def _build_measure(
    dataset_name: str,
    table_name: str,
    table_path: Path,
    active: dict[str, str | None],
) -> MeasureMetadata:
    expression = active["expression"] or ""
    return MeasureMetadata(
        dataset_name=dataset_name,
        table_name=table_name,
        measure_name=active["name"] or "",
        dax_expression=expression,
        description=active.get("description") or None,
        format_string=active.get("format_string") or None,
        display_folder=active.get("display_folder") or None,
        source_file=table_path,
        dependencies=tuple(_extract_dependencies(table_name, expression)),
        risk_flags=tuple(_extract_risk_flags(active["name"] or "", expression)),
        naming_patterns=tuple(_extract_naming_patterns(active["name"] or "", expression)),
    )


def _extract_dependencies(table_name: str, expression: str) -> list[MeasureDependency]:
    dependencies: list[MeasureDependency] = []
    seen: set[tuple[str, str | None, str]] = set()

    for dep_table, dep_column in TABLE_COLUMN_DEP_RE.findall(expression):
        key = ("column", dep_table, dep_column)
        if key not in seen:
            seen.add(key)
            dependencies.append(MeasureDependency("column", dep_table, dep_column))

    for bracket_name in BRACKET_DEPENDENCY_RE.findall(expression):
        if any(dep.object_name == bracket_name for dep in dependencies):
            continue
        key = ("measure", table_name, bracket_name)
        if key not in seen:
            seen.add(key)
            dependencies.append(MeasureDependency("measure", table_name, bracket_name))

    return dependencies


def _extract_risk_flags(measure_name: str, expression: str) -> list[str]:
    expression_upper = expression.upper()
    flags: list[str] = []
    token_map = {
        "DIVIDE(": "divide_logic",
        "CALCULATE(": "calculate_logic",
        "ALL(": "filter_removal",
        "ALLEXCEPT(": "filter_removal",
        "REMOVEFILTERS(": "filter_removal",
        "TOTALYTD(": "time_intelligence",
        "DATESYTD(": "time_intelligence",
        "SAMEPERIODLASTYEAR(": "time_intelligence",
        "DATEADD(": "time_intelligence",
        "IF(": "branching_logic",
        "SWITCH(": "branching_logic",
        "COALESCE(": "blank_handling",
        "ISBLANK(": "blank_handling",
        "RANKX(": "ranking_logic",
    }
    for token, flag in token_map.items():
        if token in expression_upper and flag not in flags:
            flags.append(flag)
    if "%" in measure_name or "PERCENT" in expression_upper:
        flags.append("percentage_logic")
    if "VAR" in measure_name.upper() or "VARIANCE" in measure_name.upper():
        flags.append("variance_logic")
    if "YTD" in measure_name.upper():
        flags.append("time_intelligence")
    return flags


def _extract_naming_patterns(measure_name: str, expression: str) -> list[str]:
    patterns: list[str] = []
    name_upper = measure_name.upper()
    expr_upper = expression.upper()
    if measure_name.startswith("Total "):
        patterns.append("total_prefix")
    if "%" in measure_name:
        patterns.append("percentage_suffix")
    if "AVERAGE" in name_upper or "AVERAGEX(" in expr_upper:
        patterns.append("average_metric")
    if "MARGIN" in name_upper:
        patterns.append("margin_metric")
    if "COUNT" in name_upper:
        patterns.append("count_metric")
    return patterns
