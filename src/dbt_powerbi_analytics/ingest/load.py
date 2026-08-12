"""Load Excel sheets into DuckDB ``raw`` schema (no business transforms)."""

from __future__ import annotations

import re
from pathlib import Path

import duckdb
import pandas as pd

from dbt_powerbi_analytics.ingest.headers import infer_header_row

# Project paths (repo root = parents[3] from this file:
# .../src/dbt_powerbi_analytics/ingest/load.py)
REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_RAW_DIR = REPO_ROOT / "rawdata"
DEFAULT_DB_PATH = REPO_ROOT / "database" / "analytics.duckdb"

HOSPITAL_FILE = "Hospital_Dataset.xlsx"
DEPARTMENT_FILE = "Department HOD.xlsx"

# Sheets we intentionally load (skip Excel filter-cache sheets).
HOSPITAL_SHEETS = [
    "PatientVisits_2020_2021",
    "PatientVisits_2022_2023",
    "PatientVisits_2024",
    "PatientVisits_2025",
    "Dim_Patient",
    "Dim_Doctor",
    "Dim_Department",
    "Dim_Diagnosis",
    "Dim_Treatment",
    "Dim_PaymentMethod",
]

DEPARTMENT_SHEETS = [
    "Dept_HOD",
]

RAW_SCHEMA = "raw"


def sheet_to_table_name(sheet_name: str) -> str:
    """Convert Excel sheet name to a snake_case DuckDB table name."""
    name = sheet_name.strip()
    name = re.sub(r"[\s\-]+", "_", name)
    # PatientVisits -> Patient_Visits; leave existing underscores alone
    name = re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", name)
    name = re.sub(r"_+", "_", name)
    return name.lower().strip("_")


def read_sheet(path: Path, sheet_name: str) -> pd.DataFrame:
    """Read one Excel sheet with an inferred header row."""
    header = infer_header_row(path, sheet_name)
    return pd.read_excel(path, sheet_name=sheet_name, header=header)


def load_raw_to_duckdb(
    raw_dir: Path | str | None = None,
    db_path: Path | str | None = None,
) -> dict[str, int]:
    """Load all configured Excel sheets into DuckDB schema ``raw``.

    Returns a mapping of fully-qualified table name -> row count.
    """
    raw_dir = Path(raw_dir) if raw_dir is not None else DEFAULT_RAW_DIR
    db_path = Path(db_path) if db_path is not None else DEFAULT_DB_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)

    hospital_path = raw_dir / HOSPITAL_FILE
    department_path = raw_dir / DEPARTMENT_FILE
    if not hospital_path.exists():
        raise FileNotFoundError(f"Missing Excel file: {hospital_path}")
    if not department_path.exists():
        raise FileNotFoundError(f"Missing Excel file: {department_path}")

    sheets: list[tuple[Path, str]] = [
        *[(hospital_path, sheet) for sheet in HOSPITAL_SHEETS],
        *[(department_path, sheet) for sheet in DEPARTMENT_SHEETS],
    ]

    row_counts: dict[str, int] = {}
    con = duckdb.connect(str(db_path))
    try:
        con.execute(f"CREATE SCHEMA IF NOT EXISTS {RAW_SCHEMA}")
        for path, sheet_name in sheets:
            table = sheet_to_table_name(sheet_name)
            df = read_sheet(path, sheet_name)
            # Register DataFrame then materialize into raw.<table>
            con.register("_staging_df", df)
            con.execute(
                f"CREATE OR REPLACE TABLE {RAW_SCHEMA}.{table} AS SELECT * FROM _staging_df"
            )
            con.unregister("_staging_df")
            count = con.execute(
                f"SELECT COUNT(*) FROM {RAW_SCHEMA}.{table}"
            ).fetchone()[0]
            row_counts[f"{RAW_SCHEMA}.{table}"] = int(count)
    finally:
        con.close()

    return row_counts
