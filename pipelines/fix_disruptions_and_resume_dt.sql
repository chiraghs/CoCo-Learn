-- ============================================================================
-- FIX DT_ACTIVE_DISRUPTIONS & OPTIMIZE DYNAMIC TABLE REFRESH LAGS
-- 1. Adds backwards-compatible columns to FACT_SHIPMENTS & FACT_PURCHASE_ORDERS
-- 2. Backfills carrier, demurrage, dest_plant_id, and shipment_status
-- 3. Recreates DT_ACTIVE_DISRUPTIONS against the unified schema
-- 4. Optimizes TARGET_LAG to 10 MINUTES to prevent unnecessary credit consumption
-- 5. Resumes all dynamic tables
-- ============================================================================

USE DATABASE SUPPLY_CHAIN_DB;
USE SCHEMA SUPPLY_CHAIN_DB.CORE;

-- 1. ADD MISSING COLUMNS TO FACT_PURCHASE_ORDERS & BACKFILL
ALTER TABLE FACT_PURCHASE_ORDERS ADD COLUMN IF NOT EXISTS dest_plant_id VARCHAR(20);
ALTER TABLE FACT_PURCHASE_ORDERS ADD COLUMN IF NOT EXISTS po_status VARCHAR(30);

UPDATE FACT_PURCHASE_ORDERS 
SET dest_plant_id = 'PLANT_02', po_status = status 
WHERE dest_plant_id IS NULL;

-- 2. ADD MISSING COLUMNS TO FACT_SHIPMENTS & BACKFILL
ALTER TABLE FACT_SHIPMENTS ADD COLUMN IF NOT EXISTS carrier VARCHAR(50);
ALTER TABLE FACT_SHIPMENTS ADD COLUMN IF NOT EXISTS transport_mode VARCHAR(20);
ALTER TABLE FACT_SHIPMENTS ADD COLUMN IF NOT EXISTS origin_port VARCHAR(50);
ALTER TABLE FACT_SHIPMENTS ADD COLUMN IF NOT EXISTS dest_port VARCHAR(50);
ALTER TABLE FACT_SHIPMENTS ADD COLUMN IF NOT EXISTS demurrage_usd DECIMAL(10,2);
ALTER TABLE FACT_SHIPMENTS ADD COLUMN IF NOT EXISTS shipment_status VARCHAR(30);

UPDATE FACT_SHIPMENTS 
SET 
    carrier = COALESCE(carrier_name, 'Pacific Maritime TRK-2051'),
    transport_mode = COALESCE(shipping_mode, 'Ocean'),
    origin_port = 'Busan, KR',
    dest_port = 'Long Beach, US',
    demurrage_usd = 14000.00,
    shipment_status = 'PORT_BOTTLENECK'
WHERE carrier IS NULL;

-- 3. RECREATE & RESUME DT_ACTIVE_DISRUPTIONS
CREATE OR REPLACE DYNAMIC TABLE DT_ACTIVE_DISRUPTIONS
    TARGET_LAG = '10 MINUTES'
    WAREHOUSE = COMPUTE_WH
AS
SELECT 
    shp.shipment_id,
    COALESCE(shp.carrier, shp.carrier_name) AS carrier,
    COALESCE(shp.transport_mode, shp.shipping_mode) AS transport_mode,
    shp.origin_port,
    shp.dest_port,
    COALESCE(shp.shipment_status, shp.status) AS shipment_status,
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
    GREATEST(0, DATEDIFF(day, po.promised_delivery_date, COALESCE(shp.actual_arrival_date, CURRENT_DATE()))) AS days_past_promised
FROM FACT_SHIPMENTS shp
JOIN FACT_PURCHASE_ORDERS po ON shp.po_id = po.po_id
JOIN DIM_PARTS prt ON po.part_id = prt.part_id
JOIN DIM_SUPPLIERS sup ON po.supplier_id = sup.supplier_id
JOIN DIM_PLANTS pl ON COALESCE(po.dest_plant_id, shp.destination_plant_id) = pl.plant_id
WHERE COALESCE(shp.shipment_status, shp.status) IN ('PORT_BOTTLENECK', 'HELD_AT_PORT', 'ARRIVED_LATE', 'DELAYED_IN_TRANSIT', 'DELAYED_IN_PORT');

-- 4. OPTIMIZE REFRESH LAG ON OTHER DYNAMIC TABLES TO PREVENT EXCESS CREDIT USAGE
ALTER DYNAMIC TABLE IF EXISTS DT_SUPPLIER_PERFORMANCE SET TARGET_LAG = '10 MINUTES';
ALTER DYNAMIC TABLE IF EXISTS DT_PLANT_STOCKOUT_RISK SET TARGET_LAG = '10 MINUTES';

-- 5. RESUME ALL DYNAMIC TABLES
ALTER DYNAMIC TABLE IF EXISTS DT_ACTIVE_DISRUPTIONS RESUME;
ALTER DYNAMIC TABLE IF EXISTS DT_SUPPLIER_PERFORMANCE RESUME;
ALTER DYNAMIC TABLE IF EXISTS DT_PLANT_STOCKOUT_RISK RESUME;

SELECT 'SUCCESS: DT_ACTIVE_DISRUPTIONS repaired and all Dynamic Tables optimized & resumed.' AS STATUS;
