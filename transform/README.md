# transform (dbt)

dbt project that builds **silver** tables in DuckDB from the `raw` schema created by Python ingest.

```text
rawdata/*.xlsx
    → Python ingest → raw.* (DuckDB)
    → dbt (this folder) → silver.* (DuckDB)
```

The hospital dashboard in [`powerbi/`](../powerbi/README.md) was built inside Power BI. This dbt project checks whether that cleaning and modeling can be automated. Gold aggregations stay in the report, so this folder has no gold models.

Bronze is skipped: ingest landing tables in `raw` are treated as the unchanged source layer.

## Prerequisites

1. Install deps from the repo root: `uv sync`
2. Load Excel into DuckDB:

```bash
cd ..   # repo root
uv run python -m dbt_powerbi_analytics.ingest
```

3. Configure a dbt profile that points at `database/analytics.duckdb`  
   (usually `~/.dbt/profiles.yml`, profile name `transform`).

Example profile output:

```yaml
transform:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: /FULL/PATH/TO/dbt-powerbi-analytics/database/analytics.duckdb
      threads: 4
      schema: main
```

Check the connection from this folder:

```bash
uv run dbt debug
```

## Layout

| Path | Role |
|------|------|
| `models/sources.yml` | Declares existing `raw.*` tables |
| `models/silver/` | Cleaning / standardization models |
| `macros/generate_schema_name.sql` | Keeps schema name as `silver` (not `main_silver`) |
| `dbt_project.yml` | Project config (`silver` → table in schema `silver`) |

## Silver models (current)

| Model | Source | What it does |
|-------|--------|----------------|
| `dim_department` | `raw.dim_department` | Keep ID/name/category; strip `Dept-` prefix; drop null/blank rows; dedupe on `DepartmentID` |
| `dim_department_hod` | `raw.dept_hod` | Trim; one HOD name per `DepartmentID` |
| `dim_diagnosis` | `raw.dim_diagnosis` | Light trim; drop blank keys (source is already clean) |
| `dim_treatment` | `raw.dim_treatment` | Light trim; drop blank keys (source is already clean) |
| `dim_payment_method` | `raw.dim_payment_method` | Collapse 72 transaction rows to 4 methods via GROUP BY; keep ID + name |
| `dim_doctor` | `raw.dim_doctor` | Drop empty rows; normalize `DoctorID` (`D-17-001` → `D001`); add `FullName`; trim text fields |
| `dim_patient` | `raw.dim_patient` | Drop NaN rows; `FullName` only (initcap; drop First/Last); `DOB` as date; `M`/`F` → Male/Female; City/State/Country (drop combined location) |
| `fact_patient_visit` | `raw.patient_visits_*` | Union four year tables; trim keys; dates as DATE; `VisitTime` to TIME (AM/PM + 24h); drop `DepartmentCategory` |

## Commands

Run from the `transform/` directory:

```bash
# connection check
uv run dbt debug

# build one model
uv run dbt run --select dim_department

# build the current silver models
uv run dbt run --select dim_department dim_department_hod dim_diagnosis dim_doctor dim_patient dim_treatment dim_payment_method fact_patient_visit

# build everything under models/silver
uv run dbt run --select path:models/silver
```

Verify in DuckDB (from repo root):

```bash
uv run python -c "import duckdb; c=duckdb.connect('database/analytics.duckdb', read_only=True); print(c.sql('show tables from silver').df())"
```

## Troubleshooting

**DuckDB lock error** while running dbt: another process (often a Jupyter notebook) has `database/analytics.duckdb` open.

- Restart/close the notebook kernel, or  
- `lsof database/analytics.duckdb` then `kill <PID>`  
- Prefer `read_only=True` in notebooks when only exploring  

## Resources

- [dbt docs](https://docs.getdbt.com/docs/introduction)
- [dbt-duckdb adapter](https://github.com/duckdb/dbt-duckdb)
