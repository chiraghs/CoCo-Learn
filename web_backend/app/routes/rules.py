from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.schemas import ConfigRule, RuleUpdate
from app.snowflake_store import RULES_DB, INVENTORY_DB

router = APIRouter(prefix="/api/rules", tags=["Rules Engine"])

@router.get("", response_model=List[Dict[str, Any]])
def list_rules():
    """List all active configurable business rules and parameters."""
    return list(RULES_DB.values())

@router.get("/{rule_id}", response_model=Dict[str, Any])
def get_rule(rule_id: str):
    """Retrieve details for a specific threshold rule."""
    if rule_id not in RULES_DB:
        raise HTTPException(status_code=404, detail=f"Rule '{rule_id}' not found.")
    return RULES_DB[rule_id]

@router.put("/{rule_id}", response_model=Dict[str, Any])
def update_rule(rule_id: str, payload: RuleUpdate):
    """
    Update rule parameters dynamically in real time.
    Re-evaluates inventory status across all onboarded facilities.
    """
    if rule_id not in RULES_DB:
        raise HTTPException(status_code=404, detail=f"Rule '{rule_id}' not found.")

    rule = RULES_DB[rule_id]
    rule["parameters"].update(payload.parameters)
    if payload.is_active is not None:
        rule["is_active"] = payload.is_active

    # Re-evaluate inventory across all plants based on new critical_doi and warning_doi
    if "critical_doi" in rule["parameters"] and "warning_doi" in rule["parameters"]:
        crit_doi = float(rule["parameters"]["critical_doi"])
        warn_doi = float(rule["parameters"]["warning_doi"])
        
        for plant_id, items in INVENTORY_DB.items():
            for itm in items:
                doi = itm["days_of_inventory"]
                if doi < crit_doi:
                    itm["status"] = "Critical Stockout"
                elif doi < warn_doi:
                    itm["status"] = "Low Stock"
                else:
                    itm["status"] = "In Stock"

    return rule

@router.post("/simulate", response_model=Dict[str, Any])
def simulate_rule_change(proposed_parameters: Dict[str, Any]):
    """
    Dry-run preview: Simulates how many SKUs flip to Low Stock / Critical
    if thresholds are changed, without persisting to state.
    """
    crit_doi = float(proposed_parameters.get("critical_doi", 5.0))
    warn_doi = float(proposed_parameters.get("warning_doi", 10.0))

    critical_count = 0
    warning_count = 0
    healthy_count = 0
    affected_facilities = set()

    for plant_id, items in INVENTORY_DB.items():
        for itm in items:
            doi = itm["days_of_inventory"]
            if doi < crit_doi:
                critical_count += 1
                affected_facilities.add(plant_id)
            elif doi < warn_doi:
                warning_count += 1
                affected_facilities.add(plant_id)
            else:
                healthy_count += 1

    return {
        "critical_skus": critical_count,
        "warning_skus": warning_count,
        "healthy_skus": healthy_count,
        "affected_facilities_count": len(affected_facilities),
        "affected_facility_ids": list(affected_facilities)
    }
