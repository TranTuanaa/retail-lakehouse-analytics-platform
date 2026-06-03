import pandas as pd
from pathlib import Path

source_dir = Path("data/source")

files = [
    "customers.csv",
    "products.csv",
    "stores.csv",
    "orders.csv",
    "order_items.csv",
]

for file_name in files:
    file_path = source_dir / file_name
    df = pd.read_csv(file_path)

    print("=" * 50)
    print(f"File: {file_name}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print(df.head())