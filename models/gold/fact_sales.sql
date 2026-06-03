with orders as (

    select
        order_id,
        customer_id,
        store_id,
        cast(order_date as date) as order_date,
        order_status
    from read_parquet('data/silver/orders/**/*.parquet')

),

order_items as (

    select
        order_item_id,
        order_id,
        product_id,
        quantity,
        unit_price,
        line_total,
        cast(order_date as date) as order_date
    from read_parquet('data/silver/order_items/**/*.parquet')

)

select
    oi.order_item_id,
    oi.order_id,
    o.customer_id,
    o.store_id,
    oi.product_id,
    oi.order_date,
    o.order_status,
    oi.quantity,
    oi.unit_price,
    oi.line_total as sales_amount
from order_items oi
inner join orders o
    on oi.order_id = o.order_id
where o.order_status = 'completed'