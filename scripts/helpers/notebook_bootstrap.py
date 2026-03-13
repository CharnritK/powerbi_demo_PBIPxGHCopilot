from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

from src.notebooksupport.bootstrap import NotebookContext, bootstrap_notebook


@dataclass(frozen=True)
class DemoNotebookContext:
    repo_root: Path
    notebook_context: NotebookContext

    def create_client(self, auth_mode: str | None = None, use_device_code: bool | None = None):
        return self.notebook_context.create_client(auth_mode=auth_mode, use_device_code=use_device_code)


def bootstrap_demo_notebook(repo_root: Path | None = None) -> DemoNotebookContext:
    resolved_root = repo_root or Path.cwd()
    if not (resolved_root / "src").exists():
        resolved_root = resolved_root.parent
    if str(resolved_root) not in sys.path:
        sys.path.insert(0, str(resolved_root))
    notebook_context = bootstrap_notebook(resolved_root)
    return DemoNotebookContext(repo_root=resolved_root, notebook_context=notebook_context)
