
from pathlib import Path
import pandas as pd

from src.generators.generate_stores import (
    COUNTY_TOWNS,
    STORE_TYPES,
)


def validate_stores(file_path):
    df = pd.read_csv(file_path)

    required_columns = [
        "store_id",
        "store_name",
        "county",
        "town",
        "opening_date",
        "store_type",
    ]

    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing columns: {sorted(missing_columns)}"
        )

    if df.empty:
        raise ValueError("Dataset is empty")

    if df[required_columns].isnull().any().any():
        raise ValueError("Missing values detected")

    if (df[required_columns].astype(str).apply(
        lambda col: col.str.strip().eq("")
    )).any().any():
        raise ValueError("Blank values detected")

    if df["store_id"].duplicated().any():
        raise ValueError("Duplicate store IDs detected")

    opening_dates = pd.to_datetime(
        df["opening_date"],
        errors="coerce"
    )

    if opening_dates.isna().any():
        raise ValueError("Invalid opening dates detected")

    if (opening_dates.dt.date > pd.Timestamp.now().date()).any():
        raise ValueError("Future opening dates detected")

    for _, row in df.iterrows():
        county = row["county"]
        town = row["town"]

        if county not in COUNTY_TOWNS:
            raise ValueError(f"Unknown county: {county}")

        if town not in COUNTY_TOWNS[county]:
            raise ValueError(
                f"Invalid town {town} for county {county}"
            )

    if not df["store_type"].isin(STORE_TYPES).all():
        raise ValueError("Invalid store type detected")

    print(f"Validation successful: {len(df)} records")
    return True


if __name__ == "__main__":
    validate_stores(Path("data/raw/stores.csv"))
