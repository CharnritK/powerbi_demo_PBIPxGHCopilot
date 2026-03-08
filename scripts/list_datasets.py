from __future__ import annotations

import argparse
import pandas as pd

from auth_delegated_user import get_delegated_user_token
from auth_service_principal import get_service_principal_token
from config_loader import load_config
from powerbi_client import PowerBIClient


def list_datasets(workspace_id: str, auth_mode: str | None = None) -> pd.DataFrame:
    config = load_config()
    selected_mode = _normalize_auth_mode(auth_mode or config.auth_mode)

    if selected_mode == "service_principal":
        token = get_service_principal_token(config)["access_token"]
    elif selected_mode == "delegated":
        token = get_delegated_user_token(config)["access_token"]
    else:
        raise ValueError("auth_mode must be 'service_principal', 'delegated', or legacy 'delegated_user'.")

    client = PowerBIClient(token, timeout_seconds=config.timeout_seconds)
    response = client.get(f"/groups/{workspace_id}/datasets")
    rows = response.get("value", [])
    frame = pd.DataFrame(rows)
    if frame.empty:
        return pd.DataFrame(columns=["id", "name", "configuredBy", "isRefreshable", "targetStorageMode"])
    keep = [c for c in ["id", "name", "configuredBy", "isRefreshable", "targetStorageMode"] if c in frame.columns]
    return frame[keep].sort_values("name").reset_index(drop=True)


def _normalize_auth_mode(value: str) -> str:
    return "delegated" if value == "delegated_user" else value


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List datasets in a Power BI workspace.")
    parser.add_argument("--workspace-id", required=True)
    parser.add_argument("--auth-mode", choices=["service_principal", "delegated", "delegated_user"], default=None)
    args = parser.parse_args()

    df = list_datasets(workspace_id=args.workspace_id, auth_mode=args.auth_mode)
    print(df.to_string(index=False))
