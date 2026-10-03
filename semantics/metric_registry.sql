-- ============================================================================
-- SUPPLYCHAINIQ: FIRST-CLASS GOVERNED METRIC REGISTRY
-- Ground truth definitions, owners, grains, and canonical formulas
-- ============================================================================

USE DATABASE SUPPLY_CHAIN_DB;
USE SCHEMA SUPPLY_CHAIN_DB.CORE;

CREATE OR REPLACE TABLE METRIC_REGISTRY (
    metric_id VARCHAR(50) PRIMARY KEY,
    display_name VARCHAR(100),
    definition VARCHAR,
    grain VARCHAR(50),
    owner_persona VARCHAR(50),
    canonical_formula VARCHAR,
    sql_expression VARCHAR,
    allowed_dimensions VARCHAR
);

INSERT INTO METRIC_REGISTRY VALUES
(
    'on_time_delivery',
    'On-Time Delivery (OTD / OTIF)',
    'Percentage of eligible shipments delivered on or before the promised delivery date with full quantity fulfilled.',
    'Shipment',
    'Logistics & Freight',
    'SUM(CASE WHEN actual_arrival_date <= promised_delivery_date AND qty_received >= qty_ordered THEN 1 ELSE 0 END) / COUNT(shipment_id) * 100',
    'ROUND(COUNT(DISTINCT CASE WHEN shp.actual_arrival_date <= po.promised_delivery_date AND shp.qty_received >= po.qty_ordered THEN shp.shipment_id END) * 100.0 / NULLIF(COUNT(DISTINCT shp.shipment_id), 0), 1)',
    '["supplier", "part", "plant", "carrier", "route", "time"]'
),
(
    'days_of_inventory',
    'Days of Inventory (DOI)',
    'Estimated production runway in days before assembly line halts due to component stockout.',
    'Plant + Part + Date',
    'Plant Operations',
    'Current On-Hand Warehouse Stock / Daily Plant Burn Rate',
    'ROUND(inv.on_hand_qty * 1.0 / NULLIF(p.daily_burn_rate_units, 0), 1)',
    '["plant", "part", "criticality", "category", "time"]'
),
(
    'liquidated_damages_liability',
    'Contractual Delay Penalty Liability',
    'Legally enforceable financial damages accrued by suppliers beyond contractual SLA grace period.',
    'Supplier + Order + Shipment',
    'Procurement',
    'SUM(Daily Liquidated Damages USD * MAX(0, Delay Days - Contract Grace Days))',
    'SUM(s.daily_liquidated_damages_usd * GREATEST(0, DATEDIFF(day, po.promised_delivery_date, COALESCE(shp.actual_arrival_date, CURRENT_DATE())) - s.contract_sla_grace_days))',
    '["supplier", "part", "contract", "po_id", "time"]'
),
(
    'landed_cost',
    'Total Landed Cost',
    'Total cost of acquiring and positioning a component including freight, demurrage, and purchase price.',
    'Part + Shipment',
    'Procurement & Logistics',
    'PO Unit Cost + Freight Premium + Demurrage Charges',
    '(po.qty_ordered * prt.unit_cost_usd) + COALESCE(shp.demurrage_usd, 0)',
    '["supplier", "part", "carrier", "plant", "transport_mode"]'
);
