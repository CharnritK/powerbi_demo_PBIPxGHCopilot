"""Mock ingest step for demo purposes."""

from pathlib import Path


def main() -> None:
    source = Path("landing/raw_sales_drop")
    target = Path("lakehouse/bronze/sales")
    print(f"[mock] ingesting files from {source} to {target}")


if __name__ == "__main__":
    main()
