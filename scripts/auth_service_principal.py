from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from src.auth.service_principal import get_service_principal_token

__all__ = ["get_service_principal_token"]
