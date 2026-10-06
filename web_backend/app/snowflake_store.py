"""
Generic In-Memory & Snowflake-Backed Unified State Store
Provides high-performance, fault-tolerant state for any onboarded plant,
syncing bidirectionally with Snowflake when credentials exist, and fallback
to high-fidelity mock data if running standalone.
"""

import os
from typing import Dict, List, Any, Optional

# Pre-seeded facilities (Riverside Hub matching reference + Austin Gigafactory + Berlin + Fremont)
FACILITIES_DB: Dict[str, Dict[str, Any]] = {
    "WH_RIVERSIDE_01": {
        "plant_id": "WH_RIVERSIDE_01",
        "plant_name": "Riverside Hub",
        "facility_type": "DEPOT",
        "location": "12 Riverside Dr, Newark NJ",
        "region": "AMER",
        "daily_burn_rate_units": 450.0,
        "total_capacity_units": 1800,
        "stock_on_hand": 1412,
        "capacity_full_pct": 78.4,
        "active_inbound_trucks": 1,
        "total_dock_bays": 2,
        "busy_dock_bays": 2,
        "overall_status": "Operational",
        "latitude": 40.7357,
        "longitude": -74.1724,
        "on_time_delivery_pct": 96.6,
        "forklift_fleet_active": "1/2 working",
        "forklift_status": "FL-01 Loading TRK-2051 at Bay 1 (75%)"
    },
    "PLANT_02": {
        "plant_id": "PLANT_02",
        "plant_name": "Austin Gigafactory",
        "facility_type": "GIGAFACTORY",
        "location": "Austin, TX, USA",
        "region": "AMER",
        "daily_burn_rate_units": 600.0,
        "total_capacity_units": 5000,
        "stock_on_hand": 2280,
        "capacity_full_pct": 45.6,
        "active_inbound_trucks": 2,
        "total_dock_bays": 4,
        "busy_dock_bays": 3,
        "overall_status": "Critical",
        "latitude": 30.2223,
        "longitude": -97.6171,
        "on_time_delivery_pct": 78.2,
        "forklift_fleet_active": "3/4 working",
        "forklift_status": "FL-03 Unloading Inbound Battery Pack Cell (90%)"
    },
    "PLANT_01": {
        "plant_id": "PLANT_01",
        "plant_name": "Fremont Assembly Plant",
        "facility_type": "ASSEMBLY",
        "location": "Fremont, CA, USA",
        "region": "AMER",
        "daily_burn_rate_units": 400.0,
        "total_capacity_units": 4500,
        "stock_on_hand": 3800,
        "capacity_full_pct": 84.4,
        "active_inbound_trucks": 1,
        "total_dock_bays": 3,
        "busy_dock_bays": 1,
        "overall_status": "Operational",
        "latitude": 37.4988,
        "longitude": -121.9430,
        "on_time_delivery_pct": 98.4,
        "forklift_fleet_active": "2/2 working",
        "forklift_status": "FL-02 Idle at Bay 2 (100%)"
    }
}

INVENTORY_DB: Dict[str, List[Dict[str, Any]]] = {
    "WH_RIVERSIDE_01": [
        {"part_id": "SKU_CB_101", "part_name": "Cardboard Box (M)", "part_number": "CB-M-101", "category": "Packaging", "criticality": "STANDARD", "on_hand_qty": 1906, "safety_stock_qty": 800, "days_of_inventory": 18.5, "status": "In Stock"},
        {"part_id": "SKU_PC_204", "part_name": "Plastic Container", "part_number": "PC-204", "category": "Storage", "criticality": "STANDARD", "on_hand_qty": 297, "safety_stock_qty": 200, "days_of_inventory": 9.2, "status": "In Stock"},
        {"part_id": "SKU_SH_809", "part_name": "Safety Helmet", "part_number": "SH-809", "category": "Safety Gear", "criticality": "HIGH", "on_hand_qty": 212, "safety_stock_qty": 350, "days_of_inventory": 4.1, "status": "Low Stock"},
        {"part_id": "SKU_PT_401", "part_name": "Packing Tape", "part_number": "PT-401", "category": "Consumables", "criticality": "STANDARD", "on_hand_qty": 4448, "safety_stock_qty": 1500, "days_of_inventory": 24.0, "status": "In Stock"}
    ],
    "PLANT_02": [
        {"part_id": "PART_BAT_402", "part_name": "High-Density Battery Cells", "part_number": "BAT-402", "category": "Powertrain", "criticality": "CRITICAL", "on_hand_qty": 2280, "safety_stock_qty": 4200, "days_of_inventory": 3.8, "status": "Critical Stockout"},
        {"part_id": "PART_SEMI_101", "part_name": "Autonomous Radar MCU", "part_number": "SEMI-101", "category": "Semiconductors", "criticality": "HIGH", "on_hand_qty": 4800, "safety_stock_qty": 3000, "days_of_inventory": 12.0, "status": "In Stock"},
        {"part_id": "PART_ALUM_201", "part_name": "Extruded Aluminum Frame", "part_number": "ALUM-201", "category": "Chassis", "criticality": "MEDIUM", "on_hand_qty": 6500, "safety_stock_qty": 3500, "days_of_inventory": 16.2, "status": "In Stock"}
    ],
    "PLANT_01": [
        {"part_id": "PART_BAT_402", "part_name": "High-Density Battery Cells", "part_number": "BAT-402", "category": "Powertrain", "criticality": "CRITICAL", "on_hand_qty": 7200, "safety_stock_qty": 3000, "days_of_inventory": 18.0, "status": "In Stock"},
        {"part_id": "PART_STEEL_301", "part_name": "Hot-Rolled Sheet Steel", "part_number": "STEEL-301", "category": "Body", "criticality": "MEDIUM", "on_hand_qty": 9100, "safety_stock_qty": 4000, "days_of_inventory": 22.7, "status": "In Stock"}
    ]
}

