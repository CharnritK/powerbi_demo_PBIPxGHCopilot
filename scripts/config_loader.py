from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from src.config.loader import load_config
from src.config.models import RuntimeSettings as AppConfig

__all__ = ["AppConfig", "load_config"]
