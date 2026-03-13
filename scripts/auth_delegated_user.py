from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from src.auth.delegated_user import get_delegated_user_token

__all__ = ["get_delegated_user_token"]
