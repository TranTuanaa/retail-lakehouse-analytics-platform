from logging import config
import sys
from pathlib import Path

import pandas as pd


project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from src.utils.config_loader import load_config


def ingest_table_to_bronze(table_name: str):
    config = load_config()

    source_path = Path(config["source"]["path"]) / f"{table_name}.csv"
    batch_id = config["pipeline"]["batch_id"]
    bronze_path = Path(config["bronze"]["path"]) / table_name / f"batch_id={batch_id}"
    
    df = pd.read_csv(source_path)

    df["_ingestion_timestamp"] = pd.Timestamp.now()
    df["_source_file"] = str(source_path)
    df["_batch_id"] = config["pipeline"]["batch_id"]

    bronze_path.mkdir(parents=True, exist_ok=True)

    output_file = bronze_path / f"{table_name}.parquet"
    df.to_parquet(output_file, index=False)

    print(f"Ingested {table_name} to bronze: {output_file}")


if __name__ == "__main__":
    tables = [
        "customers",
        "products",
        "stores",
        "orders",
        "order_items",
    ]

    for table in tables:
        ingest_table_to_bronze(table)