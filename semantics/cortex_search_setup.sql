-- ============================================================================
-- CORTEX SEARCH SERVICE SETUP FOR UNSTRUCTURED CONTRACT INTELLIGENCE
-- Enables semantic vector retrieval over supplier contracts, MSAs, and SLA penalty clauses
-- ============================================================================

USE DATABASE SUPPLY_CHAIN_DB;
USE SCHEMA SUPPLY_CHAIN_DB.CORE;

-- Stage for uploading semantic model yaml
CREATE STAGE IF NOT EXISTS SEMANTIC_MODELS_STAGE
    DIRECTORY = (ENABLE = TRUE);

-- Create Cortex Search Service over RAW_SUPPLIER_CONTRACTS
CREATE OR REPLACE CORTEX SEARCH SERVICE SUPPLIER_CONTRACTS_SEARCH
    ON contract_text
    ATTRIBUTES supplier_id, title
    WAREHOUSE = COMPUTE_WH
    TARGET_LAG = '1 hour'
    AS (
        SELECT 
            contract_id, 
            supplier_id, 
            title, 
            contract_text
        FROM SUPPLY_CHAIN_DB.CORE.RAW_SUPPLIER_CONTRACTS
    );

SELECT 'SUCCESS: CORTEX SEARCH SERVICE SUPPLIER_CONTRACTS_SEARCH created' AS STATUS;
