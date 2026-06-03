import duckdb


database_path = "data/gold/retail_lakehouse.duckdb"

tables = [
    "dim_customers",
    "dim_products",
    "dim_stores",
    "fact_sales",
]

conn = duckdb.connect(database_path)

for table in tables:
    print("=" * 60)
    print(f"Table: {table}")

    row_count = conn.execute(f"select count(*) from {table}").fetchone()[0]
    print(f"Rows: {row_count}")

    df = conn.execute(f"select * from {table} limit 5").fetchdf()
    print(df)

conn.close()