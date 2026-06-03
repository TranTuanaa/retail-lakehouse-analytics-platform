import sys
from pathlib import Path

from pyspark.sql import functions as F
from pyspark.sql.window import Window


project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from src.utils.config_loader import load_config
from src.utils.spark_session import create_spark_session


def transform_orders_to_silver():
    config = load_config()

    batch_id = config["pipeline"]["batch_id"]

    bronze_path = Path(config["bronze"]["path"]) / "orders"

    silver_path = Path(config["silver"]["path"]) / "orders"

    spark = create_spark_session("TransformOrdersToSilver")

    df = spark.read.parquet(str(bronze_path))

    cleaned_df = df.select(
        "order_id",
        "customer_id",
        "store_id",
        F.to_date("order_date").alias("order_date"),
        F.col("order_status"),
        F.to_timestamp("updated_at").alias("updated_at"),
        "_ingestion_timestamp",
        "_source_file",
        "_batch_id",
    )

    window_spec = Window.partitionBy("order_id").orderBy(F.col("updated_at").desc())

    silver_df = (
        cleaned_df
        .withColumn("row_number", F.row_number().over(window_spec))
        .filter(F.col("row_number") == 1)
        .drop("row_number")
    )

    silver_df.write.mode("overwrite").partitionBy("order_date").parquet(str(silver_path))

    print(f"Transformed orders to silver: {silver_path}")

    spark.stop()


if __name__ == "__main__":
    transform_orders_to_silver()