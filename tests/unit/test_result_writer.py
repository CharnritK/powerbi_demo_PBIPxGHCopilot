from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json

from scripts.helpers.result_writer import create_run_artifact_paths, write_json, write_markdown, write_queries, write_query_results, write_rows_to_csv


def test_create_run_artifact_paths_builds_expected_structure(tmp_path: Path) -> None:
    paths = create_run_artifact_paths(tmp_path, "Sales Semantic Model", datetime(2026, 3, 14, 15, 30, 0))
    assert paths.dataset_root == tmp_path / "sales-semantic-model"
    assert paths.run_root == tmp_path / "sales-semantic-model" / "2026-03-14_153000"
    assert paths.query_results_dir.exists()
    assert paths.report_dir.exists()
    assert paths.screenshots_dir.exists()


def test_result_writer_persists_expected_files(tmp_path: Path) -> None:
    paths = create_run_artifact_paths(tmp_path, "Demo Dataset", datetime(2026, 3, 14, 15, 30, 0))
    write_json(paths.run_summary_path, {"executed": 2})
    write_rows_to_csv(paths.selected_test_cases_path, [{"test_id": "TC001", "measure_name": "Total Sales"}])
    write_queries(paths.executed_queries_path, [{"test_id": "TC001", "measure_name": "Total Sales", "dax_query": "EVALUATE ROW(\"Value\", [Total Sales])"}])
    write_query_results(paths.query_results_dir, [{"test_id": "TC001", "rows": [{"Value": 100}]}])
    write_markdown(paths.report_summary_path, "# Report Summary")

    assert json.loads(paths.run_summary_path.read_text(encoding="utf-8"))["executed"] == 2
    assert "TC001" in paths.selected_test_cases_path.read_text(encoding="utf-8")
    assert "EVALUATE ROW" in paths.executed_queries_path.read_text(encoding="utf-8")
    assert "Value" in (paths.query_results_dir / "TC001.csv").read_text(encoding="utf-8")
    assert "Report Summary" in paths.report_summary_path.read_text(encoding="utf-8")
