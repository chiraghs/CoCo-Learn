-- ============================================================================
-- DEPLOY STREAMLIT IN SNOWFLAKE (SiS)
-- Deploys the interactive Supply Chain Command Center inside Snowflake
-- ============================================================================

USE DATABASE SUPPLY_CHAIN_DB;
USE SCHEMA SUPPLY_CHAIN_DB.CORE;

-- 1. Create a stage for the Streamlit code
CREATE STAGE IF NOT EXISTS STREAMLIT_STAGE
    DIRECTORY = (ENABLE = TRUE);

-- 2. Once app/app.py is uploaded to @STREAMLIT_STAGE:
CREATE OR REPLACE STREAMLIT SUPPLY_CHAIN_COMMAND_CENTER
    ROOT_LOCATION = '@SUPPLY_CHAIN_DB.CORE.STREAMLIT_STAGE'
    MAIN_FILE = 'app.py'
    QUERY_WAREHOUSE = 'COMPUTE_WH'
    TITLE = 'Snowflake CoCo Supply Chain Command Center';

SELECT 'SUCCESS: Streamlit app configured in SUPPLY_CHAIN_DB.CORE' AS STATUS;
