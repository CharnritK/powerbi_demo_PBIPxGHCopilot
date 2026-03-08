from __future__ import annotations

import argparse
import pandas as pd

from auth_delegated_user import get_delegated_user_token
from auth_service_principal import get_service_principal_token
from config_loader import load_config
from powerbi_client import PowerBIClient


def list_workspaces(auth_mode: str | None = None, top: int = 100) -> pd.DataFrame:
    config = load_config()
    selected_mode = _normalize_auth_mode(auth_mode or config.auth_mode)

    if selected_mode == "service_principal":
        token = get_service_principal_token(config)["access_token"]
    elif selected_mode == "delegated":
        token = get_delegated_user_token(config)["access_token"]
    else:
        raise ValueError("auth_mode must be 'service_principal', 'delegated', or legacy 'delegated_user'.")

    client = PowerBIClient(token, timeout_seconds=config.timeout_seconds)
    response = client.get("/groups", params={"$top": top})

    rows = response.get("value", [])
    frame = pd.DataFrame(rows)
    if frame.empty:
        return pd.DataFrame(columns=["id", "name", "isReadOnly", "isOnDedicatedCapacity"])
    keep = [c for c in ["id", "name", "isReadOnly", "isOnDedicatedCapacity"] if c in frame.columns]
    return frame[keep].sort_values("name").reset_index(drop=True)


def _normalize_auth_mode(value: str) -> str:
    return "delegated" if value == "delegated_user" else value


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List Power BI workspaces visible to the caller.")
    parser.add_argument("--auth-mode", choices=["service_principal", "delegated", "delegated_user"], default=None)
    parser.add_argument("--top", type=int, default=100)
    args = parser.parse_args()

    df = list_workspaces(auth_mode=args.auth_mode, top=args.top)
    print(df.to_string(index=False))
