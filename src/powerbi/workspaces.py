"""Workspace service helpers."""

from __future__ import annotations

from src.powerbi.client import PowerBIClient


def list_workspaces(client: PowerBIClient, top: int = 100) -> list[dict]:
    rows = client.get_groups(top=top)
    return sorted(rows, key=lambda item: (item.get("name") or "").lower())
