"""Lineage and source mapping helpers for the sample semantic model."""

from __future__ import annotations

from pathlib import Path
import re


SOURCE_PATTERN = re.compile(r'File\.Contents\(DataRootFolder\s*&\s*"[\\/]*([^"]+)"\)')


def build_source_to_model_mapping(definition_path: Path) -> list[dict]:
    tables_path = definition_path / "tables"
    mapping: list[dict] = []
    for table_path in sorted(tables_path.glob("*.tmdl")):
        content = table_path.read_text(encoding="utf-8")
        match = SOURCE_PATTERN.search(content)
        mapping.append(
            {
                "table": table_path.stem,
                "source_file": match.group(1) if match else None,
                "table_file": table_path.name,
            }
        )
    return mapping
