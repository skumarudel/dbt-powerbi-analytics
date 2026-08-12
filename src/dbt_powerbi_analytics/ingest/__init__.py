"""Excel → DuckDB ingestion (landing zone for bronze)."""

from dbt_powerbi_analytics.ingest.load import load_raw_to_duckdb

__all__ = ["load_raw_to_duckdb"]
