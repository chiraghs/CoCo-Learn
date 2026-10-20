# Data Quality Report 1 — Automated Structural & Signal Test Suite

*Source: `analiz data test.py` (automated Python/pandas test script)*

## Purpose

This report documents the automated data-quality and signal-testing suite used to validate the dataset before it is handed to the AI modeling stage. The script loads all core tables and runs a series of structural, business-rule, and statistical-signal checks, printing the results as a single markdown-formatted table.

The actual numeric results produced by running this suite are documented in **Data Quality Report 2** and **Data Quality Report 3**, which independently reviewed and verified the script's output. This report describes the test methodology itself.

## Tables Loaded

- `URUN` (Product)
- `URUN_TEDARIKCI` (Product–Supplier)
- `TEDARIK_YOLU` (Supply Route)
- `ABC_SEGMENT` (ABC Segmentation)
- `SATIS` (Sales)
- `SATIN_ALMA` (Purchasing)
- `STOKGUNLUK` (Daily Stock)
- `TAKVIM` (Calendar)
- `OZEL_OLAYLAR` (Special Events)

## Test Categories

### 1. Deep Structural & Relational Integrity

| Test | Check |
|---|---|
| Sales–Product match | Flags any orphaned sales record whose `product_id` does not exist in the Product table. |
| Stock–Product match | Flags any orphaned stock record whose `product_id` does not exist in the Product table. |

### 2. Business Rules & Threshold Tests

| Test | Check |
|---|---|
| Negative stock check | Flags any `on_hand_qty` value below zero (a physical impossibility). |
| Timeline check | Computes `actual_lead_time = receipt_date - order_date` for every purchase order and flags any negative value (receipt before order). |
| Supplier MOQ compliance | Joins purchase orders with product–supplier data and flags orders where `qty_ordered` is below the supplier's `min_order_qty`. |
| Currency noise rule (10%) | Compares each sale's currency (`sale_currency`) against the product's base currency (`pro_currency`) and computes the percentage that differ. The production plan targets 8–12%; 0% is flagged as a failure, values inside the target band pass, anything else is a warning. |

### 3. Deep Statistical & Correlation Signals

| Test | Check |
|---|---|
| ABC-class volume distribution (Pareto) | Aggregates sold quantity by ABC class and compares the share of Class A vs. Class C volume; expects Class A to dominate. |
| Event lift (special-day demand impact) | Compares average daily sales quantity on special-event days vs. normal days; a lift greater than 10% is treated as a strong signal. |
| Price elasticity (discount vs. quantity) | Computes the Pearson correlation between `discount_rate` and `qty` across all sales; a correlation above 0.1 is treated as a usable signal. |
| Lagged correlation (event impact vs. demand 3 days later) | Aggregates daily event impact and daily sales, shifts sales by −3 days, and computes the Pearson correlation between event impact and demand three days later. |

### 4. Risk & Bottleneck Analysis

| Test | Check |
|---|---|
| Stockout (zero-stock) distribution | Counts the number of distinct product-days where `on_hand_qty` equals zero across the whole simulation. |

## Output Format

The script aggregates every check into a single results table with four columns — **Category**, **Test Name**, **Status**, **Detail / Metric** — using ✅ / ⚠️ / ❌ status markers, and prints it as a markdown table for inclusion in downstream reports.

## Relationship to Other Reports

This script is the source of the metrics discussed in:
- **Data Quality Report 2** (compliance verification against the production plan)
- **Data Quality Report 3** (full quality assessment)

Those two reports interpret the raw test output — for example, explaining why a weak demand-side signal on event days is expected *by design* (events and weather were modeled to affect logistics, not consumer demand) rather than a defect.
