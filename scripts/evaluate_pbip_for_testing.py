from __future__ import annotations

import argparse
from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from src.common.paths import default_report_definition_path, default_semantic_model_definition_path
from src.validation.pbip_model_inspector import inspect_semantic_model
from src.validation.pbip_report_inspector import inspect_report_definition
from src.validation.scenario_generator import build_measure_validation_candidates


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect PBIP semantic model and report metadata for testing workflows.")
    parser.add_argument("--definition-path", default=str(default_semantic_model_definition_path()))
    parser.add_argument("--report-path", default=str(default_report_definition_path()))
    args = parser.parse_args()

    model_result = inspect_semantic_model(Path(args.definition_path))
    report_result = inspect_report_definition(Path(args.report_path), dataset_name=model_result.dataset_name)
    generated = build_measure_validation_candidates(model_result, report_result)

    print(f"Dataset              : {model_result.dataset_name}")
    print(f"Semantic model path  : {model_result.definition_path}")
    print(f"Measures discovered  : {len(model_result.measures)}")
    print(f"Report path          : {report_result.definition_path}")
    print(f"Report usages found  : {len(report_result.visual_usages)}")
    print(f"Draft scenarios      : {len(generated.cases)}")
    print("High-risk measures   :")
    for measure in model_result.measures:
        if any(flag in {"divide_logic", "calculate_logic", "time_intelligence", "variance_logic"} for flag in measure.risk_flags):
            print(f"- {measure.table_name}[{measure.measure_name}] :: {', '.join(measure.risk_flags)}")
    if report_result.visual_usages:
        print("Report-linked measures:")
        for usage in report_result.visual_usages:
            print(f"- {usage.page_name} / {usage.visual_name} -> {usage.table_name}[{usage.measure_name}] ({usage.usage_role})")
    if generated.issues:
        print("Notes:")
        for issue in generated.issues:
            print(f"- {issue}")


if __name__ == "__main__":
    main()
