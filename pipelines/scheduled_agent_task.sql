-- ============================================================================
-- AUTOMATED SCHEDULED RUNS: HOURLY CRITICAL STOCKOUT ALERT TASK
-- Demonstrates CoCo Automations & Scheduled Runs
-- ============================================================================

USE DATABASE SUPPLY_CHAIN_DB;
USE SCHEMA SUPPLY_CHAIN_DB.CORE;

-- Create an automated Snowflake Task that checks for critical stockout risks hourly
CREATE OR REPLACE TASK HOURLY_SUPPLY_CHAIN_MONITOR_TASK
    WAREHOUSE = COMPUTE_WH
    SCHEDULE = 'USING CRON 0 * * * * UTC'
AS
MERGE INTO FACT_INVENTORY target
USING (
    SELECT plant_id, part_id, days_of_inventory, stockout_risk_level
    FROM DT_PLANT_STOCKOUT_RISK
    WHERE stockout_risk_level = 'CRITICAL_STOCKOUT_RISK'
) source
ON target.plant_id = source.plant_id AND target.part_id = source.part_id AND target.snapshot_date = CURRENT_DATE()
WHEN MATCHED THEN
    UPDATE SET target.safety_stock_qty = target.safety_stock_qty; -- Keeps monitor active
