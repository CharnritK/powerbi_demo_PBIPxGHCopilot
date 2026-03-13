from __future__ import annotations

import argparse
import csv
import io
import json
import re
import subprocess
import time
from pathlib import Path
import sys

repo_root_path = Path(__file__).resolve().parent.parent
if str(repo_root_path) not in sys.path:
    sys.path.insert(0, str(repo_root_path))

from scripts.powerbi_modeling_mcp_common import (
    close_power_bi_desktop_window,
    MCPError,
    PowerBIModelingMCPClient,
    discover_server_binary,
    extract_resources,
    find_power_bi_desktop_exe,
    normalize_windows_slashes,
    parse_json_text_content,
    run_command,
)
from src.common.paths import default_pbip_root, default_sample_data_path, default_semantic_model_definition_path


TABLE_NAMES = [
    "Dim Channel",
    "Dim Region",
    "Dim Product",
    "Fact Sales",
    "Dim Date",
    "Security Region Access",
]

LEGACY_SALES_MEASURE_NAME = "Sales Amount"
CURRENT_SALES_MEASURE_NAME = "Total Sales"

MEASURES = [
    {
        "tableName": "Fact Sales",
        "name": CURRENT_SALES_MEASURE_NAME,
        "expression": "SUM('Fact Sales'[Sales Amount])",
        "formatString": "#,0",
    },
    {
        "tableName": "Fact Sales",
        "name": "Total Cost",
        "expression": "SUM('Fact Sales'[Cost Amount])",
        "formatString": "#,0",
    },
    {
        "tableName": "Fact Sales",
        "name": "Gross Margin",
        "expression": "[Total Sales] - [Total Cost]",
        "formatString": "#,0",
    },
]

EXPECTED_VALUES = {
    "Total Sales": "180000",
    "Total Cost": "99400",
    "Gross Margin": "80600",
}


def response_payload(response: dict) -> dict:
    payloads = parse_json_text_content(response)
    if not payloads:
        raise MCPError(f"Expected JSON text payload, received: {json.dumps(response, indent=2)}")
    return payloads[0]


def ensure_success(payload: dict, context: str) -> None:
    if not payload.get("success"):
        raise MCPError(f"{context} failed.\n{json.dumps(payload, indent=2)}")


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
    names = [item["name"] for item in payload["data"]]
    if names != TABLE_NAMES:
        raise MCPError(f"Unexpected table list: {names}")
    return names


def ensure_parameter(client: PowerBIModelingMCPClient, data_root: Path) -> None:
    list_payload = response_payload(
        client.call_tool("named_expression_operations", {"request": {"operation": "List"}})
    )
    ensure_success(list_payload, "Named expression list")
    existing = {item["name"] for item in list_payload.get("data", [])}
    definition = {
        "name": "DataRootFolder",
        "expression": str(data_root),
        "kind": "M",
        "description": "Local root folder for the demo_dataset CSV files.",
    }
    operation = "UpdateParameter" if "DataRootFolder" in existing else "CreateParameter"
    payload = response_payload(
        client.call_tool(
            "named_expression_operations",
            {"request": {"operation": operation, "definitions": [definition]}},
        )
    )
    ensure_success(payload, f"{operation} DataRootFolder")


def rewrite_partition_expression(expression: str) -> str:
    literal_match = re.search(r'File\.Contents\("([^"]+)"\)', expression)
    parameterized_match = re.search(r'File\.Contents\(DataRootFolder\s*&\s*"([^"]+)"\)', expression)
    if literal_match:
        filename = Path(literal_match.group(1)).name
        return re.sub(
            r'File\.Contents\("([^"]+)"\)',
            f'File.Contents(DataRootFolder & "\\\\{filename}")',
            expression,
            count=1,
        )
    if parameterized_match:
        filename = parameterized_match.group(1).lstrip("\\/")
        return re.sub(
            r'File\.Contents\(DataRootFolder\s*&\s*"([^"]+)"\)',
            f'File.Contents(DataRootFolder & "\\\\{filename}")',
            expression,
            count=1,
        )
    raise MCPError(f"Could not locate File.Contents() in partition expression:\n{expression}")


