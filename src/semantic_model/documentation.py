"""Semantic model documentation helpers."""

from __future__ import annotations

from pathlib import Path

from src.semantic_model.lineage import build_source_to_model_mapping
from src.semantic_model.measures import extract_measures_from_tmdl


def generate_measure_catalog(definition_path: Path) -> list[dict]:
    tables_path = definition_path / "tables"
    catalog: list[dict] = []
    for table_path in sorted(tables_path.glob("*.tmdl")):
        for measure in extract_measures_from_tmdl(table_path):
            catalog.append(
                {
                    "table": measure.table_name,
                    "measure": measure.name,
                    "description": measure.description,
                    "source_file": str(measure.source_file.name),
                }
            )
    return catalog


def render_measure_catalog_markdown(catalog: list[dict]) -> str:
    lines = [
        "# Measure Catalog",
        "",
        "| Table | Measure | Description | Source File |",
        "|---|---|---|---|",
    ]
    for item in catalog:
        lines.append(
            f"| {item['table']} | {item['measure']} | {item.get('description') or ''} | {item['source_file']} |"
        )
    return "\n".join(lines) + "\n"


def build_semantic_model_summary(definition_path: Path) -> dict:
    return {
        "measure_catalog": generate_measure_catalog(definition_path),
        "source_to_model_mapping": build_source_to_model_mapping(definition_path),
    }
