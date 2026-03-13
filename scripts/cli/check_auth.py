from __future__ import annotations

import argparse
from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parents[2]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from src.auth import get_access_token
from src.config.loader import load_settings, validate_auth_mode


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate local auth configuration and acquire a token.")
    parser.add_argument("--auth-mode", choices=["delegated", "service_principal"], default=None)
    parser.add_argument("--browser", action="store_true", help="Use interactive browser auth for delegated mode.")
    args = parser.parse_args()

    settings = load_settings()
    auth_mode = validate_auth_mode(args.auth_mode or settings.auth_mode)
    get_access_token(settings, auth_mode=auth_mode, use_device_code=not args.browser)
    print("Authentication succeeded.")
    print(settings.redacted_summary())


if __name__ == "__main__":
    main()
