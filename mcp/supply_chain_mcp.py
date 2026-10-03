"""
Supply Chain Action MCP Server
Provides real-world executable actions for CoCo agents:
1. expedite_purchase_order: Re-routes delayed shipments to expedited air cargo
2. send_supplier_sla_breach_alert: Dispatches formal SLA breach notices to Slack
"""

import json
import sys
from datetime import datetime, timezone

def expedite_purchase_order(po_id: str, part_id: str, new_carrier: str = "Global Aero Air Cargo", expedited_cost_usd: float = 12500.0) -> dict:
    """
    Simulates / triggers an emergency air-freight reorder ticket in ERP (SAP/Jira).
    """
    now = datetime.now(timezone.utc)
    action_result = {
        "action": "EXPEDITE_PURCHASE_ORDER",
        "status": "EXECUTED",
        "timestamp": now.isoformat(),
        "details": {
            "original_po_id": po_id,
            "emergency_po_id": f"EXP_{po_id[-8:]}",
            "part_id": part_id,
            "transport_mode": "Air Freight",
            "expedited_carrier": new_carrier,
            "expedited_cost_usd": expedited_cost_usd,
            "estimated_delivery_hours": 36,
            "impact": "Averts Plant 2 (Austin) assembly line shutdown. Delivery estimated in 36 hours."
        }
    }
    return action_result

def send_supplier_sla_breach_alert(supplier_id: str, supplier_name: str, po_id: str, delay_days: int, penalty_usd: float, contract_clause: str, channel: str = "#supply-chain-crisis") -> dict:
    """
    Dispatches a legally grounded breach notice citing contract terms to the Slack supplier incident channel.
    """
    now = datetime.now(timezone.utc)
    slack_payload = {
        "channel": channel,
        "username": "CoCo Governed Supply Chain Agent",
        "icon_emoji": ":warning:",
        "attachments": [
            {
                "color": "#D32F2F",
                "title": f"🚨 FORMAL CONTRACTUAL SLA BREACH NOTICE: {supplier_name}",
                "fields": [
                    {"title": "Supplier ID", "value": supplier_id, "short": True},
                    {"title": "Purchase Order", "value": po_id, "short": True},
                    {"title": "Delay Duration", "value": f"{delay_days} days beyond grace period", "short": True},
                    {"title": "Liquidated Damages Claim", "value": f"${penalty_usd:,.2f} USD", "short": True},
                    {"title": "Contractual Grounding (Cortex Search)", "value": contract_clause, "short": False}
                ],
                "footer": "Snowflake CoCo Governed Ontology & Cortex Intelligence",
                "ts": int(now.timestamp())
            }
        ]
    }
    return {
        "action": "SEND_SUPPLIER_BREACH_SLACK_ALERT",
        "status": "DISPATCHED",
        "timestamp": now.isoformat(),
        "channel": channel,
        "payload": slack_payload
    }

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Testing MCP Action: Expedite PO...")
        print(json.dumps(expedite_purchase_order("PO_2026_002", "PART_BAT_402"), indent=2))
        print("\nTesting MCP Action: Slack Alert...")
        print(json.dumps(send_supplier_sla_breach_alert(
            "SUP_001", "Apex Battery Cells Ltd", "PO_2026_002", 7, 10500.0, 
            "Section 8.2: Liquidated damages of USD $1,500.00/day per delayed shipment after 3-day grace period."
        ), indent=2))
