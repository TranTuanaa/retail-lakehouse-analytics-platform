from logging import config
import sys
from pathlib import Path

import pandas as pd


project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from src.utils.config_loader import load_config
from src.utils.metadata_utils import read_json_file, write_json_file


def ingest_orders_incremental_to_bronze():
    config = load_config()

    batch_id = config["pipeline"]["batch_id"]

    source_path = Path(config["source"]["path"]) / "orders.csv"
    bronze_path = Path(config["bronze"]["path"]) / "orders" / f"batch_id={batch_id}"
    metadata_path = Path(config["metadata"]["path"]) / "orders_state.json"

    state = read_json_file(str(metadata_path))
    last_loaded_updated_at = pd.to_datetime(state["last_loaded_updated_at"])

    lookback_days = config["pipeline"]["lookback_days"]
    cutoff_time = last_loaded_updated_at - pd.Timedelta(days=lookback_days)

    print(f"Last loaded updated_at: {last_loaded_updated_at}")
    print(f"Lookback days: {lookback_days}")
    print(f"Cutoff time: {cutoff_time}")

    df = pd.read_csv(source_path)

    df["updated_at"] = pd.to_datetime(df["updated_at"])

    incremental_df = df[df["updated_at"] >= cutoff_time].copy()

    if incremental_df.empty:
        print("No new orders to ingest.")
        return

    incremental_df["_ingestion_timestamp"] = pd.Timestamp.now()
    incremental_df["_source_file"] = str(source_path)
    incremental_df["_batch_id"] = batch_id

    bronze_path.mkdir(parents=True, exist_ok=True)

    output_file = bronze_path / "orders.parquet"
    incremental_df.to_parquet(
        output_file,
        index=False,
        engine="pyarrow",
        coerce_timestamps="ms",
        allow_truncated_timestamps=True,
    )

    new_last_loaded_updated_at = incremental_df["updated_at"].max().strftime("%Y-%m-%d %H:%M:%S")

    write_json_file(
        str(metadata_path),
        {
            "last_loaded_updated_at": new_last_loaded_updated_at
        }
    )

    print(f"Ingested incremental orders to bronze: {output_file}")
    print(f"Updated metadata: last_loaded_updated_at = {new_last_loaded_updated_at}")


if __name__ == "__main__":
    ingest_orders_incremental_to_bronze()