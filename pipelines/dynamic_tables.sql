-- ============================================================================
-- SUPPLY CHAIN ONTOLOGY: NEAR REAL-TIME DYNAMIC TABLES
-- Transforms raw transactional feeds into governed near real-time analytical feeds
-- ============================================================================

USE DATABASE SUPPLY_CHAIN_DB;
USE SCHEMA SUPPLY_CHAIN_DB.CORE;

-- 1. DYNAMIC TABLE: DT_SUPPLIER_PERFORMANCE
-- Aggregates real-time delivery reliability, delay days, and liquidated damages liability
CREATE OR REPLACE DYNAMIC TABLE DT_SUPPLIER_PERFORMANCE
    TARGET_LAG = '1 MINUTE'
    WAREHOUSE = COMPUTE_WH
AS
SELECT 
    s.supplier_id,
    s.name AS supplier_name,
    s.country AS supplier_country,
    s.tier AS supplier_tier,
    COUNT(DISTINCT po.po_id) AS total_orders,
    COUNT(DISTINCT shp.shipment_id) AS total_shipments,
    
    -- On-Time Shipments (arrived on or before promised delivery date)
    COUNT(DISTINCT CASE 
        WHEN shp.actual_arrival_date IS NOT NULL AND shp.actual_arrival_date <= po.promised_delivery_date 
        THEN shp.shipment_id 
    END) AS on_time_shipments,
    
    -- Delayed Shipments
    COUNT(DISTINCT CASE 
        WHEN (shp.actual_arrival_date > po.promised_delivery_date) 
          OR (shp.actual_arrival_date IS NULL AND CURRENT_DATE() > po.promised_delivery_date) 
        THEN shp.shipment_id 
    END) AS delayed_shipments,
    
    -- Governed OTIF Rate (%)
    ROUND(
        COUNT(DISTINCT CASE 
            WHEN shp.actual_arrival_date <= po.promised_delivery_date 
             AND shp.qty_received >= po.qty_ordered 
            THEN shp.shipment_id 
        END) * 100.0 / NULLIF(COUNT(DISTINCT shp.shipment_id), 0), 
        1
    ) AS otif_rate_pct,
    
    -- Total Delay Days across all orders
    SUM(GREATEST(0, DATEDIFF(day, po.promised_delivery_date, COALESCE(shp.actual_arrival_date, CURRENT_DATE())))) AS total_delay_days,
    
    -- Governed Liquidated Damages Liability ($)
    -- Formula: Daily Damages * max(0, delay_days - grace_days)
    SUM(
        s.daily_liquidated_damages_usd * 
        GREATEST(0, DATEDIFF(day, po.promised_delivery_date, COALESCE(shp.actual_arrival_date, CURRENT_DATE())) - s.contract_sla_grace_days)
    ) AS total_penalty_liability_usd,
    
    SUM(COALESCE(shp.demurrage_usd, 0)) AS total_demurrage_usd

FROM DIM_SUPPLIERS s
JOIN FACT_PURCHASE_ORDERS po ON s.supplier_id = po.supplier_id
LEFT JOIN FACT_SHIPMENTS shp ON po.po_id = shp.po_id
GROUP BY 
    s.supplier_id, s.name, s.country, s.tier, s.daily_liquidated_damages_usd, s.contract_sla_grace_days;


-- 2. DYNAMIC TABLE: DT_PLANT_STOCKOUT_RISK
-- Computes real-time Days of Inventory (DOI) and flags assembly line disruption risks
CREATE OR REPLACE DYNAMIC TABLE DT_PLANT_STOCKOUT_RISK
    TARGET_LAG = '1 MINUTE'
    WAREHOUSE = COMPUTE_WH
AS
SELECT 
    inv.snapshot_date,
    p.plant_id,
    p.name AS plant_name,
    p.location AS plant_location,
    prt.part_id,
    prt.part_number,
    prt.name AS part_name,
    prt.category AS part_category,
    prt.criticality AS part_criticality,
    
    inv.on_hand_qty,
    inv.safety_stock_qty,
    inv.in_transit_qty,
    p.daily_burn_rate_units AS plant_daily_burn_rate,
    
    -- Canonical Metric: Days of Inventory (DOI)
    ROUND(inv.on_hand_qty * 1.0 / NULLIF(p.daily_burn_rate_units, 0), 1) AS days_of_inventory,
    
    -- Risk Classification
    CASE 
        WHEN (inv.on_hand_qty * 1.0 / NULLIF(p.daily_burn_rate_units, 0)) < 5.0 THEN 'CRITICAL_STOCKOUT_RISK'
        WHEN (inv.on_hand_qty * 1.0 / NULLIF(p.daily_burn_rate_units, 0)) < 10.0 THEN 'ELEVATED_WARNING'
        ELSE 'HEALTHY_BUFFER'
    END AS stockout_risk_level,
    
    -- Safety Stock Deficit
    GREATEST(0, inv.safety_stock_qty - inv.on_hand_qty) AS safety_stock_deficit_units

FROM FACT_INVENTORY inv
JOIN DIM_PLANTS p ON inv.plant_id = p.plant_id
JOIN DIM_PARTS prt ON inv.part_id = prt.part_id;


-- 3. DYNAMIC TABLE: DT_ACTIVE_DISRUPTIONS
-- Real-time situational awareness on delayed shipments stuck at ports
CREATE OR REPLACE DYNAMIC TABLE DT_ACTIVE_DISRUPTIONS
    TARGET_LAG = '1 MINUTE'
    WAREHOUSE = COMPUTE_WH
AS
SELECT 
    shp.shipment_id,
    shp.carrier,
    shp.transport_mode,
    shp.origin_port,
    shp.dest_port,
    shp.shipment_status,
    shp.qty_shipped,
    shp.demurrage_usd,
    po.po_id,
    po.promised_delivery_date,
    prt.part_id,
    prt.part_number,
    prt.name AS part_name,
    prt.criticality AS part_criticality,
    sup.supplier_id,
    sup.name AS supplier_name,
    pl.plant_id,
    pl.name AS destination_plant,
    
    -- Days past promised arrival
    GREATEST(0, DATEDIFF(day, po.promised_delivery_date, COALESCE(shp.actual_arrival_date, CURRENT_DATE()))) AS days_past_promised

FROM FACT_SHIPMENTS shp
JOIN FACT_PURCHASE_ORDERS po ON shp.po_id = po.po_id
JOIN DIM_PARTS prt ON po.part_id = prt.part_id
JOIN DIM_SUPPLIERS sup ON po.supplier_id = sup.supplier_id
JOIN DIM_PLANTS pl ON po.dest_plant_id = pl.plant_id
WHERE shp.shipment_status IN ('PORT_BOTTLENECK', 'HELD_AT_PORT', 'ARRIVED_LATE', 'DELAYED_IN_TRANSIT');
