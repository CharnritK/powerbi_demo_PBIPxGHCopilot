from __future__ import annotations

import json
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
    parse_json_text_content,
)
from src.common.paths import default_sample_data_path, default_semantic_model_definition_path


TABLE_RENAMES = {
    "dim_channel": "Dim Channel",
    "dim_region": "Dim Region",
    "dim_product": "Dim Product",
    "fact_sales": "Fact Sales",
    "dim_date": "Dim Date",
    "security_region_access": "Security Region Access",
}

COLUMN_RENAMES = {
    "Dim Channel": {
        "ChannelKey": "Channel Key",
    },
    "Dim Date": {
        "DateKey": "Date Key",
        "MonthNumber": "Month Number",
        "MonthName": "Month Name",
        "YearMonth": "Year Month",
    },
    "Dim Product": {
        "ProductKey": "Product Key",
        "UnitPrice": "Unit Price",
        "UnitCost": "Unit Cost",
    },
    "Dim Region": {
        "RegionKey": "Region Key",
    },
    "Fact Sales": {
        "OrderID": "Order ID",
        "DateKey": "Date Key",
        "RegionKey": "Region Key",
        "ProductKey": "Product Key",
        "ChannelKey": "Channel Key",
        "SalesAmount": "Sales Amount",
        "CostAmount": "Cost Amount",
    },
    "Security Region Access": {
        "UserPrincipalName": "User Principal Name",
    },
}

TABLE_UPDATES = [
    {
        "name": "Dim Channel",
        "description": "Sales channel dimension used to compare performance across distribution channels.",
    },
    {
        "name": "Dim Date",
        "description": "Calendar dimension used for filtering, grouping, and time-intelligence analysis.",
    },
    {
        "name": "Dim Product",
        "description": "Product dimension used for product and category analysis.",
    },
    {
        "name": "Dim Region",
        "description": "Geography dimension used for regional performance and manager coverage analysis.",
    },
    {
        "name": "Fact Sales",
        "description": "Transaction-level sales fact table used for revenue, cost, volume, and margin analysis.",
    },
    {
        "name": "Security Region Access",
        "description": "Optional bridge table for row-level security demonstrations by region.",
        "isHidden": True,
    },
]

COLUMN_UPDATES = [
    {"tableName": "Dim Channel", "name": "Channel Key", "description": "Surrogate key for the sales channel dimension.", "isHidden": True},
    {"tableName": "Dim Channel", "name": "Channel", "description": "Sales channel name used for filtering and comparison."},
    {"tableName": "Dim Date", "name": "Date Key", "description": "Surrogate key for the calendar date.", "isHidden": True},
    {"tableName": "Dim Date", "name": "Date", "description": "Calendar date used for relationships and time intelligence."},
    {"tableName": "Dim Date", "name": "Year", "description": "Calendar year number."},
    {"tableName": "Dim Date", "name": "Quarter", "description": "Calendar quarter label."},
    {"tableName": "Dim Date", "name": "Month Number", "description": "Month number within the calendar year.", "isHidden": True},
    {"tableName": "Dim Date", "name": "Month Name", "description": "Month name used for slicers and labels.", "sortByColumn": "Month Number"},
    {"tableName": "Dim Date", "name": "Year Month", "description": "Calendar month grain used for chronological trend analysis.", "formatString": "MMM yyyy"},
    {"tableName": "Dim Product", "name": "Product Key", "description": "Surrogate key for the product dimension.", "isHidden": True},
    {"tableName": "Dim Product", "name": "Product", "description": "Product name used for analysis."},
    {"tableName": "Dim Product", "name": "Category", "description": "Product category used for grouped analysis."},
    {"tableName": "Dim Product", "name": "Unit Price", "description": "List price per unit in the sample data.", "formatString": "#,0"},
    {"tableName": "Dim Product", "name": "Unit Cost", "description": "Standard cost per unit in the sample data.", "formatString": "#,0"},
    {"tableName": "Dim Region", "name": "Region Key", "description": "Surrogate key for the region dimension.", "isHidden": True},
    {"tableName": "Dim Region", "name": "Region", "description": "Business region name."},
    {"tableName": "Dim Region", "name": "Country", "description": "Country associated with the region."},
    {"tableName": "Dim Region", "name": "Manager", "description": "Regional manager responsible for the region."},
    {"tableName": "Fact Sales", "name": "Order ID", "description": "Unique identifier for each sales order in the sample fact table.", "isHidden": True},
    {"tableName": "Fact Sales", "name": "Date Key", "description": "Surrogate key linking each sale to the date dimension.", "isHidden": True},
    {"tableName": "Fact Sales", "name": "Region Key", "description": "Surrogate key linking each sale to the region dimension.", "isHidden": True},
    {"tableName": "Fact Sales", "name": "Product Key", "description": "Surrogate key linking each sale to the product dimension.", "isHidden": True},
    {"tableName": "Fact Sales", "name": "Channel Key", "description": "Surrogate key linking each sale to the channel dimension.", "isHidden": True},
    {"tableName": "Fact Sales", "name": "Units", "description": "Number of units sold for the transaction.", "isHidden": True, "formatString": "#,0"},
    {"tableName": "Fact Sales", "name": "Sales Amount", "description": "Gross sales amount recorded for the transaction.", "isHidden": True, "formatString": "#,0"},
    {"tableName": "Fact Sales", "name": "Cost Amount", "description": "Total cost amount associated with the transaction.", "isHidden": True, "formatString": "#,0"},
    {
        "tableName": "Security Region Access",
        "name": "User Principal Name",
        "description": "User principal name allowed to access the mapped region in the optional RLS scenario.",
        "isHidden": True,
    },
    {
        "tableName": "Security Region Access",
        "name": "Region",
        "description": "Region granted to the user in the optional RLS scenario.",
        "isHidden": True,
    },
]

