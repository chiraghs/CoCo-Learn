from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.schemas import FacilityCreate, FacilityOverview, SkuInventoryItem, DockBayItem, ShipmentTracking
from app.snowflake_store import FACILITIES_DB, INVENTORY_DB, DOCKS_DB, SHIPMENT_STEPPER_DB

router = APIRouter(prefix="/api/facilities", tags=["Facilities"])

@router.get("", response_model=List[Dict[str, Any]])
def list_facilities():
    """List all onboarded facilities across regions."""
    return list(FACILITIES_DB.values())

@router.get("/{plant_id}", response_model=Dict[str, Any])
def get_facility_details(plant_id: str):
    """Retrieve top-level overview and metadata for a specific plant/hub."""
    if plant_id not in FACILITIES_DB:
        raise HTTPException(status_code=404, detail=f"Facility '{plant_id}' not found.")
    return FACILITIES_DB[plant_id]

@router.post("", response_model=Dict[str, Any])
def onboard_facility(payload: FacilityCreate):
    """
    Onboard ANY new plant, depot, or hub dynamically.
    Immediately creates spatial, dock, and inventory records.
    """
    if payload.plant_id in FACILITIES_DB:
        raise HTTPException(status_code=400, detail=f"Facility with ID '{payload.plant_id}' already exists.")

    new_facility = {
        "plant_id": payload.plant_id,
        "plant_name": payload.plant_name,
        "facility_type": payload.facility_type,
        "location": payload.location,
        "region": payload.region,
        "daily_burn_rate_units": payload.daily_burn_rate_units,
        "total_capacity_units": payload.total_capacity_units,
        "stock_on_hand": int(payload.total_capacity_units * 0.5), # initial 50% fill
        "capacity_full_pct": 50.0,
        "active_inbound_trucks": 1,
        "total_dock_bays": payload.total_dock_bays,
        "busy_dock_bays": 1,
        "overall_status": "Operational",
        "latitude": payload.latitude,
        "longitude": payload.longitude,
        "on_time_delivery_pct": 98.0,
        "forklift_fleet_active": "1/2 working",
        "forklift_status": "FL-01 Standby in Staging Area (100%)"
    }

    FACILITIES_DB[payload.plant_id] = new_facility

    # Seed initial generic SKUs for the new plant
    INVENTORY_DB[payload.plant_id] = [
        {"part_id": f"SKU_{payload.plant_id}_01", "part_name": "Primary Standard Material (A)", "part_number": "MAT-STD-01", "category": "Core", "criticality": "HIGH", "on_hand_qty": 950, "safety_stock_qty": 400, "days_of_inventory": 14.5, "status": "In Stock"},
        {"part_id": f"SKU_{payload.plant_id}_02", "part_name": "Auxiliary Packaging Pallet", "part_number": "MAT-AUX-02", "category": "Packaging", "criticality": "STANDARD", "on_hand_qty": 350, "safety_stock_qty": 200, "days_of_inventory": 11.2, "status": "In Stock"}
    ]

    # Seed dock bays
    DOCKS_DB[payload.plant_id] = [
        {"dock_id": f"DOCK_{payload.plant_id}_01", "bay_number": 1, "status": "Available", "assigned_truck_id": None, "assigned_carrier": None, "progress": None, "eta_minutes": None},
        {"dock_id": f"DOCK_{payload.plant_id}_02", "bay_number": 2, "status": "En route", "assigned_truck_id": f"TRK-{payload.plant_id[-4:]}", "assigned_carrier": "Regional Logistics", "progress": "Approaching", "eta_minutes": 15}
    ]

    # Seed shipment stepper
    SHIPMENT_STEPPER_DB[payload.plant_id] = {
        "shipment_id": f"#SHP-{payload.plant_id[-4:]}-01",
        "carrier_name": "Regional Logistics",
        "truck_id": f"TRK-{payload.plant_id[-4:]}",
        "destination": payload.location,
        "status": "In Transit",
        "current_step": 3,
        "steps": [
            {"step_index": 1, "label": "Order Confirmed", "timestamp": "08:00", "completed": True},
            {"step_index": 2, "label": "Picked", "timestamp": "09:30", "completed": True},
            {"step_index": 3, "label": "Loading 2/6", "timestamp": "ETA 10:15", "completed": False, "active": True},
            {"step_index": 4, "label": "In Transit", "timestamp": "ETA 11:00", "completed": False},
            {"step_index": 5, "label": "Delivered", "timestamp": "ETA 11:45", "completed": False}
        ],
        "bay_info": f"Bay 1 • Scheduled Arrival in 15 min"
    }

    return new_facility

@router.get("/{plant_id}/inventory", response_model=List[Dict[str, Any]])
def get_facility_inventory(plant_id: str):
    """Retrieve SKU inventory status for the facility (In Stock, Low Stock, Critical)."""
    if plant_id not in INVENTORY_DB:
        raise HTTPException(status_code=404, detail=f"No inventory records for '{plant_id}'.")
    return INVENTORY_DB[plant_id]

@router.get("/{plant_id}/docks", response_model=List[Dict[str, Any]])
def get_facility_docks(plant_id: str):
    """Retrieve loading bays status, active trucks, and ETA for the facility."""
    if plant_id not in DOCKS_DB:
        raise HTTPException(status_code=404, detail=f"No dock records for '{plant_id}'.")
    return DOCKS_DB[plant_id]

@router.get("/{plant_id}/shipment-tracker", response_model=Dict[str, Any])
def get_facility_shipment_tracker(plant_id: str):
    """Retrieve active shipment progress pipeline stepper for the facility."""
    if plant_id not in SHIPMENT_STEPPER_DB:
        raise HTTPException(status_code=404, detail=f"No active shipment tracker for '{plant_id}'.")
    return SHIPMENT_STEPPER_DB[plant_id]
