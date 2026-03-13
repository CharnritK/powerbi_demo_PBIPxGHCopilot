"""High-level MCP tool helpers."""

from __future__ import annotations

from pathlib import Path

from src.mcp.contracts import ensure_success, response_payload
from src.mcp.server import PowerBIModelingMCPClient


def connect_folder(client: PowerBIModelingMCPClient, definition_folder: Path) -> None:
    payload = response_payload(
        client.call_tool(
            "connection_operations",
            {"request": {"operation": "ConnectFolder", "folderPath": str(definition_folder)}},
        )
    )
    ensure_success(payload, "ConnectFolder")


def list_tables(client: PowerBIModelingMCPClient) -> list[str]:
    payload = response_payload(
        client.call_tool("table_operations", {"request": {"operation": "List"}})
    )
    ensure_success(payload, "Table list")
    return [item["name"] for item in payload.get("data", [])]


def list_measure_names(client: PowerBIModelingMCPClient, table_name: str) -> set[str]:
    payload = response_payload(
        client.call_tool(
            "measure_operations",
            {"request": {"operation": "List", "filter": {"tableNames": [table_name]}}},
        )
    )
    ensure_success(payload, "Measure list")
    return {item["name"] for item in payload.get("data", [])}


def ensure_named_parameter(
    client: PowerBIModelingMCPClient,
    name: str,
    expression: str,
    description: str,
) -> None:
    list_payload = response_payload(
        client.call_tool("named_expression_operations", {"request": {"operation": "List"}})
    )
    ensure_success(list_payload, "Named expression list")
    existing = {item["name"] for item in list_payload.get("data", [])}
    operation = "UpdateParameter" if name in existing else "CreateParameter"
    payload = response_payload(
        client.call_tool(
            "named_expression_operations",
            {
                "request": {
                    "operation": operation,
                    "definitions": [
                        {
                            "name": name,
                            "expression": expression,
                            "kind": "M",
                            "description": description,
                        }
                    ],
                }
            },
        )
    )
    ensure_success(payload, f"{operation} {name}")
