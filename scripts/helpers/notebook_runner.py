from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Print the notebook launch command for this repo.")
    parser.add_argument("--notebook", default="notebooks/01_delegated_auth_demo.ipynb")
    args = parser.parse_args()

    notebook_path = Path(args.notebook)
    print(f"python -m notebook {notebook_path}")


if __name__ == "__main__":
    main()
