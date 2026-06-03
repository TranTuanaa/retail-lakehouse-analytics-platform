# Retail Lakehouse Analytics Platform - Runbook

This runbook contains local development and operation commands for the project.

## 1. Start Airflow

Start the Airflow service:

```powershell
docker compose up airflow
```

Open Airflow UI:

```text
http://localhost:8081
```

Trigger the DAG manually in the Airflow UI:

```text
retail_lakehouse_pipeline
```

## 2. Build Docker Images

Build the Spark/PySpark image:

```powershell
docker compose build spark
```

Build the Airflow image:

```powershell
docker compose build airflow
```

Build all services:

```powershell
docker compose build
```

Use build commands only when `Dockerfile`, `Dockerfile.airflow`, `requirements.txt`, or Docker build settings are changed.

## 3. Check Airflow DAG Tasks

List all tasks in the pipeline DAG:

```powershell
docker compose exec airflow airflow tasks list retail_lakehouse_pipeline
```

Expected tasks:

```text
ingest_bronze
transform_silver
check_silver
run_dbt_gold
test_dbt_gold
check_gold
```

## 4. Run dbt Manually

Run dbt debug:

```powershell
docker compose run --rm spark dbt debug --profiles-dir .dbt
```

Run dbt models:

```powershell
docker compose run --rm spark dbt run --profiles-dir .dbt
```

Run dbt tests:

```powershell
docker compose run --rm spark dbt test --profiles-dir .dbt
```

Note: During normal operation, dbt is executed by Airflow tasks. Manual dbt commands are mainly for local debugging.

## 5. Check Output Tables

Check all Silver tables:

```powershell
docker compose run --rm spark python notebooks/check_silver_all.py
```

Check all Gold tables:

```powershell
docker compose run --rm spark python notebooks/check_gold_tables.py
```

Expected Gold tables:

```text
dim_customers
dim_products
dim_stores
fact_sales
```

## 6. Stop Services

Stop running containers:

```powershell
docker compose down
```

## 7. Clean Docker Build Cache

Check Docker disk usage:

```powershell
docker system df
```

Clean Docker build cache:

```powershell
docker builder prune
```

Avoid using destructive cleanup commands such as:

```powershell
docker system prune -a --volumes
```

unless you fully understand what will be removed.

## 8. Normal Local Workflow

For normal development, use this flow:

```powershell
cd C:\Users\ASUS\retail-lakehouse-analytics-platform
docker compose up airflow
```

Then open:

```text
http://localhost:8081
```

Trigger the DAG:

```text
retail_lakehouse_pipeline
```

The DAG runs the pipeline in this order:

```text
ingest_bronze
  -> transform_silver
  -> check_silver
  -> run_dbt_gold
  -> test_dbt_gold
  -> check_gold
```