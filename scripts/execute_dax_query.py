from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from src.auth import get_access_token
from src.config.loader import load_config, validate_auth_mode
from src.powerbi.client import PowerBIClient
from src.powerbi.execute_queries import DEFAULT_QUERY, execute_dax_query as _execute_dax_query


def execute_dax_query(
    workspace_id: str,
    dataset_id: str,
    dax_query: str,
    auth_mode: str | None = None,
    impersonated_user_name: str | None = None,
) -> pd.DataFrame:
    config = load_config()
    selected_mode = validate_auth_mode(auth_mode or config.auth_mode)
    token = get_access_token(config, auth_mode=selected_mode, use_device_code=config.use_device_code)
    client = PowerBIClient(token, timeout_seconds=config.timeout_seconds)
    rows = _execute_dax_query(
        client=client,
        group_id=workspace_id,
        dataset_id=dataset_id,
        dax_query=dax_query,
        impersonated_user_name=impersonated_user_name,
    )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute a DAX query against a Power BI dataset.")
    parser.add_argument("--workspace-id", required=True)
    parser.add_argument("--dataset-id", required=True)
    parser.add_argument("--auth-mode", choices=["service_principal", "delegated", "delegated_user"], default=None)
    parser.add_argument("--query-file", default=None)
    parser.add_argument("--impersonated-user-name", default=None)
    args = parser.parse_args()

    dax_query = Path(args.query_file).read_text(encoding="utf-8") if args.query_file else DEFAULT_QUERY
    df = execute_dax_query(
        workspace_id=args.workspace_id,
        dataset_id=args.dataset_id,
        dax_query=dax_query,
        auth_mode=args.auth_mode,
        impersonated_user_name=args.impersonated_user_name,
    )
    print(df.to_string(index=False) if not df.empty else "No rows returned.")
