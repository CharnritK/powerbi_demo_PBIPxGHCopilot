from __future__ import annotations

import argparse
import pandas as pd

from src.auth.delegated_auth import acquire_delegated_access_token
from src.auth.service_principal_auth import acquire_service_principal_access_token
from src.clients.powerbi_client import PowerBIClient
from src.utils.config import AppConfig, load_config, validate_auth_mode


def main() -> None:
    parser = argparse.ArgumentParser(description="List Power BI workspaces visible to the caller.")
    parser.add_argument("--auth-mode", choices=["delegated", "service_principal"], default=None)
    parser.add_argument("--browser", action="store_true", help="Use interactive browser auth instead of device code for delegated auth.")
    args = parser.parse_args()

    config = load_config()
    auth_mode = validate_auth_mode(args.auth_mode or config.auth_mode)
    access_token = _acquire_token(auth_mode, config, use_device_code=not args.browser)

    client = PowerBIClient(access_token, timeout_seconds=config.request_timeout_seconds)
    frame = pd.DataFrame(client.get_groups())
    print(frame.to_string(index=False) if not frame.empty else "No workspaces returned.")


def _acquire_token(auth_mode: str, config: AppConfig, use_device_code: bool) -> str:
    if auth_mode == "delegated":
        return acquire_delegated_access_token(config, use_device_code=use_device_code)
    return acquire_service_principal_access_token(config)


if __name__ == "__main__":
    main()

