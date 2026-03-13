from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd

repo_root = Path(__file__).resolve().parents[2]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from src.auth import get_access_token
from src.config.loader import load_settings, validate_auth_mode
from src.powerbi.client import PowerBIClient
from src.powerbi.workspaces import list_workspaces


def main() -> None:
    parser = argparse.ArgumentParser(description="List Power BI workspaces visible to the caller.")
    parser.add_argument("--auth-mode", choices=["delegated", "service_principal"], default=None)
    parser.add_argument("--browser", action="store_true")
    parser.add_argument("--top", type=int, default=100)
    args = parser.parse_args()

    settings = load_settings()
    auth_mode = validate_auth_mode(args.auth_mode or settings.auth_mode)
    token = get_access_token(settings, auth_mode=auth_mode, use_device_code=not args.browser)
    client = PowerBIClient(token, timeout_seconds=settings.request_timeout_seconds)
    frame = pd.DataFrame(list_workspaces(client, top=args.top))
    print(frame.to_string(index=False) if not frame.empty else "No workspaces returned.")


if __name__ == "__main__":
    main()
