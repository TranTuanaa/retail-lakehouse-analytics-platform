# Retail Lakehouse Analytics Platform

A production-style Data Engineering project that simulates an end-to-end retail analytics pipeline using Medallion Architecture.

The pipeline ingests retail source data, stores it in Bronze, transforms it into cleaned Silver datasets using PySpark, builds analytics-ready Gold tables using dbt, and orchestrates the whole workflow with Apache Airflow.

## 1. Project Overview

This project simulates a data platform for a retail business.

Business questions this platform can support:

- What is the total sales revenue?
- Which products generate the most revenue?
- Which stores have the highest sales?
- How many completed orders are processed?
- How does sales performance change by date?

The project is designed as a portfolio project for Data Engineering roles.

## 2. Architecture

```text
Source CSV Files
      ↓
Bronze Layer
Raw ingested data with metadata
      ↓
Silver Layer
Cleaned and refined Parquet tables using PySpark
      ↓
Gold Layer
Analytics-ready fact and dimension tables using dbt + DuckDB
      ↓
Validation
dbt tests and custom check scripts
      ↓
Orchestration
Apache Airflow DAG
```

## 3. Tech Stack

- Python
- Pandas
- PySpark
- Docker
- Apache Airflow
- dbt
- DuckDB
- Parquet
- YAML configuration

## 4. Medallion Architecture

### Bronze Layer

The Bronze layer stores ingested source data with metadata columns.

Example metadata columns:

```text
_ingestion_timestamp
_source_file
_batch_id
```

Bronze keeps data close to the original source format and acts as the raw storage layer.

### Silver Layer

The Silver layer contains cleaned and refined data.

Main transformations include:

- Type casting
- Date and timestamp parsing
- Deduplication
- Partitioning by date
- Joining orders with order items
- Calculating line-level sales amount

Silver tables:

```text
customers
products
stores
orders
order_items
```

### Gold Layer

The Gold layer contains analytics-ready tables for reporting and dashboarding.

Gold tables:

```text
dim_customers
dim_products
dim_stores
fact_sales
```

The Gold layer is built using dbt and stored in DuckDB.

## 5. Pipeline Flow

The Airflow DAG runs the pipeline in this order:

```text
ingest_bronze
  -> transform_silver
  -> check_silver
  -> run_dbt_gold
  -> test_dbt_gold
  -> check_gold
```

### Airflow DAG

DAG name:

```text
retail_lakehouse_pipeline
```

The DAG handles:

- Bronze ingestion
- Silver transformation
- Silver validation
- Gold table creation with dbt
- dbt data tests
- Gold output validation

## 6. Incremental Ingestion

The project includes incremental ingestion logic for the `orders` table.

It uses:

```text
updated_at
```

as the incremental column.

The pipeline stores the last processed timestamp in:

```text
data/metadata/orders_state.json
```

A lookback window is also used to simulate late-arriving data handling.

Example config:

```yaml
lookback_days: 2
```

This allows the pipeline to reprocess recent records and reduce the risk of missing late updates.

## 7. Data Quality

dbt tests are defined for Gold models.

Example tests:

- `not_null`
- `unique`

Important columns tested include:

```text
customer_id
product_id
store_id
order_item_id
sales_amount
```

These tests help ensure that Gold tables are reliable for analytics.

## 8. How to Run Locally

Start Airflow:

```powershell
docker compose up airflow
```

Open Airflow UI:

```text
http://localhost:8081
```

Trigger the DAG manually:

```text
retail_lakehouse_pipeline
```

For detailed local commands and troubleshooting, see:

```text
docs/runbook.md
```

## 9. Project Structure

```text
.
├── configs/
│   └── pipeline.yaml
│
├── dags/
│   └── retail_lakehouse_dag.py
│
├── data/
│   ├── source/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   └── metadata/
│
├── docs/
│   └── runbook.md
│
├── models/
│   └── gold/
│       ├── dim_customers.sql
│       ├── dim_products.sql
│       ├── dim_stores.sql
│       ├── fact_sales.sql
│       └── schema.yml
│
├── notebooks/
│   ├── check_silver_all.py
│   └── check_gold_tables.py
│
├── src/
│   ├── ingestion/
│   ├── silver/
│   └── utils/
│
├── .dbt/
│   └── profiles.yml
│
├── Dockerfile
├── Dockerfile.airflow
├── docker-compose.yml
├── dbt_project.yml
├── requirements.txt
└── README.md
```

## 10. Output Tables

### Dimension Tables

```text
dim_customers
dim_products
dim_stores
```

### Fact Table

```text
fact_sales
```

`fact_sales` contains completed sales order items and is designed for revenue analysis.

## 11. Current Status

Completed features:

- Source CSV ingestion
- Bronze layer with metadata
- Silver transformation using PySpark
- Incremental orders ingestion
- Lookback window logic
- Gold layer using dbt and DuckDB
- dbt tests
- Airflow orchestration
- Dockerized local environment

## 12. Notes

This project is designed for local development and portfolio demonstration.

For production usage, the following improvements would be recommended:

- Replace CSV sources with database or streaming sources
- Use cloud object storage such as S3
- Use a production Airflow metadata database such as PostgreSQL
- Use Spark cluster execution instead of local mode
- Add stronger data quality checks
- Add monitoring and alerting