# Synthetic Supply Chain Dataset (v3, English)

## Overview

This is a fully synthetic, relational supply-chain dataset built to train and evaluate AI models for **demand forecasting** and **inventory / stock optimization**. It simulates one full year of operations across products, customers, suppliers, purchasing, sales, logistics, weather, and calendar events.

The dataset was generated with a deterministic random seed (`seed=42`) to ensure reproducibility, and models a 365-day period from **2025-01-01 to 2025-12-31**.

## Context

The dataset supports an end-to-end AI system for demand prediction and stock optimization: forecasting product-level demand from historical sales and seasonal effects, reducing inventory holding costs, and providing decision support for order planning. It integrates:

- **120 products (SKUs)** across **30 categories**
- **12 suppliers**
- **120 customer companies**
- **4 sales channels** (Online, Retail, Wholesale, B2B Express)

## Content

The dataset consists of 13 relational CSV tables:

| File | Description | Key Columns |
|---|---|---|
| `PRODUCT.csv` | Product master data | `product_id`, `product_code`, `product_name`, `category`, `uom`, `is_active`, `pro_currency`, `base_price`, `base_cost`, `holding_cost_rate` |
| `SUPPLIER.csv` | Supplier master data | `supplier_id`, `supplier_name`, `supplier_city`, `supplier_country`, `is_active` |
| `PRODUCT_SUPPLIER.csv` | Product–supplier relationship (sourcing options, MOQ) | `product_supplier_id`, `product_id`, `supplier_id`, `is_primary`, `min_order_qty` |
| `SUPPLY_ROUTE.csv` | Shipping routes per supplier (mode, lead time, cost) | `route_id`, `supplier_id`, `origin_city`, `destination_city`, `transport_mode`, `lead_time_mean_days`, `lead_time_std_days`, `shipment_cost` |
| `PURCHASING.csv` | Purchase order lines (inbound supply) | `po_line_id`, `product_id`, `supplier_id`, `route_id`, `order_date`, `receipt_date`, `qty_ordered`, `qty_received`, `unit_cost`, `purch_currency` |
| `CUSTOMER_COMPANY.csv` | Customer master data | `customer_id`, `customer_city`, `customer_name`, `customer_segment` |
| `SALES_CHANNEL.csv` | Sales channel definitions | `channel_id`, `channel_name`, `fulfillment_type`, `ship_mode`, `sla_days` |
| `SALES.csv` | Sales order lines (outbound demand) | `sales_id`, `product_id`, `customer_id`, `channel_id`, `order_date`, `qty`, `unit_price`, `discount_rate`, `sale_currency` |
| `DAILY_STOCK.csv` | Daily inventory position per product | `product_id`, `date`, `on_hand_qty`, `in_transit_qty`, `reserved_qty` |
| `ABC_SEGMENT_v22.csv` | Monthly ABC (Pareto) classification per product | `abc_id`, `product_id`, `period_start`, `period_end`, `abc_class` |
| `CALENDAR.csv` | Calendar dimension | `date`, `dow`, `week_of_year`, `month`, `is_weekend` |
| `SPECIAL_EVENTS.csv` | Holidays, promotions and logistics-impacting events by city | `event_id`, `date`, `event_name`, `event_type`, `city`, `impact_level` |
| `WEATHER_CLEAN.csv` | Daily weather by city (cleaned) | `date`, `city`, `temp_c`, `precip_mm`, `is_extreme` |

All column names and text content are in English. City names are given in lowercase (e.g. `istanbul`, `munich`, `ningbo`) and currencies use ISO codes (`USD`, `EUR`, `TRY`).

## Data Generation Methodology

- Fully synthetic data generated with a deterministic seed (`seed=42`) for reproducibility — no real customer, supplier, or transactional data is included.
- **Design intent:** special events and weather are modeled to primarily affect the **supply / logistics side** (unit cost increases of 20–60% on event days, lead times extended by 2–7 days under extreme weather) rather than consumer demand directly. This is a deliberate design choice, not a data defect — see Data Quality Report 2 and Report 3 for details.
- Currency noise (customers/orders using a different currency than the product's base currency) was intentionally **not** injected in this version, to avoid over-complicating early modeling iterations.
- A small number of inactive products intentionally still carry historical sales rows, to allow models to be tested against real-world "stale SKU" noise.

## Data Quality Summary

An automated relational-integrity and business-rule test suite, plus two independent quality reviews, were run against this dataset before release. Highlights:

- **Referential integrity:** 0 orphaned records between Sales/Stock and Products.
- **Business rules:** 0 records with negative stock; 0 purchase orders with receipt date before order date.
- **ABC (Pareto) segmentation:** confirms the expected skew, with a small share of products driving the majority of sales volume.
- **Stockout scenarios:** stock reaches zero on several hundred distinct product-days across the simulation, providing realistic signal for stockout / lost-sales modeling.
- **Known limitation (to be addressed in a future version):** the correlation between discount rate and sales quantity is currently weak, so price-elasticity modeling should not rely on this signal as-is.

Full details are provided in the accompanying reports:

- `Data_Quality_Report_1.md` — Automated structural & business-rule test suite (methodology)
- `Data_Quality_Report_2.md` — Compliance verification against the original data production plan
- `Data_Quality_Report_3.md` — Full data quality assessment
- `Data_Quality_Report_4.md` — ABC product segmentation analysis

## Suggested Use Cases

- Demand forecasting (time series / ML regression)
- Inventory / safety-stock optimization
- Stockout and lost-sales risk modeling
- Supplier lead-time and logistics risk analysis
- ABC / Pareto-based inventory segmentation
- Feature engineering with weather and calendar events as supply-side shock indicators

## License & Notes

This dataset is entirely synthetic and contains no real personal, customer, or business data. It is provided for research, educational, and model-development purposes.
