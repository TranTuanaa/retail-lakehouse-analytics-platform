import sys
from pathlib import Path


project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from src.utils.config_loader import load_config
from src.utils.spark_session import create_spark_session


config = load_config()

silver_path = Path(config["silver"]["path"]) / "stores"

spark = create_spark_session("CheckSilverStores")

df = spark.read.parquet(str(silver_path))

print("Silver stores:")
df.show(truncate=False)

print("Schema:")
df.printSchema()

print("Rows:", df.count())

spark.stop()