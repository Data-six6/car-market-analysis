"""Clean the raw used-car dataset.

Reads ``data/raw/original_dataset.csv`` and writes
``data/processed/used_cars_cleaned.csv``:

- normalises column names and trims whitespace
- removes exact duplicates
- coerces numeric fields (price, year, mileage)
- drops rows with invalid price/year/mileage
- standardises text categories
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "original_dataset.csv"
CLEAN_PATH = ROOT / "data" / "processed" / "used_cars_cleaned.csv"

NUMERIC_COLUMNS = ("price", "year", "mileage")
TEXT_COLUMNS = ("make", "model", "fuel_type", "transmission", "seller_type", "location")


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype("string").str.strip()

    df = df.drop_duplicates()

    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in TEXT_COLUMNS:
        if col in df.columns:
            df[col] = df[col].str.title()

    if "price" in df.columns:
        df = df[df["price"] > 0]
    if "year" in df.columns:
        df = df[df["year"].between(1950, pd.Timestamp.now().year)]
    if "mileage" in df.columns:
        df = df[df["mileage"] >= 0]

    return df.dropna(subset=[c for c in NUMERIC_COLUMNS if c in df.columns])


def main() -> int:
    if not RAW_PATH.exists():
        print(
            f"Dataset not found at {RAW_PATH}. Place the raw CSV there and retry.",
            file=sys.stderr,
        )
        return 1

    raw = pd.read_csv(RAW_PATH)
    cleaned = clean(raw)

    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(CLEAN_PATH, index=False)
    print(f"Raw rows: {len(raw):,} -> cleaned rows: {len(cleaned):,}")
    print(f"Wrote {CLEAN_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
