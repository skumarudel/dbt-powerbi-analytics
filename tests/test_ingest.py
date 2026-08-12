"""Tests for Excel → DuckDB raw ingest (landing zone for bronze)."""

from __future__ import annotations

from pathlib import Path

import duckdb

from dbt_powerbi_analytics.ingest.headers import infer_header_row
from dbt_powerbi_analytics.ingest.load import (
    HOSPITAL_FILE,
    sheet_to_table_name,
    load_raw_to_duckdb,
)

EXPECTED_RAW_TABLES = {
    "patient_visits_2020_2021",
    "patient_visits_2022_2023",
    "patient_visits_2024",
    "patient_visits_2025",
    "dim_patient",
    "dim_doctor",
    "dim_department",
    "dim_diagnosis",
    "dim_treatment",
    "dim_payment_method",
    "dept_hod",
}


def test_sheet_to_table_name():
    assert sheet_to_table_name("Dim_Patient") == "dim_patient"
    assert sheet_to_table_name("PatientVisits_2020_2021") == "patient_visits_2020_2021"
    assert sheet_to_table_name("Dim_PaymentMethod") == "dim_payment_method"
    assert sheet_to_table_name("Dept_HOD") == "dept_hod"


def test_infer_header_row_skips_blank_first_row(rawdata_dir: Path):
    hospital = rawdata_dir / HOSPITAL_FILE
    assert infer_header_row(hospital, "Dim_Patient") == 1
    assert infer_header_row(hospital, "Dim_Department") == 1
    assert infer_header_row(hospital, "Dim_Doctor") == 0


def test_ingest_creates_all_raw_tables(rawdata_dir: Path, duckdb_path: Path):
    counts = load_raw_to_duckdb(raw_dir=rawdata_dir, db_path=duckdb_path)

    assert set(counts) == {f"raw.{t}" for t in EXPECTED_RAW_TABLES}
    assert all(n > 0 for n in counts.values())

    con = duckdb.connect(str(duckdb_path), read_only=True)
    try:
        tables = {
            row[0]
            for row in con.execute(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'raw'"
            ).fetchall()
        }
    finally:
        con.close()

    assert tables == EXPECTED_RAW_TABLES


def test_ingest_dim_patient_has_real_column_names(
    rawdata_dir: Path, duckdb_path: Path
):
    load_raw_to_duckdb(raw_dir=rawdata_dir, db_path=duckdb_path)
    con = duckdb.connect(str(duckdb_path), read_only=True)
    try:
        cols = [
            row[0]
            for row in con.execute(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_schema = 'raw' AND table_name = 'dim_patient' "
                "ORDER BY ordinal_position"
            ).fetchall()
        ]
        sample = con.execute(
            'SELECT "PatientID" FROM raw.dim_patient LIMIT 1'
        ).fetchone()
    finally:
        con.close()

    assert "PatientID" in cols
    assert not any(c.startswith("Unnamed") for c in cols)
    assert sample is not None
    assert str(sample[0]).startswith("P")


def test_ingest_dim_department_has_real_column_names(
    rawdata_dir: Path, duckdb_path: Path
):
    load_raw_to_duckdb(raw_dir=rawdata_dir, db_path=duckdb_path)
    con = duckdb.connect(str(duckdb_path), read_only=True)
    try:
        cols = [
            row[0]
            for row in con.execute(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_schema = 'raw' AND table_name = 'dim_department' "
                "ORDER BY ordinal_position"
            ).fetchall()
        ]
    finally:
        con.close()

    assert cols == [
        "DepartmentID",
        "DepartmentName",
        "DepartmentCategory",
        "Specialization",
        "HOD",
    ]


def test_ingest_is_idempotent(rawdata_dir: Path, duckdb_path: Path):
    first = load_raw_to_duckdb(raw_dir=rawdata_dir, db_path=duckdb_path)
    second = load_raw_to_duckdb(raw_dir=rawdata_dir, db_path=duckdb_path)
    assert first == second
