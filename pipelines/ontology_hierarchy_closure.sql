-- ============================================================================
-- SUPPLY CHAIN ONTOLOGY: HIERARCHY, TAXONOMY & RECURSIVE CLOSURE TABLE
-- Implements Anup Moncy's 5-Layer Ontology-Driven Platform on Snowflake
-- Layer 2: Ontology Metadata (ONT_CLASS)
-- Layer 3: Views and Traversal (CLASS_CLOSURE & ONT_OBJECT_SOURCE)
-- Layer 5: Cortex Agent UDFs (GET_SUBCLASSES, GET_FACILITY_RISK, GET_INBOUND_RISK)
-- ============================================================================

USE DATABASE SUPPLY_CHAIN_DB;

-- Create ONT Schema dedicated to Semantic Knowledge & Ontological Taxonomy
CREATE SCHEMA IF NOT EXISTS SUPPLY_CHAIN_DB.ONT;
USE SCHEMA SUPPLY_CHAIN_DB.ONT;

-- ============================================================================
-- LAYER 2: ONTOLOGY METADATA TABLE (Taxonomic Class Definitions & Inheritance)
-- ============================================================================
-- ONT_CLASS records every business concept, its direct parent, abstract flag,
-- and clear definitions. Joins and business metrics live in the Semantic View.
-- This table owns structural inheritance (IS-A relationships).

CREATE OR REPLACE TABLE SUPPLY_CHAIN_DB.ONT.ONT_CLASS (
    CLASS_NAME VARCHAR(100) PRIMARY KEY,
    PARENT_CLASS VARCHAR(100),       -- NULL means root class
    IS_ABSTRACT BOOLEAN DEFAULT FALSE, -- TRUE means semantic grouping without physical rows
    DESCRIPTION VARCHAR(500)
);

-- Seed Canonical Supply Chain Ontology Hierarchy
MERGE INTO SUPPLY_CHAIN_DB.ONT.ONT_CLASS tgt
USING (
    SELECT 'SupplyChainNode' AS CLASS_NAME, NULL AS PARENT_CLASS, TRUE AS IS_ABSTRACT, 'Abstract grouping for all physical supply chain nodes and facilities' AS DESCRIPTION UNION ALL
    SELECT 'Facility', 'SupplyChainNode', TRUE, 'Physical operational facility (Plant, Warehouse, Distribution Center)' UNION ALL
    SELECT 'Warehouse', 'Facility', FALSE, 'Storage node holding raw material or component inventory' UNION ALL
    SELECT 'BondedWarehouse', 'Warehouse', FALSE, 'Customs-bonded warehouse for imported parts; inherits all Warehouse properties' UNION ALL
    SELECT 'ColdStorage', 'Warehouse', FALSE, 'Temperature-controlled storage for sensitive battery chemistry / materials' UNION ALL
    SELECT 'Plant', 'Facility', FALSE, 'Assembly or gigafactory manufacturing facility with active production lines' UNION ALL
    SELECT 'SupplierNode', 'SupplyChainNode', FALSE, 'Tier-1/Tier-2 vendor origin node supplying parts' UNION ALL
    
    -- Inventory Concepts
    SELECT 'Inventory', NULL, FALSE, 'Stock level of a part/SKU held at a physical node' UNION ALL
    SELECT 'BufferSafetyStock', 'Inventory', FALSE, 'Minimum required buffer inventory to prevent assembly line stoppage' UNION ALL
    
    -- Capacity & Processing Concepts
    SELECT 'Capacity', NULL, FALSE, 'Processing throughput or physical storage constraint of a facility' UNION ALL
    SELECT 'ThroughputCapacity', 'Capacity', FALSE, 'Maximum daily assembly or processing rate (burn rate)' UNION ALL
    SELECT 'StorageCapacity', 'Capacity', FALSE, 'Maximum physical unit storage limit' UNION ALL
    SELECT 'DockCapacity', 'Capacity', FALSE, 'Loading bay throughput and turnaround capacity' UNION ALL
    
    -- Logistics & Movement Concepts
    SELECT 'Transportation', NULL, TRUE, 'Abstract grouping for physical movement of goods' UNION ALL
    SELECT 'Route', 'Transportation', FALSE, 'Defined transport lane between origin node and destination node' UNION ALL
    SELECT 'Shipment', 'Transportation', FALSE, 'Consignment of parts in-transit along a route' UNION ALL
    SELECT 'AirFreightShipment', 'Shipment', FALSE, 'Expedited air logistics consignment' UNION ALL
    SELECT 'MaritimeShipment', 'Shipment', FALSE, 'Ocean container freight subject to port congestion and demurrage' UNION ALL
    
    -- Commercial & Contract Governance Concepts
    SELECT 'CommercialContract', NULL, TRUE, 'Governed legal agreements, orders, and contractual SLAs' UNION ALL
    SELECT 'PurchaseOrder', 'CommercialContract', FALSE, 'Commercial purchase order binding supplier delivery commitments' UNION ALL
    SELECT 'MasterServiceAgreement', 'CommercialContract', FALSE, 'Master vendor contract containing SLA grace days and liquidated damages clauses'
) src
ON tgt.CLASS_NAME = src.CLASS_NAME
WHEN MATCHED THEN UPDATE SET 
    tgt.PARENT_CLASS = src.PARENT_CLASS, 
    tgt.IS_ABSTRACT = src.IS_ABSTRACT, 
    tgt.DESCRIPTION = src.DESCRIPTION
