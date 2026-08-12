"""Infer Excel header row indexes."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def infer_header_row(path: Path | str, sheet_name: str, max_scan: int = 10) -> int:
    """Return the first row index that looks like column headers.

    Skips mostly blank rows, then picks the first mostly-text row.
    Falls back to 0 if nothing matches.
    """
    preview = pd.read_excel(path, sheet_name=sheet_name, header=None, nrows=max_scan)
    for i in range(len(preview)):
        row = preview.iloc[i]
        non_null = row.dropna()
        if len(non_null) == 0:
            continue
        if row.notna().mean() < 0.5:
            continue
        text_share = non_null.map(lambda v: isinstance(v, str)).mean()
        if text_share >= 0.8:
            return i
    return 0
