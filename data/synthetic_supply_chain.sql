-- ============================================================================
-- SUPPLY CHAIN ONTOLOGY: SYNTHETIC SEED & DDL
-- Scenario: High-Tech / EV Assembly (Austin, Fremont, Berlin)
-- Crisis: Port bottleneck delaying Battery Module PART_BAT_402 bound for Austin
-- ============================================================================

CREATE DATABASE IF NOT EXISTS SUPPLY_CHAIN_DB;
CREATE SCHEMA IF NOT EXISTS SUPPLY_CHAIN_DB.CORE;
USE DATABASE SUPPLY_CHAIN_DB;
USE SCHEMA SUPPLY_CHAIN_DB.CORE;

-- 1. DIM_SUPPLIERS
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
('SUP_001', 'Apex Battery Cells Ltd', 'South Korea', 'Tier 1', 25, 3, 1500.00),
('SUP_002', 'MicroSilicon Dynamics', 'Taiwan', 'Tier 1', 30, 2, 2000.00),
('SUP_003', 'Nordic Precision Metals', 'Sweden', 'Tier 2', 15, 5, 500.00),
('SUP_004', 'VoltStorage Chem Inc', 'Japan', 'Tier 1', 28, 3, 1800.00),
('SUP_005', 'Pacific Wiring & Harness', 'Vietnam', 'Tier 2', 18, 4, 600.00);

-- 2. DIM_PARTS
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
('PART_MET_012', 'MET-BRK-012', 'Lightweight Stamped Aluminum Bracket', 'Structural', 'LOW', 18.50, 'SUP_003'),
('PART_SEN_804', 'SEN-LID-804', 'Autonomous Navigation LiDAR Unit', 'Electronics', 'HIGH', 650.00, 'SUP_002'),
('PART_CLD_202', 'CLD-RAD-202', 'Thermal Battery Cooling Radiator', 'Cooling', 'MEDIUM', 110.00, 'SUP_003'),
('PART_CEL_400', 'CEL-CYL-2170', 'Cylindrical Energy Cell Sub-Assembly', 'Powertrain', 'CRITICAL', 15.00, 'SUP_001'),
('PART_ACT_606', 'ACT-STE-606', 'Drive-by-Wire Steering Actuator', 'Chassis', 'HIGH', 230.00, 'SUP_004'),
('PART_CON_099', 'CON-AMP-099', 'Fast-Charge Power Connector Assembly', 'Electrical', 'MEDIUM', 35.00, 'SUP_005');

-- 3. DIM_PLANTS
CREATE OR REPLACE TABLE DIM_PLANTS (
    plant_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100),
    location VARCHAR(50),
    country VARCHAR(50),
    daily_burn_rate_units INT,
    daily_target_output INT
);

INSERT INTO DIM_PLANTS VALUES
('PLANT_01', 'Gigafactory California', 'Fremont', 'USA', 450, 450),
('PLANT_02', 'Gigafactory Texas', 'Austin', 'USA', 600, 600),
('PLANT_03', 'Gigafactory Europe', 'Berlin', 'Germany', 400, 400);

-- 4. FACT_PURCHASE_ORDERS
CREATE OR REPLACE TABLE FACT_PURCHASE_ORDERS (
    po_id VARCHAR(20) PRIMARY KEY,
    supplier_id VARCHAR(20),
    part_id VARCHAR(20),
    dest_plant_id VARCHAR(20),
    order_date DATE,
    promised_delivery_date DATE,
    qty_ordered INT,
    po_status VARCHAR(30)
);

INSERT INTO FACT_PURCHASE_ORDERS VALUES
('PO_2026_001', 'SUP_001', 'PART_BAT_402', 'PLANT_02', '2026-08-15', '2026-09-15', 5000, 'DELIVERED_LATE'),
('PO_2026_002', 'SUP_001', 'PART_BAT_402', 'PLANT_02', '2026-08-25', '2026-09-25', 6000, 'DELAYED_IN_TRANSIT'),
('PO_2026_003', 'SUP_001', 'PART_BAT_402', 'PLANT_01', '2026-08-20', '2026-09-20', 4000, 'DELIVERED_ON_TIME'),
('PO_2026_004', 'SUP_002', 'PART_MCU_901', 'PLANT_02', '2026-08-10', '2026-09-12', 15000, 'DELIVERED_ON_TIME'),
('PO_2026_005', 'SUP_002', 'PART_MCU_901', 'PLANT_03', '2026-08-18', '2026-09-20', 12000, 'DELIVERED_ON_TIME'),
('PO_2026_006', 'SUP_004', 'PART_INV_300', 'PLANT_02', '2026-08-12', '2026-09-16', 3000, 'DELIVERED_ON_TIME'),
('PO_2026_007', 'SUP_005', 'PART_HAR_105', 'PLANT_02', '2026-08-22', '2026-09-15', 8000, 'DELIVERED_ON_TIME'),
('PO_2026_008', 'SUP_003', 'PART_MET_012', 'PLANT_01', '2026-08-28', '2026-09-18', 10000, 'DELIVERED_ON_TIME'),
('PO_2026_009', 'SUP_001', 'PART_CEL_400', 'PLANT_03', '2026-08-20', '2026-09-22', 25000, 'DELIVERED_LATE'),
('PO_2026_010', 'SUP_002', 'PART_SEN_804', 'PLANT_02', '2026-08-25', '2026-09-26', 2500, 'DELIVERED_ON_TIME'),
('PO_2026_011', 'SUP_001', 'PART_BAT_402', 'PLANT_02', '2026-09-01', '2026-10-01', 7500, 'SEVERELY_DELAYED'),
('PO_2026_012', 'SUP_003', 'PART_CLD_202', 'PLANT_02', '2026-08-30', '2026-09-22', 4000, 'DELIVERED_ON_TIME'),
('PO_2026_013', 'SUP_004', 'PART_ACT_606', 'PLANT_01', '2026-09-02', '2026-09-28', 3500, 'DELIVERED_ON_TIME'),
('PO_2026_014', 'SUP_005', 'PART_CON_099', 'PLANT_03', '2026-08-26', '2026-09-20', 12000, 'DELIVERED_ON_TIME'),
('PO_2026_015', 'SUP_001', 'PART_BAT_402', 'PLANT_03', '2026-08-29', '2026-09-29', 5500, 'DELIVERED_ON_TIME');

