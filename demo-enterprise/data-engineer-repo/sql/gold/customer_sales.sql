-- Mock serving-layer SQL for demo purposes.
select
    c.customer_id,
    c.customer_name,
    s.region,
    s.order_date,
    s.sales_amount,
    s.cost_amount,
    s.sales_amount - s.cost_amount as gross_margin
from silver.customer c
join silver.sales s
    on c.customer_id = s.customer_id;