LEGACY_SALES_MEASURE_NAME = "Sales Amount"
CURRENT_SALES_MEASURE_NAME = "Total Sales"

MEASURE_DEFINITIONS = [
    {
        "tableName": "Fact Sales",
        "name": CURRENT_SALES_MEASURE_NAME,
        "expression": "SUM('Fact Sales'[Sales Amount])",
        "description": "Total sales amount across the current filter context.",
        "formatString": "#,0",
        "displayFolder": "Key Metrics",
    },
    {
        "tableName": "Fact Sales",
        "name": "Total Cost",
        "expression": "SUM('Fact Sales'[Cost Amount])",
        "description": "Total cost amount across the current filter context.",
        "formatString": "#,0",
        "displayFolder": "Key Metrics",
    },
    {
        "tableName": "Fact Sales",
        "name": "Gross Margin",
        "expression": "[Total Sales] - [Total Cost]",
        "description": "Difference between sales amount and total cost.",
        "formatString": "#,0",
        "displayFolder": "Key Metrics",
    },
    {
        "tableName": "Fact Sales",
        "name": "Gross Margin %",
        "expression": "DIVIDE([Gross Margin], [Total Sales])",
        "description": "Gross margin as a share of sales amount.",
        "formatString": "0.0%",
        "displayFolder": "Key Metrics",
    },
    {
        "tableName": "Fact Sales",
        "name": "Total Units",
        "expression": "SUM('Fact Sales'[Units])",
        "description": "Total units sold in the current filter context.",
        "formatString": "#,0",
        "displayFolder": "Key Metrics",
    },
    {
        "tableName": "Fact Sales",
        "name": "Order Count",
        "expression": "DISTINCTCOUNT('Fact Sales'[Order ID])",
        "description": "Distinct count of orders in the current filter context.",
        "formatString": "#,0",
        "displayFolder": "Key Metrics",
    },
    {
        "tableName": "Fact Sales",
        "name": "Average Order Value",
        "expression": "DIVIDE([Total Sales], [Order Count])",
        "description": "Average sales amount per distinct order.",
        "formatString": "#,0",
        "displayFolder": "Key Metrics",
    },
]


def payload(response: dict) -> dict:
    values = parse_json_text_content(response)
    if not values:
        raise MCPError(f"Unexpected MCP response: {json.dumps(response, indent=2)}")
    return values[0]


def ensure_success(response: dict, context: str) -> dict:
    parsed = payload(response)
    if not parsed.get("success"):
        raise MCPError(f"{context} failed.\n{json.dumps(parsed, indent=2)}")
    return parsed


def list_tables(client: PowerBIModelingMCPClient) -> set[str]:
    parsed = ensure_success(
        client.call_tool("table_operations", {"request": {"operation": "List"}}),
        "List tables",
    )
    return {item["name"] for item in parsed.get("data", [])}


def list_columns(client: PowerBIModelingMCPClient, table_name: str) -> set[str]:
    parsed = ensure_success(
        client.call_tool(
            "column_operations",
            {"request": {"operation": "List", "filter": {"tableNames": [table_name]}}},
        ),
        f"List columns for {table_name}",
    )
    names: set[str] = set()
    for table_entry in parsed.get("data", []):
        for column in table_entry.get("columns", []):
            names.add(column["name"])
    return names


def list_measures(client: PowerBIModelingMCPClient, table_name: str) -> set[str]:
    parsed = ensure_success(
        client.call_tool(
            "measure_operations",
            {"request": {"operation": "List", "filter": {"tableNames": [table_name]}}},
        ),
        f"List measures for {table_name}",
    )
    return {item["name"] for item in parsed.get("data", [])}


def normalize_sales_measure_name(client: PowerBIModelingMCPClient, existing: set[str]) -> set[str]:
    if LEGACY_SALES_MEASURE_NAME in existing and CURRENT_SALES_MEASURE_NAME not in existing:
        ensure_success(
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
            ),
            "Rename legacy sales measure",
        )
        existing = list_measures(client, "Fact Sales")

    if LEGACY_SALES_MEASURE_NAME in existing and CURRENT_SALES_MEASURE_NAME in existing:
        ensure_success(
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
            ),
            "Delete legacy sales measure",
        )
        existing = list_measures(client, "Fact Sales")

    return existing