-- 5. FACT_SHIPMENTS
CREATE OR REPLACE TABLE FACT_SHIPMENTS (
    shipment_id VARCHAR(20) PRIMARY KEY,
    po_id VARCHAR(20),
    carrier VARCHAR(50),
    transport_mode VARCHAR(20),
    origin_port VARCHAR(50),
    dest_port VARCHAR(50),
    etd DATE,
    eta DATE,
    actual_arrival_date DATE,
    qty_shipped INT,
    qty_received INT,
    demurrage_usd DECIMAL(10,2),
    shipment_status VARCHAR(30)
);

INSERT INTO FACT_SHIPMENTS VALUES
('SHP_9001', 'PO_2026_001', 'OceanBridge Logistics', 'Ocean', 'Busan, KR', 'Houston, US', '2026-08-18', '2026-09-15', '2026-09-24', 5000, 4950, 4800.00, 'ARRIVED_LATE'),
('SHP_9002', 'PO_2026_002', 'Pacific Freight Lines', 'Ocean', 'Busan, KR', 'Houston, US', '2026-08-27', '2026-09-25', NULL, 6000, 0, 7500.00, 'HELD_AT_PORT'),
('SHP_9003', 'PO_2026_003', 'OceanBridge Logistics', 'Ocean', 'Busan, KR', 'Oakland, US', '2026-08-22', '2026-09-20', '2026-09-19', 4000, 4000, 0.00, 'COMPLETED'),
('SHP_9004', 'PO_2026_004', 'Global Aero Air Cargo', 'Air', 'Taipei, TW', 'Dallas, US', '2026-08-11', '2026-08-15', '2026-08-15', 15000, 15000, 0.00, 'COMPLETED'),
('SHP_9005', 'PO_2026_005', 'Global Aero Air Cargo', 'Air', 'Taipei, TW', 'Frankfurt, DE', '2026-08-19', '2026-08-23', '2026-08-23', 12000, 12000, 0.00, 'COMPLETED'),
('SHP_9006', 'PO_2026_006', 'BlueSea Express', 'Ocean', 'Yokohama, JP', 'Houston, US', '2026-08-14', '2026-09-14', '2026-09-14', 3000, 3000, 0.00, 'COMPLETED'),
('SHP_9007', 'PO_2026_007', 'Mekong Maritime', 'Ocean', 'Haiphong, VN', 'Houston, US', '2026-08-24', '2026-09-14', '2026-09-15', 8000, 8000, 0.00, 'COMPLETED'),
('SHP_9008', 'PO_2026_008', 'Nordic Rail Cargo', 'Rail', 'Gothenburg, SE', 'Rotterdam, NL', '2026-08-29', '2026-09-08', '2026-09-07', 10000, 10000, 0.00, 'COMPLETED'),
('SHP_9009', 'PO_2026_009', 'OceanBridge Logistics', 'Ocean', 'Busan, KR', 'Hamburg, DE', '2026-08-22', '2026-09-22', '2026-09-29', 25000, 24800, 3200.00, 'ARRIVED_LATE'),
('SHP_9010', 'PO_2026_010', 'Global Aero Air Cargo', 'Air', 'Taipei, TW', 'Dallas, US', '2026-08-26', '2026-08-30', '2026-08-30', 2500, 2500, 0.00, 'COMPLETED'),
('SHP_9011', 'PO_2026_011', 'Pacific Freight Lines', 'Ocean', 'Busan, KR', 'Houston, US', '2026-09-03', '2026-10-01', NULL, 7500, 0, 12000.00, 'PORT_BOTTLENECK'),
('SHP_9012', 'PO_2026_012', 'Nordic Rail Cargo', 'Rail', 'Gothenburg, SE', 'Houston, US', '2026-08-31', '2026-09-20', '2026-09-20', 4000, 4000, 0.00, 'COMPLETED'),
('SHP_9013', 'PO_2026_013', 'BlueSea Express', 'Ocean', 'Yokohama, JP', 'Oakland, US', '2026-09-04', '2026-09-26', '2026-09-26', 3500, 3500, 0.00, 'COMPLETED'),
('SHP_9014', 'PO_2026_014', 'Mekong Maritime', 'Ocean', 'Haiphong, VN', 'Rotterdam, NL', '2026-08-28', '2026-09-18', '2026-09-19', 12000, 12000, 0.00, 'COMPLETED'),
('SHP_9015', 'PO_2026_015', 'OceanBridge Logistics', 'Ocean', 'Busan, KR', 'Hamburg, DE', '2026-08-31', '2026-09-29', '2026-09-29', 5500, 5500, 0.00, 'COMPLETED');

