# Retail-Batch-Analytics-Pipeline

# Retail Batch Analytics Pipeline

A learning project that generates fictional retail transactions in
PostgreSQL and processes them in Databricks.

## Architecture

Python → PostgreSQL → CSV exports → Databricks Bronze → Silver → Gold

## Technologies

- Python: generate and export sample data
- PostgreSQL: store transactional records
- Docker: run PostgreSQL locally
- Databricks and PySpark: process data
- Delta Lake: store analytical tables
- SQL: calculate business metrics

## Data

Six source tables:
categories, products, stores, customers, orders, order_items.

## Processing layers

- Bronze: raw CSV data saved as Delta tables
- Silver: typed and validated records, with rejected-record tables
- Gold: daily sales, store performance, product performance,
  customer metrics, and category revenue

## Run order

1. Start PostgreSQL using postgres/docker-compose.yml.
2. Execute the table definitions in postgres/01_schema.sql.
3. Install dependencies: pip install -r requirements.txt
4. Run producer/generate_orders.py.
5. Run producer/export_tables.py.
6. Upload the exported CSV files to the Databricks Volume:
   /Volumes/workspace/retail/raw_files/
7. Import and run the Databricks notebooks in numbered order.

## Sales definition

Sales include orders currently marked PAID or SHIPPED.
Reports use the order creation date.

## Limitations

- Synthetic data for learning.
- Manual CSV upload into Databricks.
- Full refreshes rather than incremental processing.
- No Kafka or streaming.
- No payment-date or partial-refund accounting.
- The multi-table pipeline is not one atomic transaction.

## Local setup credentials

The example credentials are for a local practice database only.
