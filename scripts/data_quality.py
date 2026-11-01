"""Assess the quality of the raw used-car dataset.

Produces ``outputs/data_quality_report.md`` with row/column counts, missing
values, duplicate rows, and per-column cardinality.
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "original_dataset.csv"
REPORT_PATH = ROOT / "outputs" / "data_quality_report.md"


def load_dataset(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. Place the raw CSV there and retry."
        )
    return pd.read_csv(path)


def build_report(df: pd.DataFrame, source: Path) -> str:
    total_rows, total_cols = df.shape
    duplicate_rows = int(df.duplicated().sum())
    missing = df.isna().sum()
    missing_pct = (missing / len(df) * 100).round(2) if len(df) else missing

    lines = [
        "# Data Quality Report",
        "",
        f"- **Source:** `{source}`",
        f"- **Generated:** {datetime.now():%Y-%m-%d %H:%M}",
        f"- **Rows:** {total_rows:,}",
        f"- **Columns:** {total_cols}",
        f"- **Duplicate rows:** {duplicate_rows:,}",
        "",
        "## Missing values",
        "",
        "| Column | Missing | Missing % | Unique |",
        "| --- | ---: | ---: | ---: |",
    ]

    for col in df.columns:
        lines.append(
            f"| {col} | {missing[col]:,} | {missing_pct[col]}% | {df[col].nunique(dropna=True):,} |"
        )

    high_missing = missing_pct[missing_pct > 50]
    lines += ["", "## Findings", ""]
    if duplicate_rows:
        lines.append(f"- {duplicate_rows:,} duplicate rows detected; remove during cleaning.")
    if high_missing.empty:
        lines.append("- No columns exceed 50% missing values.")
    else:
        for col, pct in high_missing.items():
            lines.append(f"- `{col}` is {pct}% missing; consider dropping or imputing.")
    if not duplicate_rows and high_missing.empty:
        lines.append("- Dataset passes basic completeness and uniqueness checks.")

    return "\n".join(lines) + "\n"


def main() -> int:
    try:
        df = load_dataset(RAW_PATH)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1

    report = build_report(df, RAW_PATH)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"Wrote {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
