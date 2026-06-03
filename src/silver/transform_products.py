import sys
from pathlib import Path

from pyspark.sql import functions as F


project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from src.utils.config_loader import load_config
from src.utils.spark_session import create_spark_session


def transform_products_to_silver():
    config = load_config()

    batch_id = config["pipeline"]["batch_id"]

    bronze_path = (
        Path(config["bronze"]["path"])
        / "products"
        / f"batch_id={batch_id}"
        / "products.parquet"
    )

    silver_path = Path(config["silver"]["path"]) / "products"

    spark = create_spark_session("TransformProductsToSilver")

    df = spark.read.parquet(str(bronze_path))

    silver_df = (
        df.select(
            "product_id",
            "product_name",
            "category",
            F.col("unit_price").cast("double").alias("unit_price"),
            F.to_date("created_at").alias("created_at"),
            "_ingestion_timestamp",
            "_source_file",
            "_batch_id",
        )
        .dropDuplicates(["product_id"])
    )

    silver_df.write.mode("overwrite").parquet(str(silver_path))

    print(f"Transformed products to silver: {silver_path}")

    spark.stop()


if __name__ == "__main__":
    transform_products_to_silver()