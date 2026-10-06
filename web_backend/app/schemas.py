from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class FacilityCreate(BaseModel):
    plant_id: str = Field(..., example="WH_RIVERSIDE_01")
    plant_name: str = Field(..., example="Riverside Hub")
    facility_type: str = Field(default="WAREHOUSE_DEPOT", example="WAREHOUSE_DEPOT")
    location: str = Field(..., example="12 Riverside Dr, Newark NJ")
    region: str = Field(default="AMER", example="AMER")
    daily_burn_rate_units: float = Field(default=500.0, example=600.0)
    total_capacity_units: int = Field(default=1800, example=1800)
    total_dock_bays: int = Field(default=2, example=2)
    latitude: Optional[float] = 40.7357
    longitude: Optional[float] = -74.1724

class FacilityOverview(BaseModel):
    plant_id: str
    plant_name: str
    facility_type: str
    location: str
    region: str
    daily_burn_rate_units: float
    total_capacity_units: int
    stock_on_hand: int
    capacity_full_pct: float
    active_inbound_trucks: int
    total_dock_bays: int
    busy_dock_bays: int
    overall_status: str # OPERATIONAL, WARNING, CRITICAL

class SkuInventoryItem(BaseModel):
    part_id: str
    part_name: str
    part_number: str
    category: str
    criticality: str
    on_hand_qty: int
    safety_stock_qty: int
    days_of_inventory: float
    status: str # In Stock, Low Stock, Critical Stockout

class DockBayItem(BaseModel):
    dock_id: str
    bay_number: int
    status: str # Loading, Available, Docked, En route
    assigned_truck_id: Optional[str] = None
    assigned_carrier: Optional[str] = None
    progress: Optional[str] = "2/6"
    eta_minutes: Optional[int] = None

class ShipmentTracking(BaseModel):
    shipment_id: str
    carrier_name: str
    truck_id: str
    destination: str
    status: str # Order Confirmed, Picked, Loading, In Transit, Delivered
    current_step: int # 1 to 5
    eta_time: str
    has_disruption: bool = False
    disruption_notes: Optional[str] = None

class ConfigRule(BaseModel):
    rule_id: str
    rule_name: str
    rule_category: str
    scope: str
    parameters: Dict[str, Any]
    is_active: bool

class RuleUpdate(BaseModel):
    parameters: Dict[str, Any]
    is_active: Optional[bool] = None

class CortexQueryRequest(BaseModel):
    query: str
    plant_id: Optional[str] = None

class CortexQueryResponse(BaseModel):
    query: str
    explanation: str
    generated_sql: str
    ground_truth_data: List[Dict[str, Any]]
    reconciliation_verified: bool

class ActionMcpRequest(BaseModel):
    action_type: str = "REROUTE_PURCHASE_ORDER"
    plant_id: str
    part_id: str
    po_id: str
    target_supplier_id: str
    delivery_mode: str = "EXPEDITED_AIR_FREIGHT"
