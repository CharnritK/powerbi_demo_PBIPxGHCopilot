"""Dataset service helpers."""

from __future__ import annotations

from src.powerbi.client import PowerBIClient


def list_datasets(client: PowerBIClient, group_id: str) -> list[dict]:
    rows = client.get_datasets_in_group(group_id)
    return sorted(rows, key=lambda item: (item.get("name") or "").lower())
