
from pathlib import Path
from datetime import date
import random

import pandas as pd
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

COUNTY_TOWNS = {
    "Nairobi": ["Westlands", "Kasarani", "Embakasi"],
    "Mombasa": ["Nyali", "Likoni", "Changamwe"],
    "Kisumu": ["Kisumu Central", "Kondele"],
    "Nakuru": ["Nakuru Town", "Naivasha"],
    "Uasin Gishu": ["Eldoret", "Turbo"],
    "Kiambu": ["Thika", "Ruiru", "Kiambu Town"],
    "Machakos": ["Machakos Town", "Athi River"],
    "Kajiado": ["Kitengela", "Ongata Rongai"],
}

STORE_TYPES = [
    "Supermarket",
    "Mini Market",
    "Wholesale",
]


def generate_stores(number_of_stores=20):
    stores = []

    for i in range(1, number_of_stores + 1):
        county = random.choice(list(COUNTY_TOWNS))
        town = random.choice(COUNTY_TOWNS[county])

        store = {
            "store_id": f"STR{i:04d}",
            "store_name": f"Retail Store {i}",
            "county": county,
            "town": town,
            "opening_date": fake.date_between(
                start_date="-5y",
                end_date="today"
            ),
            "store_type": random.choice(STORE_TYPES),
        }

        stores.append(store)

    return pd.DataFrame(stores)


if __name__ == "__main__":
    df = generate_stores(20)

    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "stores.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df)} stores")
    print(df.head())
    print(f"Saved to {output_file}")
