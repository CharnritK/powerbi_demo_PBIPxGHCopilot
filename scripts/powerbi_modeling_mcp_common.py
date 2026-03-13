from pathlib import Path
import sys

repo_root_path = Path(__file__).resolve().parent.parent
if str(repo_root_path) not in sys.path:
    sys.path.insert(0, str(repo_root_path))

from src.common.errors import MCPError
from src.common.paths import get_repo_root
from src.mcp.contracts import extract_resources, parse_json_text_content
from src.mcp.safety import (
    close_power_bi_desktop_window,
    find_power_bi_desktop_exe,
    normalize_windows_slashes,
    run_command,
)
from src.mcp.server import PowerBIModelingMCPClient, discover_server_binary


def repo_root() -> Path:
    return get_repo_root()


__all__ = [
    "MCPError",
    "PowerBIModelingMCPClient",
    "close_power_bi_desktop_window",
    "discover_server_binary",
    "extract_resources",
    "find_power_bi_desktop_exe",
    "normalize_windows_slashes",
    "parse_json_text_content",
    "repo_root",
    "run_command",
]
