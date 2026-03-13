from __future__ import annotations

import argparse
from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parents[2]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from src.common.paths import default_semantic_model_definition_path
from src.semantic_model.validation import validate_tmdl_definition


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a TMDL semantic model folder.")
    parser.add_argument("definition_path", nargs="?", default=str(default_semantic_model_definition_path()))
    args = parser.parse_args()

    report = validate_tmdl_definition(Path(args.definition_path))
    print(f"Definition path : {report.definition_path}")
    print(f"Tables          : {report.table_count}")
    print(f"Columns         : {report.column_count}")
    print(f"Measures        : {report.measure_count}")
    if report.issues:
        print("Issues:")
        for issue in report.issues:
            print(f"- {issue}")
        raise SystemExit(1)
    print("Validation passed.")


if __name__ == "__main__":
    main()