def update_partitions(client: PowerBIModelingMCPClient) -> None:
    references = [{"tableName": table_name} for table_name in TABLE_NAMES]
    get_payload = response_payload(
        client.call_tool(
            "partition_operations",
            {"request": {"operation": "Get", "references": references}},
        )
    )
    ensure_success(get_payload, "Partition get")
    updates = []
    for result in get_payload["results"]:
        if not result["success"]:
            raise MCPError(json.dumps(result, indent=2))
        data = result["data"]
        updates.append(
            {
                "tableName": data["tableName"],
                "name": data["name"],
                "sourceType": "M",
                "expression": rewrite_partition_expression(data["expression"]),
            }
        )

    update_payload = response_payload(
        client.call_tool(
            "partition_operations",
            {
                "request": {
                    "operation": "Update",
                    "definitions": updates,
                    "options": {"useTransaction": True},
                }
            },
            timeout_seconds=120,
        )
    )
    ensure_success(update_payload, "Partition update")


def list_measure_names(client: PowerBIModelingMCPClient, table_name: str) -> set[str]:
    list_payload = response_payload(
        client.call_tool(
            "measure_operations",
            {"request": {"operation": "List", "filter": {"tableNames": [table_name]}}},
        )
    )
    ensure_success(list_payload, "Measure list")
    return {item["name"] for item in list_payload.get("data", [])}


def normalize_sales_measure_name(client: PowerBIModelingMCPClient, existing: set[str]) -> set[str]:
    if LEGACY_SALES_MEASURE_NAME in existing and CURRENT_SALES_MEASURE_NAME not in existing:
        rename_payload = response_payload(
            client.call_tool(
                "measure_operations",
                {
                    "request": {
                        "operation": "Rename",
                        "renameDefinitions": [
                            {
                                "tableName": "Fact Sales",
                                "currentName": LEGACY_SALES_MEASURE_NAME,
                                "newName": CURRENT_SALES_MEASURE_NAME,
                            }
                        ],
                        "options": {"useTransaction": True},
                    }
                },
                timeout_seconds=120,
            )
        )
        ensure_success(rename_payload, "Measure rename")
        existing = list_measure_names(client, "Fact Sales")

    if LEGACY_SALES_MEASURE_NAME in existing and CURRENT_SALES_MEASURE_NAME in existing:
        delete_payload = response_payload(
            client.call_tool(
                "measure_operations",
                {
                    "request": {
                        "operation": "Delete",
                        "references": [
                            {
                                "tableName": "Fact Sales",
                                "name": LEGACY_SALES_MEASURE_NAME,
                            }
                        ],
                        "options": {"useTransaction": True},
                    }
                },
                timeout_seconds=120,
            )
        )
        ensure_success(delete_payload, "Measure delete")
        existing = list_measure_names(client, "Fact Sales")

    return existing


def upsert_measures(client: PowerBIModelingMCPClient) -> None:
    existing = list_measure_names(client, "Fact Sales")
    existing = normalize_sales_measure_name(client, existing)
    to_create = [measure for measure in MEASURES if measure["name"] not in existing]
    to_update = [measure for measure in MEASURES if measure["name"] in existing]

    if to_create:
        create_payload = response_payload(
            client.call_tool(
                "measure_operations",
                {
                    "request": {
                        "operation": "Create",
                        "definitions": to_create,
                        "options": {"useTransaction": True},
                    }
                },
                timeout_seconds=120,
            )
        )
        ensure_success(create_payload, "Measure create")

    if to_update:
        update_payload = response_payload(
            client.call_tool(
                "measure_operations",
                {
                    "request": {
                        "operation": "Update",
                        "definitions": to_update,
                        "options": {"useTransaction": True},
                    }
                },
                timeout_seconds=120,
            )
        )
        ensure_success(update_payload, "Measure update")


def export_model(client: PowerBIModelingMCPClient, definition_folder: Path) -> None:
    payload = response_payload(
        client.call_tool(
            "database_operations",
            {
                "request": {
                    "operation": "ExportToTmdlFolder",
                    "tmdlFolderPath": str(definition_folder),
                }
            },
            timeout_seconds=120,
        )
    )
    ensure_success(payload, "ExportToTmdlFolder")


def list_local_instances(client: PowerBIModelingMCPClient) -> list[dict]:
    payload = response_payload(
        client.call_tool("connection_operations", {"request": {"operation": "ListLocalInstances"}})
    )
    ensure_success(payload, "ListLocalInstances")
    return payload.get("data", [])


