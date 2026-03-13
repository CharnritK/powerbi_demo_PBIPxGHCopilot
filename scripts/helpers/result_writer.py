from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Any


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    return cleaned.strip("-") or "unnamed"


@dataclass(frozen=True)
class RunArtifactPaths:
    dataset_root: Path
    run_root: Path
    query_results_dir: Path
    report_dir: Path
    screenshots_dir: Path
    run_summary_path: Path
    selected_test_cases_path: Path
    executed_queries_path: Path
    report_metadata_path: Path
    report_summary_path: Path


def create_run_artifact_paths(base_dir: Path, dataset_name: str, run_timestamp: datetime | None = None) -> RunArtifactPaths:
    timestamp = (run_timestamp or datetime.now()).strftime("%Y-%m-%d_%H%M%S")
    dataset_root = base_dir / slugify(dataset_name)
    run_root = dataset_root / timestamp
    query_results_dir = run_root / "query_results"
    report_dir = run_root / "report"
    screenshots_dir = run_root / "screenshots"
    for path in (query_results_dir, report_dir, screenshots_dir):
        path.mkdir(parents=True, exist_ok=True)
    return RunArtifactPaths(
        dataset_root=dataset_root,
        run_root=run_root,
        query_results_dir=query_results_dir,
        report_dir=report_dir,
        screenshots_dir=screenshots_dir,
        run_summary_path=run_root / "run_summary.json",
        selected_test_cases_path=run_root / "selected_test_cases.csv",
        executed_queries_path=run_root / "executed_queries.sql.txt",
        report_metadata_path=report_dir / "report_metadata.json",
        report_summary_path=report_dir / "report_summary.md",
    )


def write_json(path: Path, payload: dict[str, Any] | list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_rows_to_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        if fieldnames:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow({key: _stringify(value) for key, value in row.items()})
        else:
            handle.write("")


def write_queries(path: Path, queries: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    blocks: list[str] = []
    for query in queries:
        blocks.append(f"-- {query['test_id']} :: {query['measure_name']}")
        blocks.append(query["dax_query"])
        blocks.append("")
    path.write_text("\n".join(blocks).rstrip() + "\n", encoding="utf-8")


def write_query_results(directory: Path, results: list[dict[str, Any]]) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for result in results:
        rows = result.get("rows", [])
        file_path = directory / f"{result['test_id']}.csv"
        write_rows_to_csv(file_path, rows if isinstance(rows, list) else [])


def write_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    return str(value)
