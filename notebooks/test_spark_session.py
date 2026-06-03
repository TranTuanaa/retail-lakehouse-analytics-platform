import sys
from pathlib import Path


project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from src.utils.spark_session import create_spark_session


spark = create_spark_session("TestSparkSession")

data = [
    ("C001", "Nguyen Van An"),
    ("C002", "Tran Thi Binh"),
]

columns = ["customer_id", "customer_name"]

df = spark.createDataFrame(data, columns)

df.show()

print("Spark version:", spark.version)

spark.stop()