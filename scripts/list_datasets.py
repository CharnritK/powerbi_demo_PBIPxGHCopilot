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
from src.powerbi.datasets import list_datasets as _list_datasets


def list_datasets(workspace_id: str, auth_mode: str | None = None) -> pd.DataFrame:
    config = load_config()
    selected_mode = validate_auth_mode(auth_mode or config.auth_mode)
    token = get_access_token(config, auth_mode=selected_mode, use_device_code=config.use_device_code)
    client = PowerBIClient(token, timeout_seconds=config.timeout_seconds)
    frame = pd.DataFrame(_list_datasets(client, workspace_id))
    if frame.empty:
        return pd.DataFrame(columns=["id", "name", "configuredBy", "isRefreshable", "targetStorageMode"])
    return frame


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List datasets in a Power BI workspace.")
    parser.add_argument("--workspace-id", required=True)
    parser.add_argument("--auth-mode", choices=["service_principal", "delegated", "delegated_user"], default=None)
    args = parser.parse_args()

    df = list_datasets(workspace_id=args.workspace_id, auth_mode=args.auth_mode)
    print(df.to_string(index=False))
