-- ============================================================================
-- SUPPLYCHAINIQ: COMPLETE END-TO-END SNOWFLAKE DEPLOYMENT SCRIPT
-- Database, Schemas, Dimensions, Facts, Crisis Data, 5-Layer Ontology,
-- Recursive Closure Hierarchy, Real-Time Dynamic Tables & Cortex Search
-- ============================================================================

-- 1. DATABASE & SCHEMAS
CREATE DATABASE IF NOT EXISTS SUPPLY_CHAIN_DB;
CREATE SCHEMA IF NOT EXISTS SUPPLY_CHAIN_DB.CORE;
CREATE SCHEMA IF NOT EXISTS SUPPLY_CHAIN_DB.ONT;

USE DATABASE SUPPLY_CHAIN_DB;
USE SCHEMA SUPPLY_CHAIN_DB.CORE;

-- 2. DIMENSION TABLES
CREATE OR REPLACE TABLE DIM_SUPPLIERS (
    supplier_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100),
    country VARCHAR(50),
    tier VARCHAR(10),
    default_lead_time_days INT,
    contract_sla_grace_days INT,
    daily_liquidated_damages_usd DECIMAL(10,2)
);

INSERT INTO DIM_SUPPLIERS VALUES
('SUP_001', 'Apex Battery Cells Ltd', 'South Korea', 'Tier 1', 25, 3, 10000.00),
('SUP_002', 'MicroSilicon Dynamics', 'Taiwan', 'Tier 1', 30, 2, 2000.00),
('SUP_003', 'Nordic Precision Metals', 'Sweden', 'Tier 2', 15, 5, 500.00),
('SUP_004', 'VoltStorage Chem Inc', 'Japan', 'Tier 1', 28, 3, 1800.00),
('SUP_005', 'Pacific Wiring & Harness', 'Vietnam', 'Tier 2', 18, 4, 600.00),
('SUP_006', 'Shenzhen EnerTech Ltd', 'China', 'Tier 1', 5, 1, 2500.00);

CREATE OR REPLACE TABLE DIM_PARTS (
    part_id VARCHAR(20) PRIMARY KEY,
    part_number VARCHAR(50),
    name VARCHAR(100),
    category VARCHAR(50),
    criticality VARCHAR(20),
    unit_cost_usd DECIMAL(10,2),
    primary_supplier_id VARCHAR(20)
);

INSERT INTO DIM_PARTS VALUES
('PART_BAT_402', 'BAT-MOD-402', 'High-Density Lithium Battery Module', 'Powertrain', 'CRITICAL', 850.00, 'SUP_001'),
('PART_MCU_901', 'MCU-901-AUTO', 'Automotive Multi-Core Microcontroller', 'Electronics', 'CRITICAL', 45.00, 'SUP_002'),
('PART_INV_300', 'INV-ACDC-300', 'High-Voltage Traction Inverter', 'Powertrain', 'HIGH', 420.00, 'SUP_004'),
('PART_HAR_105', 'HAR-HV-105', 'High-Voltage Wiring Harness', 'Electrical', 'MEDIUM', 85.00, 'SUP_005'),
('PART_MET_012', 'MET-BRK-012', 'Lightweight Stamped Aluminum Bracket', 'Structural', 'LOW', 18.50, 'SUP_003');

CREATE OR REPLACE TABLE DIM_PLANTS (
    plant_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100),
    location VARCHAR(100),
    country VARCHAR(50),
    facility_type VARCHAR(50),
    floor_area_sqm INT,
    daily_capacity_units INT,
    active_shifts INT
);

INSERT INTO DIM_PLANTS VALUES
('PLANT_02', 'Austin Gigafactory 1', 'Austin, TX', 'United States', 'Assembly & Cell Pack', 85000, 2000, 3),
('PLANT_01', 'Fremont Assembly Plant', 'Fremont, CA', 'United States', 'Automotive Assembly', 65000, 1500, 3),
('PLANT_03', 'Berlin Gigafactory 4', 'Brandenburg', 'Germany', 'Powertrain & Drive', 72000, 1800, 3),
('WH_RIVERSIDE_01', 'Riverside Smart Hub', 'Newark, NJ', 'United States', 'Automated ASRS Hub', 45000, 5000, 3);

