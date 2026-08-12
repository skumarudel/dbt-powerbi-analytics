"""Run: ``uv run python -m dbt_powerbi_analytics.ingest``"""

from __future__ import annotations

from dbt_powerbi_analytics.ingest.load import load_raw_to_duckdb


def main() -> None:
    row_counts = load_raw_to_duckdb()
    print("Loaded raw tables into DuckDB:")
    for table, count in sorted(row_counts.items()):
        print(f"  {table}: {count:,} rows")


if __name__ == "__main__":
    main()
