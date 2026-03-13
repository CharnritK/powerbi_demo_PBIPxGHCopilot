"""Local validation helpers for TMDL semantic model folders."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.common.errors import SemanticModelValidationError
from src.semantic_model.measures import extract_columns_from_tmdl, extract_measures_from_tmdl


@dataclass(frozen=True)
class ValidationReport:
    definition_path: Path
    table_count: int
    measure_count: int
    column_count: int
    issues: list[str]

    @property
    def is_valid(self) -> bool:
        return not self.issues


def validate_tmdl_definition(definition_path: Path) -> ValidationReport:
    if not definition_path.exists():
        raise SemanticModelValidationError(f"Definition folder does not exist: {definition_path}")
    tables_path = definition_path / "tables"
    if not tables_path.exists():
        raise SemanticModelValidationError(f"Tables folder does not exist: {tables_path}")

    table_files = sorted(tables_path.glob("*.tmdl"))
    column_names: set[str] = set()
    measure_names: set[str] = set()
    issues: list[str] = []
    column_count = 0
    measure_count = 0

    for table_path in table_files:
        columns = extract_columns_from_tmdl(table_path)
        measures = extract_measures_from_tmdl(table_path)
        column_count += len(columns)
        measure_count += len(measures)
        for column in columns:
            column_names.add(column)
        for measure in measures:
            if measure.name in column_names:
                issues.append(f"Measure '{measure.name}' in table '{measure.table_name}' collides with an existing column name.")
            if measure.name in measure_names:
                issues.append(f"Duplicate measure name detected: '{measure.name}'.")
            measure_names.add(measure.name)

    for required_file in ("database.tmdl", "model.tmdl", "relationships.tmdl"):
        if not (definition_path / required_file).exists():
            issues.append(f"Missing required semantic model file: {required_file}")

    return ValidationReport(
        definition_path=definition_path,
        table_count=len(table_files),
        measure_count=measure_count,
        column_count=column_count,
        issues=issues,
    )