def close_demo_dataset_desktop(client: PowerBIModelingMCPClient) -> None:
    instances = list_local_instances(client)
    for instance in instances:
        if instance.get("parentWindowTitle") == "demo_dataset":
            run_command(["taskkill", "/PID", str(instance["processId"]), "/F"], check=False)


def launch_demo_dataset(pbip_file: Path) -> None:
    desktop_exe = find_power_bi_desktop_exe()
    subprocess.Popen([str(desktop_exe), str(pbip_file)])


def wait_for_demo_dataset_instance(
    client: PowerBIModelingMCPClient, timeout_seconds: int = 180
) -> dict:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        for instance in list_local_instances(client):
            if instance.get("parentWindowTitle") == "demo_dataset":
                return instance
        time.sleep(2)
    raise MCPError("Timed out waiting for Power BI Desktop to open demo_dataset.")


def connect_desktop_instance(client: PowerBIModelingMCPClient, connection_string: str) -> None:
    payload = response_payload(
        client.call_tool(
            "connection_operations",
            {"request": {"operation": "Connect", "connectionString": connection_string}},
        )
    )
    ensure_success(payload, "Connect to Power BI Desktop")


def refresh_import_tables(client: PowerBIModelingMCPClient) -> None:
    refresh_payload = response_payload(
        client.call_tool(
            "partition_operations",
            {
                "request": {
                    "operation": "Refresh",
                    "refreshDefinitions": [
                        {"tableName": table_name, "refreshType": "Full"} for table_name in TABLE_NAMES
                    ],
                    "options": {"useTransaction": True},
                }
            },
            timeout_seconds=240,
        )
    )
    ensure_success(refresh_payload, "Partition refresh")


def run_validation_query(client: PowerBIModelingMCPClient) -> None:
    dax = (
        'EVALUATE ROW("Total Sales", [Total Sales], '
        '"Total Cost", [Total Cost], '
        '"Gross Margin", [Gross Margin])'
    )
    response = client.call_tool(
        "dax_query_operations",
        {"request": {"operation": "Execute", "query": dax, "maxRows": 10}},
        timeout_seconds=120,
    )
    payload = response_payload(response)
    ensure_success(payload, "DAX query execution")
    resources = extract_resources(response)
    if not resources:
        raise MCPError("DAX query result did not include a CSV resource.")
    csv_text = resources[0].get("text", "")
    rows = list(csv.DictReader(io.StringIO(csv_text)))
    if len(rows) != 1:
        raise MCPError(f"Expected exactly one DAX result row, received: {rows}")
    row = rows[0]
    normalized = {key.strip("[]"): value for key, value in row.items()}
    for key, expected in EXPECTED_VALUES.items():
        actual = normalized.get(key)
        if actual != expected:
            raise MCPError(f"Unexpected value for '{key}': expected {expected}, got {actual}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Apply the local Power BI Modeling MCP smoke test to demo_dataset."
    )
    parser.add_argument(
        "--skip-desktop",
        action="store_true",
        help="Skip the Power BI Desktop reopen/refresh/query validation phase.",
    )
    args = parser.parse_args()

    definition_folder = default_semantic_model_definition_path()
    pbip_file = default_pbip_root() / "demo_dataset.pbip"
    data_root = default_sample_data_path()
    server_path = discover_server_binary()

    close_power_bi_desktop_window("demo_dataset")

    with PowerBIModelingMCPClient(server_path, ["--readwrite", "--skip-confirmation"]) as client:
        connect_folder(client, definition_folder)
        list_tables(client)
        ensure_parameter(client, data_root)
        update_partitions(client)
        upsert_measures(client)
        export_model(client, definition_folder)
        close_demo_dataset_desktop(client)

    if args.skip_desktop:
        print("Folder update complete. Desktop validation was skipped.")
        return

    launch_demo_dataset(pbip_file)
    with PowerBIModelingMCPClient(server_path, ["--readwrite", "--skip-confirmation"]) as client:
        instance = wait_for_demo_dataset_instance(client)
        connection_string = normalize_windows_slashes(instance["connectionString"])
        connect_desktop_instance(client, connection_string)
        refresh_import_tables(client)
        run_validation_query(client)

    print("Smoke test complete.")
    print(f"Definition folder : {definition_folder}")
    print(f"PBIP file         : {pbip_file}")
    print(f"DataRootFolder    : {data_root}")
    print("Validated values  : Total Sales=180000, Total Cost=99400, Gross Margin=80600")


if __name__ == "__main__":
    main()
