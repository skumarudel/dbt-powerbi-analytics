# dbt-powerbi-analytics

Stage 1 for now: load Excel into DuckDB. dbt (bronze/silver/gold) comes later.

## What this stage does

```text
rawdata/*.xlsx  →  Python ingest  →  database/analytics.duckdb (schema: raw)
```

## Folders

| Path | Role |
|------|------|
| `rawdata/` | Source Excel files |
| `database/` | Local DuckDB file (gitignored) |
| `src/dbt_powerbi_analytics/ingest/` | Excel → DuckDB loader |
| `tests/` | pytest for ingest |

## Commands

```bash
# install
uv sync

# load Excel into DuckDB
uv run python -m dbt_powerbi_analytics.ingest

# test ingest before push
uv run pytest tests/test_ingest.py -v
```
