# dbt-powerbi-analytics

Hospital analytics pipeline on DuckDB with dbt medallion layers, ready for Power BI.

## Pipeline

```text
rawdata/ (Excel)
    → Python ingest (src/dbt_powerbi_analytics/ingest/)
    → database/analytics.duckdb
    → dbt transform/ (bronze → silver → gold)
    → Power BI (Windows, later)
```

## Folder roles

| Path | Role |
|------|------|
| `rawdata/` | Source Excel files (do not transform in place) |
| `database/` | Local DuckDB file (`analytics.duckdb`, gitignored) |
| `src/dbt_powerbi_analytics/` | Python package; ingest lives under `ingest/` |
| `transform/` | dbt project: bronze / silver / gold models |

## Mac workflow (high level)

1. Keep Excel files in `rawdata/`:
   - `Hospital_Dataset.xlsx`
   - `Department HOD.xlsx`
2. Ingest into DuckDB at `database/analytics.duckdb` (script to be added next).
3. Configure dbt: copy `transform/profiles.yml.example` to `transform/profiles.yml` (or `~/.dbt/profiles.yml`).
4. From `transform/`, run dbt once models exist: `dbt run`.
5. On Windows later, connect Power BI to the gold tables in DuckDB (or exported extracts).

## Setup

```bash
uv sync
```

Dependencies are declared in `pyproject.toml` (`duckdb`, `pandas`, `openpyxl`, `dbt-duckdb`).

## Status

Project layout is scaffolded. Ingestion scripts and dbt models are not implemented yet.
