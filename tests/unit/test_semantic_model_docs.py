from __future__ import annotations

import json
from pathlib import Path

from src.semantic_model.documentation import generate_measure_catalog
from src.semantic_model.lineage import build_source_to_model_mapping
from src.semantic_model.validation import validate_tmdl_definition


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFINITION = REPO_ROOT / "powerbi" / "workspaces" / "regional-sales-trust-demo" / "pbip" / "demo_dataset.SemanticModel" / "definition"
FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "sample_measure_catalog.json"


def test_generate_measure_catalog_contains_expected_measures() -> None:
    catalog = generate_measure_catalog(DEFINITION)
    expected = json.loads(FIXTURE.read_text(encoding="utf-8"))
    names = {(item["table"], item["measure"]) for item in catalog}
    for row in expected:
        assert (row["table"], row["measure"]) in names


def test_source_to_model_mapping_contains_fact_sales_file() -> None:
    mapping = build_source_to_model_mapping(DEFINITION)
    assert any(item["table"] == "Fact Sales" and item["source_file"] == "fact_sales.csv" for item in mapping)


def test_validate_tmdl_definition_passes_for_committed_model() -> None:
    report = validate_tmdl_definition(DEFINITION)
    assert report.is_valid
    assert report.measure_count >= 3
