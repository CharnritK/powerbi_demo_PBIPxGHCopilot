from __future__ import annotations

import argparse
from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parents[2]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from src.common.paths import default_semantic_model_definition_path
from src.semantic_model.documentation import generate_measure_catalog, render_measure_catalog_markdown


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Markdown measure catalog from a TMDL definition folder.")
    parser.add_argument("--definition-path", default=str(default_semantic_model_definition_path()))
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    definition_path = Path(args.definition_path)
    markdown = render_measure_catalog_markdown(generate_measure_catalog(definition_path))
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")
        print(f"Wrote measure catalog to {output_path}")
        return
    print(markdown)


if __name__ == "__main__":
    main()
