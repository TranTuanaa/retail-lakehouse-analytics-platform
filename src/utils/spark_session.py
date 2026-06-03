import os
import sys

from pyspark.sql import SparkSession


def create_spark_session(app_name: str = "RetailLakehouseApp") -> SparkSession:
    """
    Create and return a SparkSession for local or Docker-based PySpark jobs.
    """

    python_executable = sys.executable

    os.environ["PYSPARK_PYTHON"] = python_executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = python_executable

    spark = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.pyspark.python", python_executable)
        .config("spark.pyspark.driver.python", python_executable)
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    return spark