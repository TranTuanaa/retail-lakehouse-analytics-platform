import sys
from pathlib import Path


project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from src.utils.config_loader import load_config
from src.utils.spark_session import create_spark_session


tables = [
    "customers",
    "products",
    "stores",
    "orders",
    "order_items",
]

config = load_config()

silver_root = Path(config["silver"]["path"])

spark = create_spark_session("CheckSilverAll")

for table in tables:
    table_path = silver_root / table

    df = spark.read.parquet(str(table_path))

    print("=" * 60)
    print(f"Table: {table}")
    print(f"Path: {table_path}")
    print(f"Rows: {df.count()}")
    print("Schema:")
    df.printSchema()
    print("Sample data:")
    df.show(truncate=False)

spark.stop()