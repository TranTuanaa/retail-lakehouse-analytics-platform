import sys
from pathlib import Path


project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from src.utils.config_loader import load_config
from src.utils.spark_session import create_spark_session


config = load_config()

bronze_orders_root = Path(config["bronze"]["path"]) / "orders"

spark = create_spark_session("CheckBronzeOrdersBatches")

df = spark.read.parquet(str(bronze_orders_root))

print("Bronze orders from all batches:")
df.show(truncate=False)

print("Rows:", df.count())

print("Batch count:")
df.groupBy("_batch_id").count().show(truncate=False)

spark.stop()