import sys
from pathlib import Path

import pandas as pd


project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from src.utils.config_loader import load_config

tables = [
    "customers",
    "products",
    "stores",
    "orders",
    "order_items",
]

config = load_config()

bronze_root = Path(config["bronze"]["path"])
batch_id = config["pipeline"]["batch_id"]

for table in tables:
    file_path = bronze_root / table / f"batch_id={batch_id}" / f"{table}.parquet"

    df = pd.read_parquet(file_path)

    print("=" * 60)
    print(f"Table: {table}")
    print(f"Path: {file_path}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print(df.head())