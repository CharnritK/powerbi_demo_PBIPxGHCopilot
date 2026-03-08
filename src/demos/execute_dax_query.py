from __future__ import annotations

import argparse
import pandas as pd

from src.auth.delegated_auth import acquire_delegated_access_token
from src.auth.service_principal_auth import acquire_service_principal_access_token
from src.clients.powerbi_client import PowerBIClient
from src.utils.config import AppConfig, load_config, require_dataset_id, require_group_id, validate_auth_mode


def main() -> None:
    parser = argparse.ArgumentParser(description="Execute a DAX query against a Power BI dataset.")
    parser.add_argument("--group-id", default=None)
    parser.add_argument("--dataset-id", default=None)
    parser.add_argument("--auth-mode", choices=["delegated", "service_principal"], default=None)
    parser.add_argument("--browser", action="store_true")
    parser.add_argument("--query", default=None)
    parser.add_argument("--impersonated-user-name", default=None)
    args = parser.parse_args()

    config = load_config()
    auth_mode = validate_auth_mode(args.auth_mode or config.auth_mode)
    group_id = require_group_id(args.group_id, config)
    dataset_id = require_dataset_id(args.dataset_id, config)
    access_token = _acquire_token(auth_mode, config, use_device_code=not args.browser)

    client = PowerBIClient(access_token, timeout_seconds=config.request_timeout_seconds)
    query = args.query or config.dax_query
    impersonated_user_name = args.impersonated_user_name or config.impersonated_user_name

    if auth_mode == "service_principal":
        print(
            "Warning: executeQueries with service principal auth is unsupported for datasets with RLS or SSO enabled. If this call fails, switch to delegated auth."
        )

    frame = pd.DataFrame(
        client.execute_queries_in_group(
            group_id=group_id,
            dataset_id=dataset_id,
            dax_query=query,
            impersonated_user_name=impersonated_user_name,
        )
    )
    print(frame.to_string(index=False) if not frame.empty else "No rows returned.")


def _acquire_token(auth_mode: str, config: AppConfig, use_device_code: bool) -> str:
    if auth_mode == "delegated":
        return acquire_delegated_access_token(config, use_device_code=use_device_code)
    return acquire_service_principal_access_token(config)


if __name__ == "__main__":
    main()