-- 3. FACT TABLES & CRISIS DATA (Austin Battery Shortfall: 3.8 Days DOI)
CREATE OR REPLACE TABLE FACT_INVENTORY (
    inventory_id VARCHAR(36) PRIMARY KEY,
    plant_id VARCHAR(20),
    part_id VARCHAR(20),
    on_hand_qty INT,
    daily_burn_rate DECIMAL(10,2),
    safety_stock_qty INT,
    snapshot_date DATE DEFAULT CURRENT_DATE()
);

INSERT INTO FACT_INVENTORY VALUES
('INV_001', 'PLANT_02', 'PART_BAT_402', 2280, 600.00, 3000, CURRENT_DATE()),
('INV_002', 'PLANT_02', 'PART_MCU_901', 9400, 400.00, 2000, CURRENT_DATE()),
('INV_003', 'WH_RIVERSIDE_01', 'PART_BAT_402', 1412, 100.00, 500, CURRENT_DATE()),
('INV_004', 'PLANT_01', 'PART_BAT_402', 4800, 450.00, 1500, CURRENT_DATE());

CREATE OR REPLACE TABLE FACT_PURCHASE_ORDERS (
    po_id VARCHAR(20) PRIMARY KEY,
    supplier_id VARCHAR(20),
    part_id VARCHAR(20),
    dest_plant_id VARCHAR(20),
    qty_ordered INT,
    order_date DATE,
    promised_delivery_date DATE,
    status VARCHAR(30),
    po_status VARCHAR(30)
);

INSERT INTO FACT_PURCHASE_ORDERS VALUES
('PO_401', 'SUP_001', 'PART_BAT_402', 'PLANT_02', 5000, DATEADD(day, -30, CURRENT_DATE()), DATEADD(day, -14, CURRENT_DATE()), 'DELAYED', 'DELAYED');

CREATE OR REPLACE TABLE FACT_SHIPMENTS (
    shipment_id VARCHAR(20) PRIMARY KEY,
    po_id VARCHAR(20),
    origin_node_id VARCHAR(20),
    destination_plant_id VARCHAR(20),
    carrier VARCHAR(50),
    carrier_name VARCHAR(100),
    transport_mode VARCHAR(20),
    shipping_mode VARCHAR(20),
    origin_port VARCHAR(50),
    dest_port VARCHAR(50),
    qty_shipped INT,
    qty_received INT,
    demurrage_usd DECIMAL(10,2),
    dispatch_date DATE,
    expected_arrival_date DATE,
    actual_arrival_date DATE,
    status VARCHAR(20),
    shipment_status VARCHAR(30)
);

INSERT INTO FACT_SHIPMENTS VALUES
('SHP_401', 'PO_401', 'SUP_001', 'PLANT_02', 'Pacific Maritime TRK-2051', 'Pacific Maritime TRK-2051', 'Ocean', 'OCEAN_FREIGHT', 'Busan, KR', 'Long Beach, US', 5000, 0, 14000.00, DATEADD(day, -25, CURRENT_DATE()), DATEADD(day, -14, CURRENT_DATE()), NULL, 'DELAYED_IN_PORT', 'PORT_BOTTLENECK');

-- 4. CONTRACT INTELLIGENCE (For Cortex Search Legal Mining)
CREATE OR REPLACE TABLE RAW_SUPPLIER_CONTRACTS (
    contract_id VARCHAR(20) PRIMARY KEY,
    supplier_id VARCHAR(20),
    title VARCHAR(200),
    contract_text TEXT
);

