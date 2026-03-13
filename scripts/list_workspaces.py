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
from src.powerbi.workspaces import list_workspaces as _list_workspaces


def list_workspaces(auth_mode: str | None = None, top: int = 100) -> pd.DataFrame:
    config = load_config()
    selected_mode = validate_auth_mode(auth_mode or config.auth_mode)
    token = get_access_token(config, auth_mode=selected_mode, use_device_code=config.use_device_code)
    client = PowerBIClient(token, timeout_seconds=config.timeout_seconds)
    frame = pd.DataFrame(_list_workspaces(client, top=top))
    if frame.empty:
        return pd.DataFrame(columns=["id", "name", "isReadOnly", "isOnDedicatedCapacity"])
    return frame


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List Power BI workspaces visible to the caller.")
    parser.add_argument("--auth-mode", choices=["service_principal", "delegated", "delegated_user"], default=None)
    parser.add_argument("--top", type=int, default=100)
    args = parser.parse_args()

    df = list_workspaces(auth_mode=args.auth_mode, top=args.top)
    print(df.to_string(index=False))
