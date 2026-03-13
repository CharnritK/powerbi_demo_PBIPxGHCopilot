from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd

repo_root = Path(__file__).resolve().parents[2]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from src.auth import get_access_token
from src.config.loader import load_settings, require_group_id, validate_auth_mode
from src.powerbi.client import PowerBIClient
from src.powerbi.datasets import list_datasets


def main() -> None:
    parser = argparse.ArgumentParser(description="List datasets in a Power BI workspace.")
    parser.add_argument("--group-id", default=None)
    parser.add_argument("--auth-mode", choices=["delegated", "service_principal"], default=None)
    parser.add_argument("--browser", action="store_true")
    args = parser.parse_args()

    settings = load_settings()
    group_id = require_group_id(args.group_id, settings)
    auth_mode = validate_auth_mode(args.auth_mode or settings.auth_mode)
    token = get_access_token(settings, auth_mode=auth_mode, use_device_code=not args.browser)
    client = PowerBIClient(token, timeout_seconds=settings.request_timeout_seconds)
    frame = pd.DataFrame(list_datasets(client, group_id))
    print(frame.to_string(index=False) if not frame.empty else "No datasets returned.")


if __name__ == "__main__":
    main()
