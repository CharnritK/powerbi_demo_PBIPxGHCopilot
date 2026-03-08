from __future__ import annotations

import argparse
import json
import pandas as pd

from auth_delegated_user import get_delegated_user_token
from auth_service_principal import get_service_principal_token
from config_loader import load_config
from powerbi_client import PowerBIClient


DEFAULT_QUERY = """EVALUATE
TOPN(
    10,
    SUMMARIZECOLUMNS(
        'Dim Region'[Region],
        "Total Sales", [Total Sales],
        "Gross Margin", [Gross Margin]
    ),
    [Total Sales], DESC
)"""


def _extract_first_table(response: dict) -> pd.DataFrame:
    results = response.get("results", [])
    if not results:
        return pd.DataFrame()

    tables = results[0].get("tables", [])
    if not tables:
        return pd.DataFrame()

    rows = tables[0].get("rows", [])
    return pd.DataFrame(rows)


def execute_dax_query(
    workspace_id: str,
    dataset_id: str,
    dax_query: str,
    auth_mode: str | None = None,
    impersonated_user_name: str | None = None,
) -> pd.DataFrame:
    config = load_config()
    selected_mode = auth_mode or config.auth_mode

    if selected_mode == "service_principal":
        token = get_service_principal_token(config)["access_token"]
    elif selected_mode == "delegated_user":
        token = get_delegated_user_token(config)["access_token"]
    else:
        raise ValueError("auth_mode must be 'service_principal' or 'delegated_user'.")

    client = PowerBIClient(token, timeout_seconds=config.timeout_seconds)

    payload = {
        "queries": [{"query": dax_query}],
        "serializerSettings": {"includeNulls": True},
    }
    if impersonated_user_name:
        payload["impersonatedUserName"] = impersonated_user_name

    response = client.post(
        f"/groups/{workspace_id}/datasets/{dataset_id}/executeQueries",
        payload=payload,
    )
    return _extract_first_table(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute a DAX query against a Power BI dataset.")
    parser.add_argument("--workspace-id", required=True)
    parser.add_argument("--dataset-id", required=True)
    parser.add_argument("--auth-mode", choices=["service_principal", "delegated_user"], default=None)
    parser.add_argument("--query-file", default=None)
    parser.add_argument("--impersonated-user-name", default=None)
    args = parser.parse_args()

    if args.query_file:
        with open(args.query_file, "r", encoding="utf-8") as handle:
            dax_query = handle.read()
    else:
        dax_query = DEFAULT_QUERY

    df = execute_dax_query(
        workspace_id=args.workspace_id,
        dataset_id=args.dataset_id,
        dax_query=dax_query,
        auth_mode=args.auth_mode,
        impersonated_user_name=args.impersonated_user_name,
    )
    if df.empty:
        print("No rows returned.")
    else:
        print(df.to_string(index=False))
