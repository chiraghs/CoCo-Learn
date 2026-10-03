-- ============================================================================
-- COCO TEST SUITE: GOVERNED ONTOLOGY VALIDATION & ACCURACY TESTS
-- Phase 4: Testing & Validation
-- ============================================================================

USE DATABASE SUPPLY_CHAIN_DB;
USE SCHEMA SUPPLY_CHAIN_DB.CORE;

-- TEST 1: Verify Referential Integrity between Orders, Suppliers, and Parts
SELECT 
    'TEST 1: Foreign Key Integrity' AS TEST_NAME,
    COUNT(*) AS ORPHAN_RECORDS,
    CASE WHEN COUNT(*) = 0 THEN 'PASSED' ELSE 'FAILED' END AS TEST_STATUS
FROM FACT_PURCHASE_ORDERS po
LEFT JOIN DIM_SUPPLIERS s ON po.supplier_id = s.supplier_id
LEFT JOIN DIM_PARTS p ON po.part_id = p.part_id
WHERE s.supplier_id IS NULL OR p.part_id IS NULL;

-- TEST 2: Canonical Metric Accuracy - Austin Battery Days of Inventory (DOI)
-- Must match exactly 2280 on-hand / 600 burn rate = 3.8 days
SELECT 
    'TEST 2: Canonical DOI Metric (Plant 2 Battery)' AS TEST_NAME,
    days_of_inventory,
    stockout_risk_level,
    CASE 
        WHEN days_of_inventory = 3.8 AND stockout_risk_level = 'CRITICAL_STOCKOUT_RISK' 
        THEN 'PASSED' 
        ELSE 'FAILED' 
    END AS TEST_STATUS
FROM DT_PLANT_STOCKOUT_RISK
WHERE plant_id = 'PLANT_02' AND part_id = 'PART_BAT_402';

-- TEST 3: Governed Liquidated Damages Calculation Accuracy (Apex Battery Cells)
-- Apex delay days must correctly deduct 3-day SLA grace period
SELECT 
    'TEST 3: Legal Penalty Calculation (Apex Battery Cells)' AS TEST_NAME,
    supplier_name,
    total_penalty_liability_usd,
    CASE 
        WHEN total_penalty_liability_usd = 18000.00 THEN 'PASSED' 
        ELSE 'FAILED' 
    END AS TEST_STATUS
FROM DT_SUPPLIER_PERFORMANCE
WHERE supplier_id = 'SUP_001';

-- TEST 4: Boundary Validation - OTIF % must always be between 0 and 100
SELECT 
    'TEST 4: OTIF Boundary Check' AS TEST_NAME,
    MIN(otif_rate_pct) AS MIN_OTIF,
    MAX(otif_rate_pct) AS MAX_OTIF,
    CASE 
        WHEN MIN(otif_rate_pct) >= 0.0 AND MAX(otif_rate_pct) <= 100.0 
        THEN 'PASSED' 
        ELSE 'FAILED' 
    END AS TEST_STATUS
FROM DT_SUPPLIER_PERFORMANCE;
