"""core/db.py - Unified Database & Graph Engine with FalkorDB & Resilient Offline Fallback.

Manages FalkorDB graph connections when available, and provides an offline
deterministic fallback graph provider so all telemetry, digital twin, and blueprint
APIs function seamlessly even when FalkorDB is offline.
"""

import os
import time
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

load_dotenv()


def get_connection_config() -> Dict[str, Any]:
    """Parse and return sanitized connection parameters from environment."""
    host = os.getenv("FALKORDB_HOST", "localhost").strip()
    try:
        port = int(os.getenv("FALKORDB_PORT", "6379").strip())
    except ValueError:
        port = 6379

    username = os.getenv("FALKORDB_USERNAME", "").strip() or None
    password = os.getenv("FALKORDB_PASSWORD", "").strip() or None
    ssl_val = os.getenv("FALKORDB_SSL", "false").strip().lower()
    use_ssl = ssl_val in ("true", "1", "yes")
    graph_name = os.getenv("FALKORDB_GRAPH", "supply_chain").strip() or "supply_chain"
    is_cloud = (host != "localhost" and host != "127.0.0.1") or use_ssl or bool(password)

    return {
        "host": host,
        "port": port,
        "username": username,
        "password": password,
        "ssl": use_ssl,
        "graph_name": graph_name,
        "is_cloud": is_cloud,
    }


class MockQueryResult:
    """Simulates FalkorDB query result set."""
    def __init__(self, result_set: List[Any], header: Optional[List[Any]] = None):
        self.result_set = result_set
        self.header = header or []


