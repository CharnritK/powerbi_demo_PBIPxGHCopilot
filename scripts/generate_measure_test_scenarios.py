from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from src.common.paths import default_report_definition_path, default_semantic_model_definition_path
from src.validation.measure_validation_template import write_validation_template
from src.validation.pbip_model_inspector import inspect_semantic_model
from src.validation.pbip_report_inspector import inspect_report_definition
from src.validation.scenario_generator import build_measure_validation_candidates


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate draft measure validation scenarios and coverage CSVs.")
    parser.add_argument("--definition-path", default=str(default_semantic_model_definition_path()))
    parser.add_argument("--report-path", default=str(default_report_definition_path()))
    parser.add_argument(
        "--candidate-path",
        default=str(repo_root / "tests" / "measure-validation" / "generated" / "measure_validation_candidates.csv"),
    )
    parser.add_argument(
        "--coverage-path",
        default=str(repo_root / "tests" / "measure-validation" / "generated" / "report_measure_coverage.csv"),
    )
    args = parser.parse_args()

    model_result = inspect_semantic_model(Path(args.definition_path))
    report_result = inspect_report_definition(Path(args.report_path), dataset_name=model_result.dataset_name)
    generated = build_measure_validation_candidates(model_result, report_result)
    write_validation_template(Path(args.candidate_path), generated.cases)
    _write_csv(Path(args.coverage_path), generated.coverage_rows)

    print(f"Candidate path : {args.candidate_path}")
    print(f"Coverage path  : {args.coverage_path}")
    print(f"Candidates     : {len(generated.cases)}")
    print(f"Coverage rows  : {len(generated.coverage_rows)}")


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else [
        "dataset_name",
        "report_name",
        "page_name",
        "visual_name",
        "visual_type",
        "table_name",
        "measure_name",
        "usage_role",
        "is_high_visibility",
        "priority_hint",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


if __name__ == "__main__":
    main()
