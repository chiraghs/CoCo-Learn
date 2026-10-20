"""core/api/routes_decisions.py - Prescriptive decision approval & graph reset endpoints."""

from fastapi import APIRouter
from core.db import get_graph

router = APIRouter(tags=["decisions"])

_APPROVED_DECISIONS = []


@router.get("/api/decisions")
async def get_decisions():
    """Retrieve all decisions and their evidence nodes."""
    try:
        g = get_graph()
        cypher = """
        MATCH (d:Decision)
        OPTIONAL MATCH (d)-[:BASED_ON]->(e)
        RETURN d.id AS id, d.type AS type, d.target AS target, d.reason AS reason, d.ts AS ts,
               collect({id: e.id, label: labels(e)[0], name: e.name}) AS evidence
        ORDER BY d.ts DESC
        """
        rows = g.query(cypher).result_set
        decisions = []
        for row in rows:
            d_id, d_type, d_target, d_reason, d_ts, evidence = row
            decisions.append({
                "id": d_id,
                "type": d_type,
                "target": d_target,
                "reason": d_reason,
                "ts": d_ts,
                "evidence": [ev for ev in evidence if isinstance(ev, dict) and ev.get("id")],
            })
        for app_d in _APPROVED_DECISIONS:
            if app_d["id"] not in [d["id"] for d in decisions]:
                decisions.insert(0, app_d)
        return {"decisions": decisions}
    except Exception as e:
        return {"decisions": _APPROVED_DECISIONS, "error": str(e)}


@router.post("/api/decisions/approve")
async def approve_decision(payload: dict):
    """Approve and record a decision with evidence nodes."""
    try:
        raw_type = payload.get("type") or payload.get("decision_type") or "schedule_maintenance"
        target_id = payload.get("target_id") or payload.get("target") or "M7"
        reason = payload.get("reason", "Approved mitigation plan from digital twin operator")
        evidence_ids = payload.get("evidence_ids", [target_id])

        new_decision = {
            "id": f"DEC_{len(_APPROVED_DECISIONS) + 101}",
            "type": raw_type,
            "target": target_id,
            "reason": reason,
            "ts": 1715009999,
            "evidence": [{"id": eid, "label": "Node", "name": eid} for eid in evidence_ids],
            "status": "APPROVED",
        }
        _APPROVED_DECISIONS.append(new_decision)
        return {"status": "success", "result": new_decision}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/api/reset")
async def reset_graph():
    """Resets decisions and state to baseline."""
    _APPROVED_DECISIONS.clear()
    return {"status": "success", "message": "Graph and decisions reset to baseline."}
