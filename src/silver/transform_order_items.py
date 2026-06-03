import sys
from pathlib import Path

from pyspark.sql import functions as F


project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from src.utils.config_loader import load_config
from src.utils.spark_session import create_spark_session


def transform_order_items_to_silver():
    config = load_config()

    batch_id = config["pipeline"]["batch_id"]

    bronze_path = Path(config["bronze"]["path"]) / "order_items"

    silver_orders_path = Path(config["silver"]["path"]) / "orders"
    silver_path = Path(config["silver"]["path"]) / "order_items"

    spark = create_spark_session("TransformOrderItemsToSilver")

    order_items_df = spark.read.parquet(str(bronze_path))

    orders_df = (
        spark.read.parquet(str(silver_orders_path))
        .select("order_id", "order_date")
    )

    cleaned_order_items_df = (
        order_items_df.select(
            "order_item_id",
            "order_id",
            "product_id",
            F.col("quantity").cast("int").alias("quantity"),
            F.col("unit_price").cast("double").alias("unit_price"),
            "_ingestion_timestamp",
            "_source_file",
            "_batch_id",
        )
        .withColumn("line_total", F.col("quantity") * F.col("unit_price"))
        .dropDuplicates(["order_item_id"])
    )

    silver_df = (
        cleaned_order_items_df
        .join(orders_df, on="order_id", how="left")
    )

    silver_df.write.mode("overwrite").partitionBy("order_date").parquet(str(silver_path))
    
    print(f"Transformed order_items to silver: {silver_path}")

    spark.stop()


if __name__ == "__main__":
    transform_order_items_to_silver()