WHEN NOT MATCHED THEN INSERT (CLASS_NAME, PARENT_CLASS, IS_ABSTRACT, DESCRIPTION)
VALUES (src.CLASS_NAME, src.PARENT_CLASS, src.IS_ABSTRACT, src.DESCRIPTION);

-- ============================================================================
-- LAYER 3: RECURSIVE TRANSITIVE CLOSURE TABLE & TRAVERSAL
-- ============================================================================
-- Materializes every ancestor-descendant pair from ONT_CLASS with traversal depth.
-- For example, ancestor 'SupplyChainNode' resolves to:
-- Warehouse (depth 2), BondedWarehouse (depth 3), ColdStorage (depth 3), Plant (depth 2), etc.
-- This allows Cortex Analyst and AI Agents to reason over entire concept families!

CREATE OR REPLACE TABLE SUPPLY_CHAIN_DB.ONT.CLASS_CLOSURE AS
WITH RECURSIVE hierarchy AS (
    -- Anchor: Every concept is its own ancestor at depth 0
    SELECT 
        CLASS_NAME AS ancestor, 
        CLASS_NAME AS descendant, 
        0 AS depth
    FROM SUPPLY_CHAIN_DB.ONT.ONT_CLASS
    
    UNION ALL
    
    -- Recursive step: Follow parent-child links down the ontology tree
    SELECT 
        h.ancestor, 
        c.CLASS_NAME AS descendant, 
        h.depth + 1 AS depth
    FROM hierarchy h
    JOIN SUPPLY_CHAIN_DB.ONT.ONT_CLASS c ON c.PARENT_CLASS = h.descendant
)
SELECT ancestor, descendant, depth 
FROM hierarchy;

-- Mapping physical tables to their ontological classes
CREATE OR REPLACE TABLE SUPPLY_CHAIN_DB.ONT.ONT_OBJECT_SOURCE (
    SOURCE_TABLE VARCHAR(200),
    TYPE_VALUE VARCHAR(100),
    CLASS_NAME VARCHAR(100) REFERENCES SUPPLY_CHAIN_DB.ONT.ONT_CLASS(CLASS_NAME),
    PRIMARY KEY (SOURCE_TABLE, TYPE_VALUE)
);

MERGE INTO SUPPLY_CHAIN_DB.ONT.ONT_OBJECT_SOURCE tgt
USING (
    SELECT 'SUPPLY_CHAIN_DB.CORE.DIM_PLANTS' AS SOURCE_TABLE, 'ASSEMBLY_PLANT' AS TYPE_VALUE, 'Plant' AS CLASS_NAME UNION ALL
    SELECT 'SUPPLY_CHAIN_DB.CORE.DIM_PLANTS', 'GIGAFACTORY', 'Plant' UNION ALL
    SELECT 'SUPPLY_CHAIN_DB.CORE.DIM_SUPPLIERS', 'TIER_1', 'SupplierNode' UNION ALL
    SELECT 'SUPPLY_CHAIN_DB.CORE.DIM_SUPPLIERS', 'TIER_2', 'SupplierNode' UNION ALL
    SELECT 'SUPPLY_CHAIN_DB.CORE.FACT_INVENTORY', 'ON_HAND', 'Inventory' UNION ALL
    SELECT 'SUPPLY_CHAIN_DB.CORE.FACT_SHIPMENTS', 'MARITIME', 'MaritimeShipment' UNION ALL
    SELECT 'SUPPLY_CHAIN_DB.CORE.FACT_SHIPMENTS', 'AIR_EXPEDITED', 'AirFreightShipment' UNION ALL
    SELECT 'SUPPLY_CHAIN_DB.CORE.RAW_SUPPLIER_CONTRACTS', 'MSA', 'MasterServiceAgreement'
) src
ON tgt.SOURCE_TABLE = src.SOURCE_TABLE AND tgt.TYPE_VALUE = src.TYPE_VALUE
WHEN MATCHED THEN UPDATE SET tgt.CLASS_NAME = src.CLASS_NAME
WHEN NOT MATCHED THEN INSERT (SOURCE_TABLE, TYPE_VALUE, CLASS_NAME)
VALUES (src.SOURCE_TABLE, src.TYPE_VALUE, src.CLASS_NAME);

