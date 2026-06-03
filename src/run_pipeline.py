from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="retail_lakehouse_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["retail", "lakehouse", "data-engineering"],
) as dag:

    ingest_bronze = BashOperator(
        task_id="ingest_bronze",
        bash_command="cd /app && python src/ingestion/ingest_csv_to_bronze.py && python src/ingestion/ingest_orders_incremental.py",
    )

    transform_silver = BashOperator(
        task_id="transform_silver",
        bash_command="cd /app && python src/silver/run_all_silver_transforms.py",
    )

    check_silver = BashOperator(
        task_id="check_silver",
        bash_command="cd /app && python notebooks/check_silver_all.py",
    )

    ingest_bronze >> transform_silver >> check_silver # type: ignore