INSERT INTO RAW_SUPPLIER_CONTRACTS VALUES
('CTR_APEX_2024', 'SUP_001', 'Master Supply Agreement - Apex Battery Cells Ltd',
'MASTER PURCHASE AGREEMENT (2024-2027)
BETWEEN: Global Automotive Manufacturing Corp AND Apex Battery Cells Ltd (Supplier).
SECTION 8: SERVICE LEVEL AGREEMENTS & DELAY LIQUIDATED DAMAGES
8.1 Delivery Timeliness: The Supplier shall ensure 100% on-time dispatch for all High-Density Lithium Battery Modules (PART_BAT_402).
8.2 Liquidated Damages for Inbound Delays: In the event of a shipment delay exceeding the three (3) business day grace period, the Supplier shall be strictly liable to pay liquidated damages of five percent (5%) base contract penalty plus USD $10,000.00 per calendar day for each day of delay until full delivery at the designated destination plant.
8.3 Mitigation and Expedited Air Freight: The Buyer reserves the unconditional right to procure emergency substitute modules from alternate approved suppliers (including Shenzhen EnerTech) and bill back all differential freight and procurement costs to Apex Battery Cells Ltd.');

-- 5. ONTOLOGY HIERARCHY, TAXONOMY & RECURSIVE CLOSURE
CREATE OR REPLACE TABLE SUPPLY_CHAIN_DB.ONT.ONT_CLASS (
    CLASS_NAME VARCHAR(100) PRIMARY KEY,
    PARENT_CLASS VARCHAR(100),
    IS_ABSTRACT BOOLEAN DEFAULT FALSE,
    DESCRIPTION VARCHAR(500)
);

INSERT INTO SUPPLY_CHAIN_DB.ONT.ONT_CLASS VALUES
('SupplyChainNode', NULL, TRUE, 'Abstract root grouping for all physical locations'),
('Facility', 'SupplyChainNode', TRUE, 'Operational physical facility'),
('Warehouse', 'Facility', FALSE, 'Storage location holding inventory'),
('BondedWarehouse', 'Warehouse', FALSE, 'Customs-bonded warehouse for imported goods'),
('ColdStorage', 'Warehouse', FALSE, 'Temperature-controlled storage for batteries and chemicals'),
('Plant', 'Facility', FALSE, 'Assembly or gigafactory manufacturing plant'),
('SupplierNode', 'SupplyChainNode', FALSE, 'Tier-1/Tier-2 vendor origin node'),
('Inventory', NULL, FALSE, 'Stock level of a part/SKU held at a physical node'),
('Capacity', NULL, FALSE, 'Throughput or storage limit'),
('Shipment', NULL, FALSE, 'Movement of goods between nodes');

CREATE OR REPLACE TABLE SUPPLY_CHAIN_DB.ONT.CLASS_CLOSURE AS
WITH RECURSIVE hierarchy AS (
    SELECT CLASS_NAME AS ANCESTOR, CLASS_NAME AS DESCENDANT, 0 AS DEPTH
    FROM SUPPLY_CHAIN_DB.ONT.ONT_CLASS
    UNION ALL
    SELECT h.ANCESTOR, c.CLASS_NAME AS DESCENDANT, h.DEPTH + 1
    FROM hierarchy h
    JOIN SUPPLY_CHAIN_DB.ONT.ONT_CLASS c ON c.PARENT_CLASS = h.DESCENDANT
)
SELECT ANCESTOR, DESCENDANT, DEPTH FROM hierarchy;

CREATE OR REPLACE FUNCTION SUPPLY_CHAIN_DB.ONT.GET_SUBCLASSES(root_class VARCHAR)
RETURNS TABLE (subclass_name VARCHAR, depth INT)
AS
$$
    SELECT DESCENDANT AS subclass_name, DEPTH
    FROM SUPPLY_CHAIN_DB.ONT.CLASS_CLOSURE
    WHERE ANCESTOR = root_class AND DEPTH > 0
$$;

-- 6. REAL-TIME DYNAMIC TABLES (10-minute lag for optimal credit efficiency)
CREATE OR REPLACE DYNAMIC TABLE SUPPLY_CHAIN_DB.CORE.DT_SUPPLIER_PERFORMANCE
    TARGET_LAG = '10 MINUTES'
    WAREHOUSE = COMPUTE_WH
AS
SELECT 
    s.supplier_id,
    s.name AS supplier_name,
    s.country AS supplier_country,
    s.tier AS supplier_tier,
    COUNT(DISTINCT po.po_id) AS total_orders,
    COUNT(DISTINCT shp.shipment_id) AS total_shipments,
    COALESCE(SUM(DATEDIFF(day, po.promised_delivery_date, CURRENT_DATE())), 0) AS cumulative_delay_days,
    SUM(CASE 
        WHEN DATEDIFF(day, po.promised_delivery_date, CURRENT_DATE()) > s.contract_sla_grace_days 
        THEN (DATEDIFF(day, po.promised_delivery_date, CURRENT_DATE()) - s.contract_sla_grace_days) * s.daily_liquidated_damages_usd
        ELSE 0 
    END) AS total_liquidated_damages_usd
FROM SUPPLY_CHAIN_DB.CORE.DIM_SUPPLIERS s
LEFT JOIN SUPPLY_CHAIN_DB.CORE.FACT_PURCHASE_ORDERS po ON s.supplier_id = po.supplier_id
LEFT JOIN SUPPLY_CHAIN_DB.CORE.FACT_SHIPMENTS shp ON po.po_id = shp.po_id
GROUP BY s.supplier_id, s.name, s.country, s.tier;

CREATE OR REPLACE DYNAMIC TABLE SUPPLY_CHAIN_DB.CORE.DT_PLANT_STOCKOUT_RISK
    TARGET_LAG = '10 MINUTES'
    WAREHOUSE = COMPUTE_WH
AS
SELECT 
    p.plant_id,
    p.name AS plant_name,
    prt.part_id,
    prt.name AS part_name,
    inv.on_hand_qty,
    inv.daily_burn_rate,
    ROUND(inv.on_hand_qty / NULLIF(inv.daily_burn_rate, 0), 1) AS days_of_inventory,
    CASE 
        WHEN (inv.on_hand_qty / NULLIF(inv.daily_burn_rate, 0)) < 5.0 THEN 'CRITICAL_STOCKOUT_RISK'
        WHEN (inv.on_hand_qty / NULLIF(inv.daily_burn_rate, 0)) < 10.0 THEN 'WARNING_LOW_STOCK'
        ELSE 'BALANCED'
    END AS stockout_risk_level
FROM SUPPLY_CHAIN_DB.CORE.FACT_INVENTORY inv
JOIN SUPPLY_CHAIN_DB.CORE.DIM_PLANTS p ON inv.plant_id = p.plant_id
JOIN SUPPLY_CHAIN_DB.CORE.DIM_PARTS prt ON inv.part_id = prt.part_id;

CREATE OR REPLACE DYNAMIC TABLE SUPPLY_CHAIN_DB.CORE.DT_ACTIVE_DISRUPTIONS
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
FROM SUPPLY_CHAIN_DB.CORE.FACT_SHIPMENTS shp
JOIN SUPPLY_CHAIN_DB.CORE.FACT_PURCHASE_ORDERS po ON shp.po_id = po.po_id
JOIN SUPPLY_CHAIN_DB.CORE.DIM_PARTS prt ON po.part_id = prt.part_id
JOIN SUPPLY_CHAIN_DB.CORE.DIM_SUPPLIERS sup ON po.supplier_id = sup.supplier_id
JOIN SUPPLY_CHAIN_DB.CORE.DIM_PLANTS pl ON COALESCE(po.dest_plant_id, shp.destination_plant_id) = pl.plant_id
WHERE COALESCE(shp.shipment_status, shp.status) IN ('PORT_BOTTLENECK', 'HELD_AT_PORT', 'ARRIVED_LATE', 'DELAYED_IN_TRANSIT', 'DELAYED_IN_PORT');

-- 7. CORTEX SEARCH SERVICE
CREATE OR REPLACE CORTEX SEARCH SERVICE SUPPLY_CHAIN_DB.CORE.SUPPLIER_CONTRACTS_SEARCH
    ON contract_text
    ATTRIBUTES supplier_id, title
    WAREHOUSE = COMPUTE_WH
    TARGET_LAG = '1 hour'
    AS (
        SELECT contract_id, supplier_id, title, contract_text
        FROM SUPPLY_CHAIN_DB.CORE.RAW_SUPPLIER_CONTRACTS
    );

SELECT 'SUCCESS: SUPPLY_CHAIN_DB Initialized with All Tables, Dynamic Tables & Cortex Search' AS STATUS;
