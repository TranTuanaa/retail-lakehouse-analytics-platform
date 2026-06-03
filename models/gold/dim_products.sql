select
    product_id,
    product_name,
    category,
    unit_price,
    created_at
from read_parquet('data/silver/products/*.parquet')