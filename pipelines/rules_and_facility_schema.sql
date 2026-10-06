-- ============================================================================
-- SUPPLY CHAIN ONTOLOGY: EXTENSION FOR GENERIC FACILITY ONBOARDING & RULES
-- Enables onboarding ANY plant/depot and configurable threshold rules
-- ============================================================================

USE DATABASE SUPPLY_CHAIN_DB;
USE SCHEMA SUPPLY_CHAIN_DB.CORE;

-- 1. CONFIG_RULES: Declarative Enterprise Business Rules
CREATE TABLE IF NOT EXISTS CONFIG_RULES (
    rule_id VARCHAR(50) PRIMARY KEY,
    rule_name VARCHAR(100) NOT NULL,
    rule_category VARCHAR(50) NOT NULL, -- INVENTORY_BUFFER, DOCK_UTILIZATION, SUPPLIER_OTIF
    scope VARCHAR(50) DEFAULT 'GLOBAL',  -- GLOBAL, REGIONAL, PLANT_SPECIFIC
    parameters VARIANT NOT NULL,        -- JSON thresholds e.g. {"critical_doi": 5.0, "warning_doi": 10.0}
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Seed default global rules if empty
MERGE INTO CONFIG_RULES tgt
USING (
    SELECT 'RULE_DOI_GLOBAL' AS rule_id, 
           'Global Stockout DOI Thresholds' AS rule_name, 
           'INVENTORY_BUFFER' AS rule_category, 
           'GLOBAL' AS scope, 
           PARSE_JSON('{"critical_doi": 5.0, "warning_doi": 10.0, "low_stock_ratio": 0.25}') AS parameters, 
           TRUE AS is_active
) src
ON tgt.rule_id = src.rule_id
WHEN NOT MATCHED THEN INSERT (rule_id, rule_name, rule_category, scope, parameters, is_active)
VALUES (src.rule_id, src.rule_name, src.rule_category, src.scope, src.parameters, src.is_active);

-- 2. PLANT_RULE_BINDINGS: Facility-Specific Threshold Overrides
CREATE TABLE IF NOT EXISTS PLANT_RULE_BINDINGS (
    binding_id VARCHAR(50) PRIMARY KEY,
    plant_id VARCHAR(50) REFERENCES DIM_PLANTS(plant_id),
    rule_id VARCHAR(50) REFERENCES CONFIG_RULES(rule_id),
    custom_overrides VARIANT, -- Optional JSON override
    is_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- 3. FACILITY_DOCKS: Loading bays and live telemetry per facility
CREATE TABLE IF NOT EXISTS FACILITY_DOCKS (
    dock_id VARCHAR(50) PRIMARY KEY,
    plant_id VARCHAR(50) REFERENCES DIM_PLANTS(plant_id),
    bay_number INT NOT NULL,
    status VARCHAR(30) DEFAULT 'AVAILABLE', -- DOCKED, LOADING, UNLOADING, AVAILABLE, MAINTENANCE
    assigned_truck_id VARCHAR(50),
    assigned_shipment_id VARCHAR(50),
    eta_minutes INT,
    last_updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- 4. FACILITY_SHIPMENTS: Live inbound / outbound progress tracker (Stepper)
CREATE TABLE IF NOT EXISTS FACILITY_SHIPMENTS (
    shipment_id VARCHAR(50) PRIMARY KEY,
    plant_id VARCHAR(50) REFERENCES DIM_PLANTS(plant_id),
    carrier_name VARCHAR(100),
    truck_id VARCHAR(50),
    destination_or_origin VARCHAR(100),
    status VARCHAR(50) DEFAULT 'IN_TRANSIT', -- ORDER_CONFIRMED, PICKED, LOADING, IN_TRANSIT, DELIVERED
    current_step INT DEFAULT 3, -- 1 to 5
    eta_minutes INT DEFAULT 15,
    has_disruption BOOLEAN DEFAULT FALSE,
    disruption_notes VARCHAR(255),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
