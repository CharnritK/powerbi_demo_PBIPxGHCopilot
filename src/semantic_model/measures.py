"""Helpers for extracting measures and columns from TMDL files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


MEASURE_PATTERN = re.compile(r"^\s*measure\s+'?([^'=]+?)'?\s*=", re.MULTILINE)
COLUMN_PATTERN = re.compile(r"^\s*column\s+'?([^'\r\n]+?)'?(?:\s*$|\s)", re.MULTILINE)
DESCRIPTION_PATTERN = re.compile(r"^\s*description:\s*(.+)$", re.MULTILINE)


@dataclass(frozen=True)
class MeasureDefinition:
    table_name: str
    name: str
    source_file: Path
    description: str | None = None


def extract_measures_from_tmdl(table_path: Path) -> list[MeasureDefinition]:
    content = table_path.read_text(encoding="utf-8")
    table_name = table_path.stem
    descriptions = DESCRIPTION_PATTERN.findall(content)
    measures = MEASURE_PATTERN.findall(content)
    results: list[MeasureDefinition] = []
    for index, name in enumerate(measures):
        description = descriptions[index] if index < len(descriptions) else None
        results.append(
            MeasureDefinition(
                table_name=table_name,
                name=name.strip(),
                source_file=table_path,
                description=description.strip() if description else None,
            )
        )
    return results


def extract_columns_from_tmdl(table_path: Path) -> list[str]:
    content = table_path.read_text(encoding="utf-8")
    return [name.strip() for name in COLUMN_PATTERN.findall(content)]
