from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parents[2]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from src.auth import get_access_token
from src.config.loader import load_settings, require_group_id, validate_auth_mode
from src.powerbi.client import PowerBIClient
from src.powerbi.metadata import export_workspace_metadata


def main() -> None:
    parser = argparse.ArgumentParser(description="Export Power BI workspace metadata as JSON.")
    parser.add_argument("--group-id", default=None)
    parser.add_argument("--auth-mode", choices=["delegated", "service_principal"], default=None)
    parser.add_argument("--browser", action="store_true")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    settings = load_settings()
    group_id = require_group_id(args.group_id, settings)
    auth_mode = validate_auth_mode(args.auth_mode or settings.auth_mode)
    token = get_access_token(settings, auth_mode=auth_mode, use_device_code=not args.browser)
    client = PowerBIClient(token, timeout_seconds=settings.request_timeout_seconds)
    payload = export_workspace_metadata(client, group_id)
    text = json.dumps(payload, indent=2)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")
        print(f"Wrote metadata to {output_path}")
        return
    print(text)


if __name__ == "__main__":
    main()
