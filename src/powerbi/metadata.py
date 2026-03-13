"""Metadata export helpers for workspaces and semantic models."""

from __future__ import annotations

from src.powerbi.client import PowerBIClient
from src.powerbi.datasets import list_datasets
from src.powerbi.reports import list_reports


def export_workspace_metadata(client: PowerBIClient, group_id: str) -> dict:
    return {
        "workspace_id": group_id,
        "datasets": list_datasets(client, group_id),
        "reports": list_reports(client, group_id),
    }


def normalize_table_rows(rows: list[dict]) -> list[dict]:
    return [{str(key): value for key, value in row.items()} for row in rows]