DOCKS_DB: Dict[str, List[Dict[str, Any]]] = {
    "WH_RIVERSIDE_01": [
        {"dock_id": "DOCK_01", "bay_number": 1, "status": "Loading", "assigned_truck_id": "TRK-2051", "assigned_carrier": "WareTrack", "progress": "2/6", "eta_minutes": 13},
        {"dock_id": "DOCK_02", "bay_number": 2, "status": "Available", "assigned_truck_id": None, "assigned_carrier": None, "progress": None, "eta_minutes": None},
        {"dock_id": "DOCK_INBOUND", "bay_number": 3, "status": "En route", "assigned_truck_id": "TRK-2287", "assigned_carrier": "Bluepeak", "progress": "Approaching", "eta_minutes": 2}
    ],
    "PLANT_02": [
        {"dock_id": "DOCK_AUSTIN_01", "bay_number": 1, "status": "Unloading", "assigned_truck_id": "TRK-9011", "assigned_carrier": "Apex Logistics", "progress": "5/6", "eta_minutes": 8},
        {"dock_id": "DOCK_AUSTIN_02", "bay_number": 2, "status": "Delayed", "assigned_truck_id": "TRK-8812", "assigned_carrier": "Port Long Beach Rail", "progress": "Held at Berth", "eta_minutes": 20160},
        {"dock_id": "DOCK_AUSTIN_03", "bay_number": 3, "status": "Available", "assigned_truck_id": None, "assigned_carrier": None, "progress": None, "eta_minutes": None}
    ],
    "PLANT_01": [
        {"dock_id": "DOCK_FREMONT_01", "bay_number": 1, "status": "Loading", "assigned_truck_id": "TRK-4401", "assigned_carrier": "Pacific Freight", "progress": "4/6", "eta_minutes": 25},
        {"dock_id": "DOCK_FREMONT_02", "bay_number": 2, "status": "Available", "assigned_truck_id": None, "assigned_carrier": None, "progress": None, "eta_minutes": None}
    ]
}

SHIPMENT_STEPPER_DB: Dict[str, Dict[str, Any]] = {
    "WH_RIVERSIDE_01": {
        "shipment_id": "#SHP-78442",
        "carrier_name": "WareTrack TRK-2051",
        "truck_id": "TRK-2051",
        "destination": "Philadelphia, PA",
        "status": "Loading 2/6",
        "current_step": 3, # 1: Order Confirmed, 2: Picked, 3: Loading 2/6, 4: In Transit, 5: Delivered
        "steps": [
            {"step_index": 1, "label": "Order Confirmed", "timestamp": "06:49", "completed": True},
            {"step_index": 2, "label": "Picked", "timestamp": "08:20", "completed": True},
            {"step_index": 3, "label": "Loading 2/6", "timestamp": "ETA 09:53", "completed": False, "active": True},
            {"step_index": 4, "label": "In Transit", "timestamp": "ETA 10:01", "completed": False},
            {"step_index": 5, "label": "Delivered", "timestamp": "ETA 10:33", "completed": False}
        ],
        "bay_info": "WH-01 • Bay 1 - 13 min left"
    },
    "PLANT_02": {
        "shipment_id": "#SHP-401",
        "carrier_name": "Apex Intermodal Freight",
        "truck_id": "TRK-8812",
        "destination": "Austin Giga 1, TX",
        "status": "Disrupted In Transit",
        "current_step": 4,
        "steps": [
            {"step_index": 1, "label": "Order Confirmed", "timestamp": "Sep 12", "completed": True},
            {"step_index": 2, "label": "Picked", "timestamp": "Sep 14", "completed": True},
            {"step_index": 3, "label": "Berth Loaded", "timestamp": "Sep 18", "completed": True},
            {"step_index": 4, "label": "Port Delay (+14d)", "timestamp": "Berth Strike", "completed": False, "active": True, "alert": True},
            {"step_index": 5, "label": "Delivered", "timestamp": "Delayed", "completed": False}
        ],
        "bay_info": "Austin Bay 2 • Delay: +14 Business Days"
    }
}

RULES_DB: Dict[str, Dict[str, Any]] = {
    "RULE_DOI_GLOBAL": {
        "rule_id": "RULE_DOI_GLOBAL",
        "rule_name": "Global Stockout DOI Thresholds",
        "rule_category": "INVENTORY_BUFFER",
        "scope": "GLOBAL",
        "parameters": {
            "critical_doi": 5.0,
            "warning_doi": 10.0,
            "low_stock_ratio": 0.25
        },
        "is_active": True
    },
    "RULE_DOCK_UTILIZATION": {
        "rule_id": "RULE_DOCK_UTILIZATION",
        "rule_name": "Bay Turnaround & Congestion Alert",
        "rule_category": "DOCK_UTILIZATION",
        "scope": "GLOBAL",
        "parameters": {
            "max_loading_minutes": 45,
            "max_berth_delay_minutes": 120,
            "alert_on_congestion": True
        },
        "is_active": True
    },
    "RULE_SUPPLIER_OTIF": {
        "rule_id": "RULE_SUPPLIER_OTIF",
        "rule_name": "Supplier Minimum OTIF Rating",
        "rule_category": "SUPPLIER_OTIF",
        "scope": "GLOBAL",
        "parameters": {
            "min_acceptable_otif_pct": 85.0,
            "max_delay_days_warning": 3,
            "liquidated_damages_grace_days": 3
        },
        "is_active": True
    }
}
