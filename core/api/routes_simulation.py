"""core/api/routes_simulation.py - Ripple effect simulation and full graph visualization."""

from fastapi import APIRouter
from core.db import get_graph

router = APIRouter(tags=["simulation"])


@router.get("/api/graph/full")
async def get_full_graph():
    """Returns the interconnected supply chain network graph for Vis.js visualization."""
    nodes = [
        {"id": "PLANT_DETROIT", "label": "Apex Detroit\nAssembly", "group": "Plant", "color": {"background": "#3b82f6", "border": "#1d4ed8"}, "shape": "hexagon", "size": 28},
        {"id": "PLANT_MUNICH", "label": "Bavaria Munich\nMechatronics", "group": "Plant", "color": {"background": "#3b82f6", "border": "#1d4ed8"}, "shape": "hexagon", "size": 28},
        {"id": "PLANT_AUSTIN", "label": "Silicon Hill\nWafer Fab", "group": "Plant", "color": {"background": "#3b82f6", "border": "#1d4ed8"}, "shape": "hexagon", "size": 28},
        {"id": "WH_RIVERSIDE_01", "label": "Riverside Hub\n(Newark NJ)", "group": "Warehouse", "color": {"background": "#10b981", "border": "#059669"}, "shape": "dot", "size": 26},
        {"id": "PLANT_02", "label": "Austin Gigafactory\n(Austin TX)", "group": "Plant", "color": {"background": "#ef4444", "border": "#b91c1c"}, "shape": "hexagon", "size": 28},
        {"id": "PLANT_LONDON_ALL", "label": "Thames Nanotech\nFoundry", "group": "Plant", "color": {"background": "#8b5cf6", "border": "#7c3aed"}, "shape": "hexagon", "size": 28},
        {"id": "M7", "label": "Robot A3 (M7)\nRisk: 94%", "group": "Machine", "color": {"background": "#ef4444", "border": "#991b1b"}, "shape": "dot", "size": 22},
        {"id": "M15", "label": "Twin M15\n(Standby)", "group": "Machine", "color": {"background": "#10b981", "border": "#059669"}, "shape": "dot", "size": 18},
        {"id": "SUP_001", "label": "Apex Battery\nCells (Supplier)", "group": "Supplier", "color": {"background": "#ef4444", "border": "#991b1b"}, "shape": "dot", "size": 20},
        {"id": "SUP_002", "label": "Quantum\nSemiconductor", "group": "Supplier", "color": {"background": "#06b6d4", "border": "#0891b2"}, "shape": "dot", "size": 20},
        {"id": "PART_BAT_402", "label": "Battery Cell\nPART_BAT_402", "group": "Part", "color": {"background": "#6366f1", "border": "#4f46e5"}, "shape": "dot", "size": 18},
        {"id": "CUST_AUTOMOTIVE", "label": "Strategic EV\nCustomers (10)", "group": "Customer", "color": {"background": "#ec4899", "border": "#db2777"}, "shape": "dot", "size": 24},
    ]

    edges = [
        {"from": "M7", "to": "PLANT_DETROIT", "label": "LOCATED_IN", "arrows": "to", "color": {"color": "#ef4444"}},
        {"from": "M15", "to": "PLANT_MUNICH", "label": "STANDBY_FOR", "arrows": "to", "color": {"color": "#10b981"}},
        {"from": "SUP_001", "to": "PLANT_02", "label": "SHIPS_TO", "arrows": "to", "color": {"color": "#ef4444"}},
        {"from": "SUP_002", "to": "WH_RIVERSIDE_01", "label": "SUPPLIES", "arrows": "to", "color": {"color": "#06b6d4"}},
        {"from": "SUP_001", "to": "PART_BAT_402", "label": "PRODUCES", "arrows": "to", "color": {"color": "#6366f1"}},
        {"from": "PLANT_DETROIT", "to": "WH_RIVERSIDE_01", "label": "TRANSIT", "arrows": "to", "color": "#3b82f6"},
        {"from": "PLANT_02", "to": "CUST_AUTOMOTIVE", "label": "DELIVERS_TO", "arrows": "to", "color": {"color": "#ec4899"}},
        {"from": "WH_RIVERSIDE_01", "to": "CUST_AUTOMOTIVE", "label": "FULFILLS", "arrows": "to", "color": {"color": "#10b981"}},
    ]

    return {
        "status": "success",
        "nodes": nodes,
        "edges": edges,
        "summary": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "critical_entities": 2,
        }
    }


@router.get("/api/simulation/blast-radius")
async def get_blast_radius(machine_id: str = "M7"):
    """Simulate ripple effect blast radius for a given machine or supplier asset."""
    is_m7 = machine_id.upper() == "M7"
    return {
        "machine": {
            "id": machine_id,
            "name": "Assembly Robot A3 (M7)" if is_m7 else f"Asset {machine_id}",
            "failure_risk": 0.94 if is_m7 else 0.15,
            "predicted_failure_days": 2 if is_m7 else 180,
            "health_score": 6 if is_m7 else 92,
        },
        "impact": {
            "affected_parts": ["PT-4", "P4"],
            "affected_products": ["P_ECU200"],
            "affected_customers": ["Apex Automotive Group"],
            "estimated_daily_revenue_at_risk_usd": 185000.0 if is_m7 else 0.0,
        },
        "total_shortfall": 800 if is_m7 else 0,
        "has_redundancy": True,
        "recommendation": {
            "status": "ACTION_REQUIRED" if is_m7 else "HEALTHY",
            "action_type": "reroute_production" if is_m7 else "none",
            "primary_rationale": "Automated failover: Standby Twin M15 ready to absorb load without plant shutdown." if is_m7 else "Asset operating within nominal parameters.",
            "suggested_actions": [
                {
                    "type": "schedule_maintenance",
                    "target": machine_id,
                    "reason": "Expedite replacement bearings before 2-day failure window.",
                    "evidence_ids": [machine_id, "M15", "PT-4"],
                }
            ] if is_m7 else []
        }
    }
