import sys
from pathlib import Path

from pyspark.sql import functions as F


project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from src.utils.config_loader import load_config
from src.utils.spark_session import create_spark_session


def transform_customers_to_silver():
    config = load_config()

    batch_id = config["pipeline"]["batch_id"]

    bronze_path = (
        Path(config["bronze"]["path"])
        / "customers"
        / f"batch_id={batch_id}"
        / "customers.parquet"
    )

    silver_path = Path(config["silver"]["path"]) / "customers"

    spark = create_spark_session("TransformCustomersToSilver")

    df = spark.read.parquet(str(bronze_path))

    silver_df = (
        df.select(
            "customer_id",
            "customer_name",
            "email",
            "city",
            F.to_date("created_at").alias("created_at"),
            "_ingestion_timestamp",
            "_source_file",
            "_batch_id",
        )
        .dropDuplicates(["customer_id"])
    )

    silver_df.write.mode("overwrite").parquet(str(silver_path))

    print(f"Transformed customers to silver: {silver_path}")

    spark.stop()


if __name__ == "__main__":
    transform_customers_to_silver()