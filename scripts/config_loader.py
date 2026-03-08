from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv


@dataclass
class AppConfig:
    tenant_id: str
    client_id: str
    client_secret: Optional[str]
    redirect_uri: Optional[str]
    auth_mode: str
    scope: str
    workspace_id: Optional[str]
    dataset_id: Optional[str]
    timeout_seconds: int = 60
    log_level: str = "INFO"


def _setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def load_config(env_path: str | None = None, settings_json_path: str | None = None) -> AppConfig:
    if env_path:
        load_dotenv(env_path)
    else:
        load_dotenv()

    settings: Dict[str, Any] = {}
    if settings_json_path:
        settings_path = Path(settings_json_path)
        if settings_path.exists():
            settings = json.loads(settings_path.read_text(encoding="utf-8"))

    def read(name: str, default: Any = None) -> Any:
        return os.getenv(name, settings.get(name, default))

    config = AppConfig(
        tenant_id=read("PBI_TENANT_ID", ""),
        client_id=read("PBI_CLIENT_ID", ""),
        client_secret=read("PBI_CLIENT_SECRET"),
        redirect_uri=read("PBI_REDIRECT_URI"),
        auth_mode=read("PBI_AUTH_MODE", "service_principal"),
        scope=read("PBI_SCOPE", "https://analysis.windows.net/powerbi/api/.default"),
        workspace_id=read("PBI_WORKSPACE_ID"),
        dataset_id=read("PBI_DATASET_ID"),
        timeout_seconds=int(read("PBI_TIMEOUT_SECONDS", 60)),
        log_level=read("PBI_LOG_LEVEL", "INFO"),
    )

    _setup_logging(config.log_level)

    missing = []
    if not config.tenant_id:
        missing.append("PBI_TENANT_ID")
    if not config.client_id:
        missing.append("PBI_CLIENT_ID")

    if missing:
        raise ValueError(f"Missing required configuration: {', '.join(missing)}")

    return config
