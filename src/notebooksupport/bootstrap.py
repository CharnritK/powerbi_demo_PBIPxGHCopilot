"""Notebook bootstrap helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

from src.auth import get_access_token
from src.config.loader import load_settings
from src.config.models import RuntimeSettings
from src.powerbi.client import PowerBIClient


@dataclass
class NotebookContext:
    repo_root: Path
    settings: RuntimeSettings

    def create_client(self, auth_mode: str | None = None, use_device_code: bool | None = None) -> PowerBIClient:
        token = get_access_token(
            settings=self.settings,
            auth_mode=auth_mode or self.settings.auth_mode,
            use_device_code=use_device_code,
        )
        return PowerBIClient(token, timeout_seconds=self.settings.request_timeout_seconds)


def bootstrap_notebook(repo_root: Path | None = None) -> NotebookContext:
    resolved_root = repo_root or Path.cwd()
    if not (resolved_root / "src").exists():
        resolved_root = resolved_root.parent
    if str(resolved_root) not in sys.path:
        sys.path.insert(0, str(resolved_root))
    settings = load_settings()
    return NotebookContext(repo_root=resolved_root, settings=settings)
