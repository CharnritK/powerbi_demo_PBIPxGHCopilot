# Serving Layer

The BI team is expected to consume curated tables or views from the serving layer rather than raw ingestion outputs.

Example curated assets:

- `gold.customer_sales`
- `gold.dim_date`
- `gold.dim_product`
- `gold.dim_region`

This separation keeps transformation ownership with Data Engineering and semantic ownership with BI.
