"""Repository path helpers."""

from __future__ import annotations

from pathlib import Path


SOLUTION_NAME = "regional-sales-trust-demo"


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_bi_repo_root() -> Path:
    return get_repo_root() / "demo-enterprise" / "bi-repo"


def default_workspace_root() -> Path:
    return default_bi_repo_root() / "powerbi" / "workspaces" / SOLUTION_NAME


def default_pbip_root() -> Path:
    return default_workspace_root() / "pbip"


def default_semantic_model_definition_path() -> Path:
    return default_pbip_root() / "demo_dataset.SemanticModel" / "definition"


def default_report_definition_path() -> Path:
    return default_pbip_root() / "demo_dataset.Report" / "definition"


def default_sample_data_path() -> Path:
    return default_workspace_root() / "assets" / "data"
