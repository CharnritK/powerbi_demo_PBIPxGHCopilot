"""Helpers for interpreting Power BI Modeling MCP responses."""

from __future__ import annotations

import json
from typing import Any

from src.common.errors import MCPError


def parse_json_text_content(response: dict[str, Any]) -> list[dict[str, Any]]:
    contents = response.get("result", {}).get("content", [])
    parsed: list[dict[str, Any]] = []
    for item in contents:
        if item.get("type") != "text":
            continue
        parsed.append(json.loads(item["text"]))
    return parsed


def extract_resources(response: dict[str, Any]) -> list[dict[str, Any]]:
    contents = response.get("result", {}).get("content", [])
    return [item["resource"] for item in contents if item.get("type") == "resource"]


def response_payload(response: dict[str, Any]) -> dict[str, Any]:
    payloads = parse_json_text_content(response)
    if not payloads:
        raise MCPError(f"Expected JSON text payload, received: {json.dumps(response, indent=2)}")
    return payloads[0]


def ensure_success(payload: dict[str, Any], context: str) -> None:
    if not payload.get("success"):
        raise MCPError(f"{context} failed.\n{json.dumps(payload, indent=2)}")
