from __future__ import annotations

from pathlib import Path

import pytest

from dbt_powerbi_analytics.ingest.load import (
    DEFAULT_RAW_DIR,
    load_raw_to_duckdb,
)


@pytest.fixture
def rawdata_dir() -> Path:
    assert DEFAULT_RAW_DIR.exists(), f"Missing rawdata at {DEFAULT_RAW_DIR}"
    return DEFAULT_RAW_DIR


@pytest.fixture
def duckdb_path(tmp_path: Path) -> Path:
    return tmp_path / "test_analytics.duckdb"
