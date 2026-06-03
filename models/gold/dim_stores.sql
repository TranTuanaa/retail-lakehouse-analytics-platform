select
    store_id,
    store_name,
    city,
    region,
    opened_at
from read_parquet('data/silver/stores/*.parquet')