-- 6. FACT_INVENTORY (Daily Snapshots - Austin Battery Stock is Critical)
CREATE OR REPLACE TABLE FACT_INVENTORY (
    snapshot_date DATE,
    plant_id VARCHAR(20),
    part_id VARCHAR(20),
    on_hand_qty INT,
    safety_stock_qty INT,
    in_transit_qty INT,
    PRIMARY KEY (snapshot_date, plant_id, part_id)
);

INSERT INTO FACT_INVENTORY VALUES
('2026-10-01', 'PLANT_02', 'PART_BAT_402', 2280, 5000, 13500), -- 2280 / 600 daily burn = 3.8 DAYS OF INVENTORY (CRITICAL RISK!)
('2026-10-01', 'PLANT_01', 'PART_BAT_402', 6800, 4500, 4000),  -- Fremont has surplus buffer
('2026-10-01', 'PLANT_03', 'PART_BAT_402', 5200, 3500, 5500),
('2026-10-01', 'PLANT_02', 'PART_MCU_901', 18500, 10000, 15000),
('2026-10-01', 'PLANT_02', 'PART_INV_300', 4200, 2500, 3000),
('2026-10-01', 'PLANT_02', 'PART_HAR_105', 9600, 6000, 8000),
('2026-10-01', 'PLANT_01', 'PART_MCU_901', 14000, 8000, 12000),
('2026-10-01', 'PLANT_03', 'PART_MCU_901', 11500, 7000, 12000);

-- 7. RAW_SUPPLIER_CONTRACTS (Unstructured Contract Clauses for Cortex RAG)
CREATE OR REPLACE TABLE RAW_SUPPLIER_CONTRACTS (
    contract_id VARCHAR(20) PRIMARY KEY,
    supplier_id VARCHAR(20),
    title VARCHAR(200),
    effective_date DATE,
    contract_text VARCHAR
);

INSERT INTO RAW_SUPPLIER_CONTRACTS VALUES
('CTR_APEX_2025', 'SUP_001', 'Master Service Agreement: Apex Battery Cells Ltd', '2025-01-01',
'MASTER SERVICES & SUPPLY AGREEMENT - APEX BATTERY CELLS LTD.
SECTION 5: DELIVERY TERMS & LEAD TIMES
Supplier guarantees a baseline lead time of 25 calendar days for all high-density battery cell shipments (PART_BAT_402).
SECTION 8: SERVICE LEVEL AGREEMENTS & DELAY PENALTIES
8.1 Grace Period: Buyer agrees to a 3-calendar-day grace period for port congestion beyond promised delivery date.
8.2 Liquidated Damages: If shipment delivery exceeds the promised delivery date plus grace period, Supplier shall incur liquidated damages of USD $1,500.00 per calendar day per delayed shipment until actual receipt at designated facility.
8.3 Force Majeure: Delays resulting from certified government embargoes or catastrophic weather shall toll penalties, provided Supplier furnishes notarized documentation within 48 hours of occurrence. Routine port terminal berth congestion does not qualify as Force Majeure.'),

('CTR_MICRO_2025', 'SUP_002', 'Master Supply Agreement: MicroSilicon Dynamics', '2025-02-01',
'MASTER SUPPLY AGREEMENT - MICROSILICON DYNAMICS.
SECTION 4: AIR FREIGHT COMMITMENTS
All automotive microcontroller units (PART_MCU_901) must be dispatched via Tier-1 Air Freight carriers.
SECTION 7: PENALTY CLAUSES
7.1 Liquidated damages for unapproved delivery delays are assessed at USD $2,000.00 per day after a 48-hour grace window.'),

('CTR_VOLT_2025', 'SUP_004', 'Master Supply Agreement: VoltStorage Chem Inc', '2025-03-01',
'MASTER SUPPLY AGREEMENT - VOLTSTORAGE CHEM INC.
SECTION 6: DELAY PENALTIES & EXPEDITED FREIGHT
Supplier agrees to reimburse all expedited air freight premiums if ocean shipments fall behind schedule by more than 5 days. Daily liquidated damages are USD $1,800.00 per delayed consignment.');

SELECT 'SUCCESS: Synthetic Supply Chain data seeded into SUPPLY_CHAIN_DB.CORE' AS STATUS;
