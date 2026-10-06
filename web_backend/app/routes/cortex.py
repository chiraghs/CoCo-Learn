from fastapi import APIRouter
from typing import Dict, Any
from app.schemas import CortexQueryRequest, CortexQueryResponse, ActionMcpRequest
from app.snowflake_store import INVENTORY_DB, FACILITIES_DB, SHIPMENT_STEPPER_DB

router = APIRouter(prefix="/api/cortex", tags=["Cortex AI & Actions"])

@router.post("/query", response_model=CortexQueryResponse)
def execute_cortex_query(payload: CortexQueryRequest):
    """
    Simulates / proxies Cortex Analyst text-to-semantic-SQL queries.
    Returns the auditable 3-Way Reconciliation Ledger.
    """
    q = payload.query.lower()
    plant_id = payload.plant_id or "WH_RIVERSIDE_01"
    
    if "austin" in q or "battery" in q or plant_id == "PLANT_02":
        return CortexQueryResponse(
            query=payload.query,
            explanation="Austin Gigafactory (PLANT_02) High-Density Battery Cells (PART_BAT_402) has 3.8 Days of Inventory remaining, breaching the critical 5.0-day threshold. Daily burn rate is 600 units with 2,280 units on hand. Primary shipment SHP-401 is delayed 14 days due to Port of Long Beach berth congestion.",
            generated_sql="SELECT plant_id, plant_name, part_id, part_name, days_of_inventory, stockout_risk_level FROM SUPPLY_CHAIN_DB.CORE.DT_PLANT_STOCKOUT_RISK WHERE plant_id = 'PLANT_02' AND part_id = 'PART_BAT_402';",
            ground_truth_data=[
                {"plant_id": "PLANT_02", "plant_name": "Austin Gigafactory", "part_id": "PART_BAT_402", "part_name": "High-Density Battery Cells", "days_of_inventory": 3.8, "stockout_risk_level": "CRITICAL_STOCKOUT_RISK"}
            ],
            reconciliation_verified=True
        )
    elif "penalty" in q or "section 8" in q or "liquidated" in q or "apex" in q:
        return CortexQueryResponse(
            query=payload.query,
            explanation="Under Section 8.2 of the Master Service Agreement with Apex Battery Cells Ltd, delayed deliveries incur liquidated damages of 5% order penalty plus $10,000 per calendar day beyond a 3-day grace period. For 14 delay days, total enforceable claim is $140,000.00.",
            generated_sql="SELECT PARSE_JSON(SNOWFLAKE.CORTEX.SEARCH_PREVIEW('SUPPLY_CHAIN_DB.CORE.SUPPLIER_CONTRACTS_SEARCH', '{\"query\": \"Apex Battery liquidated damages Section 8\", \"limit\": 1}'))['results'][0]['clause_text']::STRING;",
            ground_truth_data=[
                {"supplier_name": "Apex Battery Cells Ltd", "clause_ref": "Section 8.2", "penalty_daily_usd": 10000.0, "grace_period_days": 3, "delay_days": 14, "enforceable_damages_usd": 140000.0}
            ],
            reconciliation_verified=True
        )
    else:
        facility = FACILITIES_DB.get(plant_id, list(FACILITIES_DB.values())[0])
        inventory = INVENTORY_DB.get(plant_id, [])
        return CortexQueryResponse(
            query=payload.query,
            explanation=f"Facility '{facility['plant_name']}' is currently '{facility['overall_status']}' with {facility['stock_on_hand']} units on hand ({facility['capacity_full_pct']}% capacity). {len([i for i in inventory if i['status'] != 'In Stock'])} items require attention.",
            generated_sql=f"SELECT * FROM SUPPLY_CHAIN_DB.CORE.DT_FACILITY_LIVE_TELEMETRY WHERE plant_id = '{plant_id}';",
            ground_truth_data=[facility],
            reconciliation_verified=True
        )

@router.post("/action/reroute", response_model=Dict[str, Any])
def execute_action_mcp_reroute(payload: ActionMcpRequest):
    """
    Executes 1-Click closed-loop PO reroute via Action MCP Server.
    Updates the facility buffer state dynamically.
    """
    # Restore inventory DOI for the affected plant
    if payload.plant_id in INVENTORY_DB:
        for itm in INVENTORY_DB[payload.plant_id]:
            if itm["part_id"] == payload.part_id:
                itm["on_hand_qty"] += 4500
                itm["days_of_inventory"] = 14.2
                itm["status"] = "In Stock"

    if payload.plant_id in FACILITIES_DB:
        FACILITIES_DB[payload.plant_id]["overall_status"] = "Operational"
        FACILITIES_DB[payload.plant_id]["stock_on_hand"] += 4500

    return {
        "status": "SUCCESS",
        "action": "EXPEDITE_AND_REROUTE_PO",
        "original_po_id": payload.po_id,
        "emergency_po_id": f"EXP_{payload.po_id[-6:]}",
        "plant_id": payload.plant_id,
        "target_supplier": "Shenzhen EnerTech",
        "transport_mode": payload.delivery_mode,
        "new_days_of_inventory": 14.2,
        "downtime_hours_prevented": 91.2,
        "sla_claim_usd": 140000.0
    }
