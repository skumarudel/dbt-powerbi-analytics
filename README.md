# dbt-powerbi-analytics

Hospital analytics pipeline: Excel → DuckDB → dbt silver → (gold / Power BI later).

```text
rawdata/*.xlsx
    → Python ingest → database/analytics.duckdb (schema: raw)
    → dbt transform/ → silver.* (department, diagnosis, doctor, …)
    → gold + Power BI (later; optional MS Fabric later)
```

## Folders

| Path | Role |
|------|------|
| `rawdata/` | Source Excel files |
| `database/` | Local DuckDB file (`analytics.duckdb`, gitignored) |
| `src/dbt_powerbi_analytics/ingest/` | Excel → DuckDB loader |
| `transform/` | dbt project (silver models) — see [transform/README.md](transform/README.md) |
| `tests/` | pytest for ingest |
| `notebooks/` | Local exploration only (gitignored) |

## Setup

```bash
uv sync
```

Configure dbt once: point profile `transform` at `database/analytics.duckdb` (see [transform/README.md](transform/README.md)).

## Common commands

```bash
# 1) Load Excel into DuckDB (raw schema)
uv run python -m dbt_powerbi_analytics.ingest

# 2) Test ingest
uv run pytest tests/test_ingest.py -v

# 3) Build silver models
cd transform
uv run dbt debug
uv run dbt run --select dim_department dim_department_hod dim_diagnosis dim_doctor dim_patient dim_treatment dim_payment_method fact_patient_visit
```

## Status

| Stage | Status |
|-------|--------|
| Ingest → `raw.*` | Done |
| Silver `dim_department` | Done |
| Silver `dim_department_hod` | Done |
| Silver `dim_diagnosis` | Done |
| Silver `dim_doctor` | Done |
| Silver `dim_patient` | Done |
| Silver `dim_treatment` | Done |
| Silver `dim_payment_method` | Done |
| Silver `fact_patient_visit` | Done |
| Gold + Power BI | Later |
