from __future__ import annotations

import json
from pathlib import Path

from src.powerbi.metadata import export_workspace_metadata, normalize_table_rows


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "sample_dataset_metadata.json"


class FakeClient:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def get_datasets_in_group(self, group_id: str) -> list[dict]:
        assert group_id == self.payload["workspace_id"]
        return self.payload["datasets"]

    def get_reports_in_group(self, group_id: str) -> list[dict]:
        assert group_id == self.payload["workspace_id"]
        return self.payload["reports"]


def test_export_workspace_metadata_aggregates_datasets_and_reports() -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    exported = export_workspace_metadata(FakeClient(payload), payload["workspace_id"])
    assert exported["datasets"][0]["name"] == "Sales Model"
    assert exported["reports"][0]["name"] == "Regional Sales"


def test_normalize_table_rows_preserves_keys_as_strings() -> None:
    assert normalize_table_rows([{1: "a", "b": 2}]) == [{"1": "a", "b": 2}]
