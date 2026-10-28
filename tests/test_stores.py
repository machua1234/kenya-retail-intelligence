
from datetime import date

from src.generators.generate_stores import (
    generate_stores,
    COUNTY_TOWNS,
    STORE_TYPES,
)


def test_store_count():
    df = generate_stores(20)
    assert len(df) == 20


def test_unique_store_ids():
    df = generate_stores(20)
    assert df["store_id"].is_unique


def test_no_missing_values():
    df = generate_stores(20)
    assert not df.isnull().any().any()


def test_required_columns():
    df = generate_stores(20)

    required = {
        "store_id",
        "store_name",
        "county",
        "town",
        "opening_date",
        "store_type",
    }

    assert required.issubset(df.columns)


def test_valid_opening_dates():
    df = generate_stores(20)

    assert all(
        opening_date <= date.today()
        for opening_date in df["opening_date"]
    )


def test_valid_county_town_relationship():
    df = generate_stores(20)

    for _, row in df.iterrows():
        assert row["county"] in COUNTY_TOWNS
        assert row["town"] in COUNTY_TOWNS[row["county"]]


def test_valid_store_types():
    df = generate_stores(20)

    assert df["store_type"].isin(STORE_TYPES).all()
