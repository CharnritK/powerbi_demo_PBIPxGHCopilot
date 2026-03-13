from __future__ import annotations

import argparse
from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from src.common.paths import default_report_definition_path, default_semantic_model_definition_path
from src.validation import merge_validation_cases, read_validation_template, write_validation_template
from src.validation.pbip_model_inspector import inspect_semantic_model
from src.validation.pbip_report_inspector import inspect_report_definition
from src.validation.scenario_generator import build_measure_validation_candidates


def main() -> None:
    parser = argparse.ArgumentParser(description="Populate or update the measure validation template from PBIP metadata.")
    parser.add_argument("--definition-path", default=str(default_semantic_model_definition_path()))
    parser.add_argument("--report-path", default=str(default_report_definition_path()))
    parser.add_argument(
        "--template-path",
        default=str(repo_root / "tests" / "measure-validation" / "templates" / "measure_validation_template.csv"),
    )
    args = parser.parse_args()

    model_result = inspect_semantic_model(Path(args.definition_path))
    report_result = inspect_report_definition(Path(args.report_path), dataset_name=model_result.dataset_name)
    template = read_validation_template(Path(args.template_path))
    generated = build_measure_validation_candidates(model_result, report_result, template.rows)
    merged = merge_validation_cases(template.rows, generated.cases)
    write_validation_template(Path(args.template_path), merged)

    print(f"Template path : {args.template_path}")
    print(f"Existing rows  : {len(template.rows)}")
    print(f"Generated rows : {len(generated.cases)}")
    print(f"Merged rows    : {len(merged)}")
    if generated.issues:
        print("Notes:")
        for issue in generated.issues:
            print(f"- {issue}")


if __name__ == "__main__":
    main()
