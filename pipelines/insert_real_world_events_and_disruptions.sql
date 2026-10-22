-- ============================================================================
-- SUPPLYCHAINIQ: REAL-WORLD CRISIS EVENTS & DISRUPTIONS PIPELINE
-- Run this in Snowflake Worksheets or tell CoCo in Snowflake to execute it.
-- Ground truth for:
--  1. Red Sea / Suez Canal Shipping Crisis (Cape of Good Hope Diversions)
--  2. Port of Long Beach / LA Pier G Berth Congestion (Austin Battery Shortfall)
--  3. Apex Battery Master Service Agreement Section 8.2 SLA Liquidated Damages
--  4. Port of Baltimore Key Bridge Collapse & East Coast Drayage Reroute
--  5. TSMC Hsinchu Wafer Allocation Throttle (Automotive MCU Lead Time Spike)
-- ============================================================================

USE ROLE ACCOUNTADMIN;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE SUPPLY_CHAIN_DB;
USE SCHEMA CORE;

-- 1. Ensure SHIPMENTS table supports full tracking attributes
CREATE TABLE IF NOT EXISTS SUPPLY_CHAIN_DB.CORE.SHIPMENTS (
    shipment_id VARCHAR(50) PRIMARY KEY,
    po_id VARCHAR(50),
    carrier VARCHAR(100),
    origin_node VARCHAR(100),
    origin_port VARCHAR(100),
    destination_plant VARCHAR(100),
    dest_plant_id VARCHAR(50),
    part_id VARCHAR(50),
    part_name VARCHAR(150),
    quantity NUMBER(12, 2),
    transit_mode VARCHAR(50),
    eta_scheduled TIMESTAMP_NTZ,
    eta_projected TIMESTAMP_NTZ,
    delay_days NUMBER(6, 1),
    shipment_status VARCHAR(50),
    demurrage_usd NUMBER(12, 2),
    root_cause_event VARCHAR(255),
    geo_coordinates VARCHAR(100),
    last_updated TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- 2. Insert / Overwrite Real-World Crisis Shipments
MERGE INTO SUPPLY_CHAIN_DB.CORE.SHIPMENTS AS target
USING (
    SELECT 
        'SHP-SUEZ-992' AS shipment_id,
        'PO-8812' AS po_id,
        'Maersk Line (Triple-E)' AS carrier,
        'Shanghai Deepwater Terminal' AS origin_node,
        'Bab-el-Mandeb Strait' AS origin_port,
        'Munich Mechatronics Hub' AS destination_plant,
        'PLANT_MUNICH_01' AS dest_plant_id,
        'PART_INV_901' AS part_id,
        'High-Efficiency Power Inverters' AS part_name,
        1200 AS quantity,
        'MARITIME_DIVERT' AS transit_mode,
        DATEADD(day, -4, CURRENT_TIMESTAMP()) AS eta_scheduled,
        DATEADD(day, 8, CURRENT_TIMESTAMP()) AS eta_projected,
        12.0 AS delay_days,
        'DIVERTED_CAPE_GOOD_HOPE' AS shipment_status,
        85000.00 AS demurrage_usd,
        'Red Sea / Suez Canal Crisis: Rerouted around Cape of Good Hope (+4,500 nm)' AS root_cause_event,
        '34.35° S, 18.47° E (South Africa Coast)' AS geo_coordinates

    UNION ALL

    SELECT 
        'SHP-78442' AS shipment_id,
        'PO-9412' AS po_id,
        'Pacific Horizon Shipping' AS carrier,
        'Shenzhen Yantian Terminal' AS origin_node,
        'Port of Long Beach (Pier G)' AS origin_port,
        'Austin Gigafactory' AS destination_plant,
        'PLANT_02' AS dest_plant_id,
        'PART_BAT_402' AS part_id,
        '4680 High-Density Battery Cells' AS part_name,
        2280 AS quantity,
        'MARITIME' AS transit_mode,
        DATEADD(day, -14, CURRENT_TIMESTAMP()) AS eta_scheduled,
        DATEADD(day, 2, CURRENT_TIMESTAMP()) AS eta_projected,
        14.0 AS delay_days,
        'CRITICAL_PORT_CONGESTION' AS shipment_status,
        140000.00 AS demurrage_usd,
        'Port of Long Beach outer anchorage congestion (22 container vessels idling)' AS root_cause_event,
        '33.75° N, 118.19° W (San Pedro Bay)' AS geo_coordinates

    UNION ALL

    SELECT 
        'SHP-BALT-104' AS shipment_id,
        'PO-7731' AS po_id,
        'Atlantic Intermodal Express' AS carrier,
        'Bremerhaven Auto Port' AS origin_node,
        'Port of Virginia (Norfolk Divert)' AS origin_port,
        'Detroit Powertrain Plant' AS destination_plant,
        'PLANT_01' AS dest_plant_id,
        'PART_STP_301' AS part_id,
        'High-Tensile Chassis Stampings' AS part_name,
        3400 AS quantity,
        'INTERMODAL_RAIL' AS transit_mode,
        DATEADD(day, -2, CURRENT_TIMESTAMP()) AS eta_scheduled,
        DATEADD(day, 4, CURRENT_TIMESTAMP()) AS eta_projected,
        6.0 AS delay_days,
        'PORT_DIVERT_DRAYAGE' AS shipment_status,
        28000.00 AS demurrage_usd,
        'Baltimore Francis Scott Key Bridge Collapse: Vessel redirected to Norfolk; drayage delayed' AS root_cause_event,
        '36.95° N, 76.33° W (Hampton Roads)' AS geo_coordinates

    UNION ALL

    SELECT 
        'SHP-TSMC-501' AS shipment_id,
        'PO-6620' AS po_id,
        'EVA Air Cargo' AS carrier,
        'Taipei Taoyuan Cargo Hub' AS origin_node,
        'Hsinchu Science Park' AS origin_port,
        'Riverside Smart Logistics Hub' AS destination_plant,
        'WH_RIVERSIDE_01' AS dest_plant_id,
        'PART_MCU_505' AS part_id,
        '5nm Automotive Microcontrollers (ECU)' AS part_name,
        5000 AS quantity,
        'AIR_CARGO' AS transit_mode,
        DATEADD(day, -1, CURRENT_TIMESTAMP()) AS eta_scheduled,
        DATEADD(day, 17, CURRENT_TIMESTAMP()) AS eta_projected,
        18.0 AS delay_days,
        'FAB_ALLOCATION_THROTTLE' AS shipment_status,
        0.00 AS demurrage_usd,
        'Taiwan Fab Seismic Safety Interlock: Cleanroom wafer tool recalibration throttles allocation 15%' AS root_cause_event,
        '24.78° N, 120.99° E (Hsinchu)' AS geo_coordinates
) AS src
ON target.shipment_id = src.shipment_id
WHEN MATCHED THEN UPDATE SET
    target.delay_days = src.delay_days,
    target.shipment_status = src.shipment_status,
    target.demurrage_usd = src.demurrage_usd,
    target.root_cause_event = src.root_cause_event,
    target.geo_coordinates = src.geo_coordinates,
    target.last_updated = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN INSERT (
    shipment_id, po_id, carrier, origin_node, origin_port, destination_plant,
    dest_plant_id, part_id, part_name, quantity, transit_mode, eta_scheduled,
    eta_projected, delay_days, shipment_status, demurrage_usd, root_cause_event,
    geo_coordinates, last_updated
) VALUES (
    src.shipment_id, src.po_id, src.carrier, src.origin_node, src.origin_port, src.destination_plant,
    src.dest_plant_id, src.part_id, src.part_name, src.quantity, src.transit_mode, src.eta_scheduled,
    src.eta_projected, src.delay_days, src.shipment_status, src.demurrage_usd, src.root_cause_event,
    src.geo_coordinates, CURRENT_TIMESTAMP()
);

-- 3. Upsert Contract Clauses into Vectorized Contracts Table
MERGE INTO SUPPLY_CHAIN_DB.CORE.SUPPLIER_CONTRACTS AS target
USING (
    SELECT 
        'CTR_APEX_2024' AS contract_id,
        'SUP_001' AS supplier_id,
        'Apex Battery Cells Ltd' AS supplier_name,
        'Section 8.2 (Liquidated Damages for Inbound Delays)' AS clause_ref,
        'In the event of unexcused inbound consignment delays exceeding a seventy-two (72) hour grace period, Seller shall pay liquidated damages of 5% of order value plus $10,000 per calendar day of delay thereafter. For PO-9412 (14 days delayed past 3-day grace period = 11 billable days), total enforceable damages equal $140,000.00 USD.' AS clause_text,
        10000.00 AS daily_penalty_usd,
        3 AS grace_period_days,
        140000.00 AS total_enforceable_damages_usd

    UNION ALL

    SELECT 
        'CTR_MAERSK_2024' AS contract_id,
        'SUP_004' AS supplier_id,
        'Maersk Line Maritime' AS carrier_name,
        'Section 14.4 (Force Majeure & Geopolitical Route Divert Caps)' AS clause_ref,
        'When war risk zones or maritime blockades necessitate Cape of Good Hope transit, bunker adjustment factor (BAF) surcharge is capped at $45,000 per 1,000 TEU. Excess transit costs above threshold are absorbed by carrier under international maritime insurance clause.' AS clause_text,
        5000.00 AS daily_penalty_usd,
        5 AS grace_period_days,
        85000.00 AS total_enforceable_damages_usd
) AS src
ON target.contract_id = src.contract_id
WHEN MATCHED THEN UPDATE SET
    target.clause_text = src.clause_text,
    target.daily_penalty_usd = src.daily_penalty_usd,
    target.total_enforceable_damages_usd = src.total_enforceable_damages_usd
WHEN NOT MATCHED THEN INSERT (
    contract_id, supplier_id, supplier_name, clause_ref, clause_text,
    daily_penalty_usd, grace_period_days, total_enforceable_damages_usd
) VALUES (
    src.contract_id, src.supplier_id, src.supplier_name, src.clause_ref, src.clause_text,
    src.daily_penalty_usd, src.grace_period_days, src.total_enforceable_damages_usd
);

-- 4. Recreate & Resume DT_ACTIVE_DISRUPTIONS Dynamic Table
CREATE OR REPLACE DYNAMIC TABLE SUPPLY_CHAIN_DB.CORE.DT_ACTIVE_DISRUPTIONS
TARGET_LAG = '1 MINUTE'
WAREHOUSE = COMPUTE_WH
AS
SELECT 
    s.shipment_id,
    s.carrier,
    s.origin_port,
    s.destination_plant,
    s.dest_plant_id,
    s.part_id,
    s.part_name,
    s.quantity,
    s.delay_days,
    s.shipment_status,
    s.demurrage_usd,
    s.root_cause_event,
    s.geo_coordinates,
    CASE 
        WHEN s.delay_days >= 10 THEN 'CRITICAL_DISRUPTION'
        WHEN s.delay_days >= 5 THEN 'MODERATE_WARNING'
        ELSE 'LOW_RISK'
    END AS severity_level,
    CURRENT_TIMESTAMP() AS last_reconciled
FROM SUPPLY_CHAIN_DB.CORE.SHIPMENTS s
WHERE s.delay_days > 0;

ALTER DYNAMIC TABLE SUPPLY_CHAIN_DB.CORE.DT_ACTIVE_DISRUPTIONS RESUME;

-- 5. Verification Query
SELECT 
    shipment_id, 
    carrier, 
    origin_port, 
    destination_plant, 
    delay_days, 
    demurrage_usd, 
    shipment_status,
    severity_level
FROM SUPPLY_CHAIN_DB.CORE.DT_ACTIVE_DISRUPTIONS
ORDER BY delay_days DESC;