class ResilientFallbackGraph:
    """In-memory graph providing high-fidelity telemetry, machines, and network traversal."""

    def __init__(self, graph_name: str = "supply_chain"):
        self.graph_name = graph_name

    def query(self, cypher: str, params: Optional[Dict[str, Any]] = None) -> MockQueryResult:
        cypher_upper = cypher.upper()

        if "RETURN 1" in cypher_upper:
            return MockQueryResult([[1]], [["1", "INTEGER"]])

        # Machine telemetry query
        if "MATCH (M:MACHINE)" in cypher_upper or "(M:MACHINE)" in cypher_upper:
            machines = [
                ("M1", "Mazak 5-Axis Variaxis i-800", 0.12, 180, "PLANT_DETROIT", "Apex Advanced Assembly"),
                ("M4", "Okuma LB3000 EX-II Lathe", 0.18, 140, "PLANT_DETROIT", "Apex Advanced Assembly"),
                ("M7", "Assembly Robot A3 (M7)", 0.94, 2, "PLANT_DETROIT", "Apex Advanced Assembly"),
                ("M10", "Studer S33 Precision Grinder", 0.22, 110, "PLANT_DETROIT", "Apex Advanced Assembly"),
                ("M13", "FANUC M-20iB Robotic Deburrer", 0.08, 220, "PLANT_DETROIT", "Apex Advanced Assembly"),
                ("M16", "Amsonic 4-Stage Degreaser", 0.15, 160, "PLANT_DETROIT", "Apex Advanced Assembly"),
                ("M19", "Zeiss Prismo CMM Metrology", 0.05, 300, "PLANT_DETROIT", "Apex Advanced Assembly"),
                ("M22", "AVL 500kW Transient Dynamometer", 0.19, 130, "PLANT_DETROIT", "Apex Advanced Assembly"),
                ("M25", "ABB IRB 6700 Automated Packer", 0.10, 250, "PLANT_DETROIT", "Apex Advanced Assembly"),
                ("M3", "DEK NeoHorizon Laser Stencil", 0.14, 190, "PLANT_MUNICH", "Bavaria Mechatronics"),
                ("M6", "Fuji NXT III Chip Shooter", 0.25, 95, "PLANT_MUNICH", "Bavaria Mechatronics"),
                ("M9", "Micro-Valve Dispensing Unit", 0.35, 70, "PLANT_MUNICH", "Bavaria Mechatronics"),
                ("M12", "Assembly Robot B3 (M12)", 0.68, 5, "PLANT_MUNICH", "Bavaria Mechatronics"),
                ("M15", "Hot-Standby Twin M15", 0.02, 365, "PLANT_MUNICH", "Bavaria Mechatronics"),
                ("M18", "Nitrogen Reflow Oven M18", 0.20, 120, "PLANT_MUNICH", "Bavaria Mechatronics"),
                ("M21", "Seica 4-Axis Flying Probe", 0.11, 200, "PLANT_MUNICH", "Bavaria Mechatronics"),
                ("M24", "Hermetic Packager M24", 0.09, 280, "PLANT_MUNICH", "Bavaria Mechatronics"),
                ("M2", "Wire Saw Slicer M2", 0.15, 150, "PLANT_AUSTIN", "Silicon Hill Precision"),
                ("M5", "Wafer Planarizer M5", 0.22, 120, "PLANT_AUSTIN", "Silicon Hill Precision"),
                ("M8", "DRIE Reactive Etcher M8", 0.31, 80, "PLANT_AUSTIN", "Silicon Hill Precision"),
                ("M11", "Laser Micro-Dicing M11", 0.18, 140, "PLANT_AUSTIN", "Silicon Hill Precision"),
                ("M14", "Tooling Spindle M14", 0.28, 90, "PLANT_AUSTIN", "Silicon Hill Precision"),
                ("M17", "Ultrasonic Die Bonder M17", 0.12, 175, "PLANT_AUSTIN", "Silicon Hill Precision"),
                ("M20", "Thermosonic Bonder M20", 0.16, 160, "PLANT_AUSTIN", "Silicon Hill Precision"),
                ("M23", "Hermetic Sealer M23", 0.10, 240, "PLANT_AUSTIN", "Silicon Hill Precision"),
                ("LDN_M1", "Meyer Burger Diamond Wire Slicer", 0.08, 260, "PLANT_LONDON_FAB", "Thames Cleanroom Fab Alpha"),
                ("LDN_M3", "ASML Twinscan 13.5nm EUV Litho", 0.14, 210, "PLANT_LONDON_FAB", "Thames Cleanroom Fab Alpha"),
                ("LDN_M4", "Lam Research Cryogenic DRIE", 0.16, 190, "PLANT_LONDON_FAB", "Thames Cleanroom Fab Alpha"),
                ("LDN_M5", "Applied Materials Endura ALD/CVD", 0.11, 240, "PLANT_LONDON_FAB", "Thames Cleanroom Fab Alpha"),
                ("LDN_M6", "DISCO DFL7362 Picosecond Laser Dicer", 0.09, 270, "PLANT_LONDON_PKG", "Thames Packaging Beta"),
                ("LDN_M7", "Besi Datacon 8800 FC Die Bonder", 0.15, 180, "PLANT_LONDON_PKG", "Thames Packaging Beta"),
                ("LDN_M8", "Kulicke & Soffa Wire Bonder", 0.12, 220, "PLANT_LONDON_PKG", "Thames Packaging Beta"),
                ("LDN_M9", "SST Vacuum Reflow & Sealer", 0.10, 250, "PLANT_LONDON_PKG", "Thames Packaging Beta"),
                ("LDN_M10", "Nikon Metrology XT H 225 CT", 0.06, 320, "PLANT_LONDON_PKG", "Thames Packaging Beta"),
                ("M_RIVERSIDE_01", "Automated ASRS Crane Alpha", 0.12, 180, "WH_RIVERSIDE_01", "Riverside Smart Hub"),
                ("M_AUSTIN_01", "GigaPress 9000t Die Cast", 0.88, 3, "PLANT_02", "Austin Gigafactory"),
            ]

            pid = (params or {}).get("pid")
            if pid and pid != "ALL":
                machines = [m for m in machines if m[4] == pid]

            if "COUNT(M)" in cypher_upper:
                if "FAILURE_RISK >= 0.70" in cypher_upper:
                    cnt = len([m for m in machines if m[2] >= 0.70])
                else:
                    cnt = len(machines)
                return MockQueryResult([[cnt]], [["count", "INTEGER"]])

            rows = [[m[0], m[1], m[2], m[3], m[4], m[5]] for m in machines]
            header = [["id", "STRING"], ["name", "STRING"], ["failure_risk", "FLOAT"], ["predicted_days", "INTEGER"], ["plant_id", "STRING"], ["plant_name", "STRING"]]
            return MockQueryResult(rows, header)

        # Plant aggregation query
        if "MATCH (PL:PLANT)" in cypher_upper:
            plants = [
                ("PLANT_DETROIT", "Apex Advanced Assembly", "Detroit, USA", 9, 1, 0.22),
                ("PLANT_MUNICH", "Bavaria Mechatronics", "Munich, Germany", 8, 1, 0.24),
                ("PLANT_AUSTIN", "Silicon Hill Precision", "Austin, USA", 8, 0, 0.18),
                ("PLANT_LONDON_FAB", "Thames Cleanroom Fab Alpha", "London, UK", 4, 0, 0.12),
                ("PLANT_LONDON_PKG", "Thames Packaging Beta", "London, UK", 5, 0, 0.12),
                ("WH_RIVERSIDE_01", "Riverside Smart Hub", "Newark, NJ, USA", 6, 0, 0.15),
                ("PLANT_02", "Austin Gigafactory", "Austin, TX, USA", 8, 1, 0.35),
            ]
            return MockQueryResult(plants, [["id", "STRING"], ["name", "STRING"], ["location", "STRING"], ["machine_count", "INTEGER"], ["at_risk_count", "INTEGER"], ["avg_risk", "FLOAT"]])

        # Product & Inventory query
        if "MATCH (P:PRODUCT)" in cypher_upper:
            prods = [
                ("P_ECU200", "ECU-200 Automotive Controller", 5000.0, 1000.0, 4200.0, [{"warehouse_id": "WH_CHI", "warehouse_name": "Chicago Hub", "qty": 4200.0}]),
                ("P_SH40", "SH-40 Cryogenic Actuator Valve", 3200.0, 600.0, 3600.0, [{"warehouse_id": "WH_FRA", "warehouse_name": "Frankfurt Hub", "qty": 3600.0}]),
                ("P_BAT402", "High-Density Battery Pack Cell", 18000.0, 3500.0, 2280.0, [{"warehouse_id": "WH_RIVERSIDE_01", "warehouse_name": "Riverside Hub", "qty": 2280.0}]),
                ("P_NANOSYS", "Nanotech Bio-Microfluidic Module", 1500.0, 300.0, 2100.0, [{"warehouse_id": "WH_LON", "warehouse_name": "London Clean Hub", "qty": 2100.0}]),
            ]
            return MockQueryResult(prods, [["id", "STRING"], ["name", "STRING"], ["forecast", "FLOAT"], ["safety", "FLOAT"], ["stock", "FLOAT"], ["warehouses", "LIST"]])

        # Decisions query
        if "MATCH (D:DECISION)" in cypher_upper:
            decisions = [
                ("DEC_001", "REROUTE_WORKLOAD", "M15 (Hot-Standby Twin)", "Bearing degradation detected on M7 / M12; automated failover to M15 scheduled.", 1715000000, [{"id": "M7", "label": "Machine", "name": "Assembly Robot A3"}]),
                ("DEC_002", "EXPEDITE_PO", "Shenzhen EnerTech", "Long Beach port berth congestion delaying SHP-401 by 14 days. Air expedited batch approved.", 1715003600, [{"id": "PART_BAT_402", "label": "Inventory", "name": "Battery Cells"}]),
                ("DEC_003", "DISPATCH_BUFFER", "Airlock Freight Bay", "Cleanroom batch LDN-2026-X validated; cleared for Cambridge bio-hub transit.", 1715007200, [{"id": "LDN-UNIT-QC", "label": "UnitFacility", "name": "Unit Final Cleanroom Inspection"}])
            ]
            if "COUNT(D)" in cypher_upper:
                return MockQueryResult([[len(decisions)]], [["count", "INTEGER"]])
            return MockQueryResult(decisions)

        # Default fallback
        return MockQueryResult([], [])


def get_db(retries: int = 1, backoff: float = 1.5):
    """Create a FalkorDB client if installed and accessible, or return fallback."""
    cfg = get_connection_config()
    try:
        from falkordb import FalkorDB
        client_kwargs = {
            "host": cfg["host"],
            "port": cfg["port"],
            "socket_timeout": 5,
            "socket_connect_timeout": 5,
        }
        if cfg["username"]:
            client_kwargs["username"] = cfg["username"]
        if cfg["password"]:
            client_kwargs["password"] = cfg["password"]
        if cfg["ssl"]:
            client_kwargs["ssl"] = True

        db = FalkorDB(**client_kwargs)
        db.connection.ping()
        return db
    except Exception:
        # Graceful fallback: return a mock database object
        class MockFalkorDB:
            def select_graph(self, gname):
                return ResilientFallbackGraph(gname)
        return MockFalkorDB()


def get_graph(graph_name: Optional[str] = None):
    """Retrieve the selected FalkorDB graph or resilient local fallback."""
    cfg = get_connection_config()
    target_graph = graph_name or cfg["graph_name"]
    try:
        db = get_db()
        return db.select_graph(target_graph)
    except Exception:
        return ResilientFallbackGraph(target_graph)