-- View unifying physical nodes with ontological inheritance
CREATE OR REPLACE VIEW SUPPLY_CHAIN_DB.ONT.V_UNIFIED_NODES AS
SELECT 
    p.plant_id AS node_id,
    p.name AS node_name,
    p.location,
    'Plant' AS ont_class,
    p.daily_burn_rate_units AS daily_throughput_capacity,
    TRUE AS is_active
FROM SUPPLY_CHAIN_DB.CORE.DIM_PLANTS p
UNION ALL
SELECT 
    s.supplier_id AS node_id,
    s.name AS node_name,
    s.country AS location,
    'SupplierNode' AS ont_class,
    NULL AS daily_throughput_capacity,
    TRUE AS is_active
FROM SUPPLY_CHAIN_DB.CORE.DIM_SUPPLIERS s;

-- ============================================================================
-- LAYER 5: CORTEX AGENT UDF TOOLS
-- ============================================================================

-- Tool 1: Get all subclasses of any concept dynamically
CREATE OR REPLACE FUNCTION SUPPLY_CHAIN_DB.ONT.GET_SUBCLASSES(root_class VARCHAR)
RETURNS TABLE (CLASS_NAME VARCHAR, DEPTH INTEGER)
AS $$
    SELECT descendant, depth 
    FROM SUPPLY_CHAIN_DB.ONT.CLASS_CLOSURE 
    WHERE ancestor = root_class AND depth > 0
$$;

-- Tool 2: Get facility supply risk profile (Days of Inventory, Burn Rate, Deficit)
CREATE OR REPLACE FUNCTION SUPPLY_CHAIN_DB.ONT.GET_FACILITY_RISK(p_plant_id VARCHAR)
RETURNS TABLE (
    PLANT_ID VARCHAR,
    PLANT_NAME VARCHAR,
    PART_NAME VARCHAR,
    ON_HAND_QTY NUMBER,
    DAILY_BURN_RATE NUMBER,
    DAYS_OF_INVENTORY NUMBER,
    RISK_LEVEL VARCHAR
)
AS $$
    SELECT 
        plant_id,
        plant_name,
        part_name,
        on_hand_qty,
        plant_daily_burn_rate,
        days_of_inventory,
        stockout_risk_level
    FROM SUPPLY_CHAIN_DB.CORE.DT_PLANT_STOCKOUT_RISK
    WHERE plant_id = p_plant_id
$$;

-- Tool 3: Get delayed or at-risk inbound shipments into a facility
CREATE OR REPLACE FUNCTION SUPPLY_CHAIN_DB.ONT.GET_INBOUND_RISK(p_plant_id VARCHAR)
RETURNS TABLE (
    SHIPMENT_ID VARCHAR,
    CARRIER VARCHAR,
    DAYS_PAST_PROMISED NUMBER,
    DEMURRAGE_USD NUMBER,
    STATUS VARCHAR
)
AS $$
    SELECT 
        s.shipment_id,
        s.carrier,
        GREATEST(0, DATEDIFF(day, po.promised_delivery_date, COALESCE(s.actual_arrival_date, CURRENT_DATE()))) AS days_past_promised,
        COALESCE(s.demurrage_usd, 0) AS demurrage_usd,
        CASE 
            WHEN s.actual_arrival_date IS NOT NULL THEN 'DELIVERED'
            WHEN CURRENT_DATE() > po.promised_delivery_date THEN 'DELAYED'
            ELSE 'IN_TRANSIT'
        END AS status
    FROM SUPPLY_CHAIN_DB.CORE.FACT_SHIPMENTS s
    JOIN SUPPLY_CHAIN_DB.CORE.FACT_PURCHASE_ORDERS po ON s.po_id = po.po_id
    WHERE s.dest_port = p_plant_id 
       OR po.dest_plant_id = p_plant_id
$$;

SELECT 'SUCCESS: SUPPLY_CHAIN_DB.ONT 5-Layer Ontology & Closure Tables Created' AS STATUS;