def rename_tables(client: PowerBIModelingMCPClient) -> None:
    current_tables = list_tables(client)
    rename_definitions = []
    for old_name, new_name in TABLE_RENAMES.items():
        if old_name in current_tables and new_name not in current_tables:
            rename_definitions.append({"currentName": old_name, "newName": new_name})
    if not rename_definitions:
        return
    ensure_success(
        client.call_tool(
            "table_operations",
            {
                "request": {
                    "operation": "Rename",
                    "renameDefinitions": rename_definitions,
                    "options": {"useTransaction": True},
                }
            },
            timeout_seconds=120,
        ),
        "Rename tables",
    )


def rename_columns(client: PowerBIModelingMCPClient) -> None:
    for table_name, renames in COLUMN_RENAMES.items():
        current_columns = list_columns(client, table_name)
        rename_definitions = []
        for old_name, new_name in renames.items():
            if old_name in current_columns and new_name not in current_columns:
                rename_definitions.append(
                    {"tableName": table_name, "currentName": old_name, "newName": new_name}
                )
        if not rename_definitions:
            continue
        ensure_success(
            client.call_tool(
                "column_operations",
                {
                    "request": {
                        "operation": "Rename",
                        "renameDefinitions": rename_definitions,
                        "options": {"useTransaction": True},
                    }
                },
                timeout_seconds=120,
            ),
            f"Rename columns for {table_name}",
        )


def update_parameter_description(client: PowerBIModelingMCPClient, data_root: Path) -> None:
    ensure_success(
        client.call_tool(
            "named_expression_operations",
            {
                "request": {
                    "operation": "UpdateParameter",
                    "definitions": [
                        {
                            "name": "DataRootFolder",
                            "expression": str(data_root),
                            "kind": "M",
                            "description": "Root folder for the demo_dataset CSV source files.",
                        }
                    ],
                }
            },
        ),
        "Update DataRootFolder parameter",
    )


def update_tables(client: PowerBIModelingMCPClient) -> None:
    ensure_success(
        client.call_tool(
            "table_operations",
            {
                "request": {
                    "operation": "Update",
                    "definitions": TABLE_UPDATES,
                    "options": {"useTransaction": True},
                }
            },
            timeout_seconds=120,
        ),
        "Update table properties",
    )


def update_columns(client: PowerBIModelingMCPClient) -> None:
    ensure_success(
        client.call_tool(
            "column_operations",
            {
                "request": {
                    "operation": "Update",
                    "definitions": COLUMN_UPDATES,
                    "options": {"useTransaction": True},
                }
            },
            timeout_seconds=120,
        ),
        "Update column properties",
    )


def mark_date_table(client: PowerBIModelingMCPClient) -> None:
    ensure_success(
        client.call_tool(
            "table_operations",
            {
                "request": {
                    "operation": "MarkAsDateTable",
                    "markAsDateTableDefinitions": [
                        {"tableName": "Dim Date", "dateColumnName": "Date"}
                    ],
                    "options": {"useTransaction": True},
                }
            },
        ),
        "Mark Dim Date as date table",
    )


def upsert_measures(client: PowerBIModelingMCPClient) -> None:
    existing_measures = normalize_sales_measure_name(client, list_measures(client, "Fact Sales"))
    to_create = [definition for definition in MEASURE_DEFINITIONS if definition["name"] not in existing_measures]
    to_update = [definition for definition in MEASURE_DEFINITIONS if definition["name"] in existing_measures]

    if to_create:
        ensure_success(
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
            ),
            "Create measures",
        )

    if to_update:
        ensure_success(
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
            ),
            "Update measures",
        )


def export_model(client: PowerBIModelingMCPClient, definition_folder: Path) -> None:
    ensure_success(
        client.call_tool(
            "database_operations",
            {
                "request": {
                    "operation": "ExportToTmdlFolder",
                    "tmdlFolderPath": str(definition_folder),
                }
            },
            timeout_seconds=120,
        ),
        "Export model to TMDL",
    )


def main() -> None:
    definition_folder = default_semantic_model_definition_path()
    data_root = default_sample_data_path()
    server_path = discover_server_binary()

    close_power_bi_desktop_window("demo_dataset")

    with PowerBIModelingMCPClient(server_path, ["--readwrite", "--skip-confirmation"]) as client:
        ensure_success(
            client.call_tool(
                "connection_operations",
                {
                    "request": {
                        "operation": "ConnectFolder",
                        "folderPath": str(definition_folder),
                    }
                },
            ),
            "Connect folder",
        )
        update_parameter_description(client, data_root)
        rename_tables(client)
        rename_columns(client)
        update_tables(client)
        update_columns(client)
        mark_date_table(client)
        upsert_measures(client)
        export_model(client, definition_folder)

    print("Applied semantic model best-practice updates to demo_dataset.")
    print(f"Definition folder : {definition_folder}")
    print("Highlights        : friendly names, descriptions, hidden technical fields, date table, core measures.")


if __name__ == "__main__":
    main()
