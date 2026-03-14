from __future__ import annotations

import json
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_NOTEBOOKS = [
    REPO_ROOT / "notebooks" / "01_delegated_auth_demo.ipynb",
    REPO_ROOT / "notebooks" / "02_service_principal_demo.ipynb",
    REPO_ROOT / "notebooks" / "03_measure_validation_showcase.ipynb",
]


@pytest.mark.parametrize("notebook_path", CANONICAL_NOTEBOOKS, ids=lambda path: path.name)
def test_canonical_notebook_code_cells_compile(notebook_path: Path) -> None:
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))

    for index, cell in enumerate(notebook.get("cells", []), start=1):
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source", "")
        if isinstance(source, list):
            source = "".join(source)
        compile(source, f"{notebook_path.name}::cell_{index}", "exec")


@pytest.mark.parametrize("notebook_path", CANONICAL_NOTEBOOKS, ids=lambda path: path.name)
def test_canonical_notebook_cells_have_ids(notebook_path: Path) -> None:
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))

    missing_ids = [
        index
        for index, cell in enumerate(notebook.get("cells", []), start=1)
        if not cell.get("id")
    ]

    assert not missing_ids, f"{notebook_path.name} is missing cell ids at positions: {missing_ids}"
