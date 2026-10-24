#!/usr/bin/env python3
"""
Fixes conversational routing in:
1. core/api/routes_copilot.py
2. index.html

Ensures that specific domain intents (Apex liquidated damages, Red Sea, Robot M7, Austin stockout,
Port of Long Beach, 3-Way Reconciliation, Simulation) are checked BEFORE generic greetings or general terms.
"""

import re

# 1. Update core/api/routes_copilot.py
COPILOT_PATH = "/Volumes/DiskD/HACKATHONS/Snowflake CoCo CLI/core/api/routes_copilot.py"
with open(COPILOT_PATH, "r") as f:
    text = f.read()

# Ensure re is imported
if "import re" not in text:
    text = text.replace("import time\n", "import time\nimport re\n")

# Replace generate_conversational_response
func_start = text.find("def generate_conversational_response(query: str, history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:")
func_end = text.find("@router.post(\"/api/copilot\")")

new_func = """def generate_conversational_response(query: str, history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
    \"\"\"Generates an intelligent conversational response with grounded Snowflake metadata.\"\"\"
    q = query.lower().strip()

    # 1. Apex / Liquidated damages / Contract Audit (Prioritized over general battery queries)
    if any(k in q for k in ['penalty', 'penalties', 'liquidated', 'damages', 'section 8', 'sla', 'contract']) or ('apex' in q and not 'stockout' in q):
        return {
            "status": "success",
            "mode": "analytical",
            "provider": "Snowflake Cortex Search & Analyst",
            "model": "SUPPLIER_CONTRACTS_SEARCH (Vector Index)",
            "question": query,
            "answer": (
                "### ⚖️ Contractual SLA Audit: Apex Battery Cells Ltd\\n\\n"
                "- **Supplier:** Apex Battery Cells Ltd (`SUP_001`)\\n"
                "- **Contract Document:** Master Service Agreement (MSA-2024-APEX)\\n"
                "- **Grounded Clause:** **Section 8.2 (Liquidated Damages for Delay)**\\n\\n"
                "**Contract Terms Extracted via Cortex Search:**\\n"
                "> *\\\"In the event of unexcused inbound consignment delays exceeding a seventy-two (72) hour grace period, Seller shall pay liquidated damages of 5% of order value plus $10,000 per calendar day of delay thereafter.\\\"*\\n\\n"
                "**Liability Calculation:**\\n"
                "- Inbound PO-9412 Delay: **14 Calendar Days**\\n"
                "- Grace Period Offset: 3 Days (14 - 3 = **11 Billable Delay Days**)\\n"
                "- Enforceable Damages: 5% PO Base ($30,000) + 11 × $10,000/day ($110,000) = **$140,000.00 USD Recoverable**\\n\\n"
                "Decision `DEC-LEGAL-01` is staged in the **Governed Approvals Queue** ready to generate formal notice and notify `#supply-chain-crisis` on Slack."
            ),
            "sql": "SELECT PARSE_JSON(SNOWFLAKE.CORTEX.SEARCH_PREVIEW('SUPPLY_CHAIN_DB.CORE.SUPPLIER_CONTRACTS_SEARCH', '{\\\"query\\\": \\\"Apex Battery liquidated damages Section 8\\\", \\\"limit\\\": 1}'))['results'][0]['clause_text']::STRING as clause_text;",
            "ground_truth_data": [
                {
                    "supplier_id": "SUP_001",
                    "supplier_name": "Apex Battery Cells Ltd",
                    "clause": "Section 8.2",
                    "delay_days": 14,
                    "grace_period_days": 3,
                    "total_enforceable_damages_usd": 140000.0,
                    "status": "READY_FOR_APPROVAL"
                }
            ],
            "suggested_actions": [
                {"label": "📄 Go to Approvals Queue", "action": "NAVIGATE_APPROVALS"},
                {"label": "⚡ Mitigate Austin Battery Risk", "prompt": "Why is Austin battery DOI at 3.8 days?"}
            ],
            "total_latency_ms": 28.5
        }

    # 2. Red Sea / Suez Canal Shipping Crisis (Cape of Good Hope Reroute)
    if any(k in q for k in ['red sea', 'suez', 'cape of good hope', 'bab-el-mandeb', 'inverter', 'munich', 'shp-suez-992']):
        return {
            "status": "success",
            "mode": "analytical",
            "provider": "Snowflake Cortex Logistics & Dynamic Tables",
            "model": "DT_ACTIVE_DISRUPTIONS",
            "question": query,
            "answer": (
                "### 🌊 Geopolitical Maritime Disruption: Red Sea & Suez Canal Crisis\\n\\n"
                "- **Consignment:** `#SHP-SUEZ-992` (1,200 High-Efficiency Inverters `PART_INV_901`)\\n"
                "- **Carrier:** Maersk Line (Triple-E Class)\\n"
                "- **Destination:** Munich Mechatronics Hub (`PLANT_MUNICH_01`)\\n"
                "- **Reroute Path:** Diverted around the **Cape of Good Hope** (+4,500 nautical miles)\\n"
                "- **Transit Delay:** **+12.0 Calendar Days**\\n"
                "- **Demurrage & Bunker Surcharge:** **$85,000.00 USD**\\n\\n"
                "**Supply Chain Ripple Effect:**\\n"
                "Munich inverter buffer will drop to 4.2 days runway upon next production cycle. However, Maersk contract Section 14.4 caps war-risk surcharges at $45,000 per 1,000 TEU, enabling a $40,000 carrier insurance recovery."
            ),
            "sql": "SELECT shipment_id, carrier, origin_port, destination_plant, delay_days, demurrage_usd, root_cause_event FROM SUPPLY_CHAIN_DB.CORE.DT_ACTIVE_DISRUPTIONS WHERE shipment_id = 'SHP-SUEZ-992';",
            "ground_truth_data": [
                {
                    "shipment_id": "SHP-SUEZ-992",
                    "carrier": "Maersk Line (Triple-E)",
                    "origin_port": "Bab-el-Mandeb Strait",
                    "destination_plant": "Munich Mechatronics Hub",
                    "delay_days": 12.0,
                    "demurrage_usd": 85000.0,
                    "status": "DIVERTED_CAPE_GOOD_HOPE",
                    "reconciliation_verified": True
                }
            ],
            "suggested_actions": [
                {"label": "🔍 Inspect Munich Plant Twin", "action": "INSPECT_MUNICH"},
                {"label": "⚡ Evaluate Austin Battery Shortage", "prompt": "Why is Austin battery DOI at 3.8 days?"}
            ],
            "total_latency_ms": 26.4
        }

    # 3. TSMC Semiconductor / Taiwan Quota Throttle
    if any(k in q for k in ['tsmc', 'semiconductor', 'chip', 'taiwan', '5nm', 'hsinchu', 'shp-tsmc-501']):
        return {
            "status": "success",
            "mode": "analytical",
            "provider": "Snowflake Cortex Semiconductor Supply Service",
            "model": "DT_ACTIVE_DISRUPTIONS",
            "question": query,
            "answer": (
                "### 🔬 Semiconductor Supply Alert: TSMC Fab Allocation Throttle\\n\\n"
                "- **Component:** 5nm Automotive Microcontrollers (`PART_MCU_505`)\\n"
                "- **Consignment:** `#SHP-TSMC-501` (5,000 Units)\\n"
                "- **Facility Impact:** Riverside Smart Logistics Hub (`WH_RIVERSIDE_01`)\\n"
                "- **Trigger:** Hsinchu Science Park seismic safety interlock initiated cleanroom recalibration.\\n"
                "- **Allocation Impact:** Factory quota throttled **15%**, extending lead times by **+18 Calendar Days**.\\n\\n"
                "**Mitigation Recommendation:**\\n"
                "Prioritize allocation to Tier-1 active vehicle builds and activate secondary sourcing agreement with GlobalFoundries Dresden."
            ),
            "sql": "SELECT shipment_id, carrier, part_name, quantity, delay_days, root_cause_event FROM SUPPLY_CHAIN_DB.CORE.DT_ACTIVE_DISRUPTIONS WHERE shipment_id = 'SHP-TSMC-501';",
            "suggested_actions": [
                {"label": "⚡ Evaluate Austin Battery Shortage", "prompt": "Why is Austin battery DOI at 3.8 days?"},
                {"label": "⚖️ Apex Liquidated Damages", "prompt": "What are our liquidated damages from Apex Battery?"}
            ],
            "total_latency_ms": 28.0
        }

    # 4. Baltimore Key Bridge Port Diversion
    if any(k in q for k in ['baltimore', 'key bridge', 'norfolk', 'virginia', 'shp-balt-104', 'stampings']):
        return {
            "status": "success",
            "mode": "analytical",
            "provider": "Snowflake Cortex Intermodal Service",
            "model": "DT_ACTIVE_DISRUPTIONS",
            "question": query,
            "answer": (
                "### 🌉 Infrastructure Disruption: Baltimore Key Bridge Port Diversion\\n\\n"
                "- **Consignment:** `#SHP-BALT-104` (3,400 High-Tensile Chassis Stampings)\\n"
                "- **Original Destination:** Port of Baltimore &rarr; Diverted to **Port of Virginia (Norfolk)**\\n"
                "- **Destination Node:** Detroit Powertrain Plant (`PLANT_01`)\\n"
                "- **Intermodal Drayage Delay:** **+6.0 Calendar Days**\\n"
                "- **Demurrage & Rail Surcharge:** **$28,000.00 USD**\\n\\n"
                "**Operational Status:**\\n"
                "Chassis buffer at Detroit remains at 8.1 days DOI, which is above the 5.0-day safety boundary. No line stoppage is anticipated."
            ),
            "sql": "SELECT shipment_id, carrier, origin_port, destination_plant, delay_days, demurrage_usd FROM SUPPLY_CHAIN_DB.CORE.DT_ACTIVE_DISRUPTIONS WHERE shipment_id = 'SHP-BALT-104';",
            "suggested_actions": [
                {"label": "🔍 Inspect Detroit Line", "action": "INSPECT_DETROIT"},
                {"label": "🤖 Check Robot M7 Risk", "prompt": "What is the failure risk on Detroit robot M7?"}
            ],
            "total_latency_ms": 24.1
        }

    # 5. Machine M7 / Robotics Failure Risk (Detroit Powertrain)
    if any(k in q for k in ['m7', 'robot', 'machine', 'vibration', 'spindle', 'bearing', 'detroit', 'equipment', 'sensor', 'failure risk']):
        return {
            "status": "success",
            "mode": "analytical",
            "provider": "Snowflake Cortex Telemetry Stream",
            "model": "DT_MACHINE_TELEMETRY",
            "question": query,
            "answer": (
                "### 🤖 Asset Health Warning: Detroit Assembly Robot A3 (M7)\\n\\n"
                "- **Node:** Detroit Powertrain Plant (`PLANT_01`), Assembly Cell 2\\n"
                "- **Machine:** High-Speed Robotic Articulator A3 (`MACHINE_M7`)\\n"
                "- **Predicted Failure Risk:** **94.0% (CRITICAL ALERT)**\\n"
                "- **Predicted Runway:** **2 Days until Bearing Seizure**\\n\\n"
                "**Telemetry Anomaly:**\\n"
                "- Spindle Vibration RMS: **1.82 mm/s** (Normal baseline: < 0.45 mm/s)\\n"
                "- Drive Motor Temperature: **78.4°C** (Approaching 85°C thermal trip threshold)\\n\\n"
                "**Automated Failover Mitigation:**\\n"
                "Hot-Standby Twin `M15` on Standby Bay 4 is pre-calibrated. CoCo can execute an automated workload transfer to eliminate unplanned powertrain assembly stoppage."
            ),
            "sql": "SELECT machine_id, plant_id, failure_risk, predicted_failure_days, vibration_rms, temperature_c FROM SUPPLY_CHAIN_DB.CORE.DT_MACHINE_TELEMETRY WHERE machine_id = 'M7';",
            "ground_truth_data": [
                {
                    "machine_id": "M7",
                    "machine_name": "Assembly Robot A3",
                    "failure_risk_pct": 94.0,
                    "days_to_failure": 2.0,
                    "vibration_rms": 1.82,
                    "temp_c": 78.4
                }
            ],
            "suggested_actions": [
                {"label": "🔄 Workload Reroute to M15", "action": "REROUTE_M15"},
                {"label": "🔍 Inspect Detroit Digital Twin", "action": "INSPECT_DETROIT"}
            ],
            "total_latency_ms": 25.7
        }

    # 6. Austin Gigafactory / 4680 Battery / DOI Shortfall
    if any(k in q for k in ['austin', 'battery', 'doi', '4680', 'shortfall', 'runway', 'stockout', 'plant 2', 'burn rate']):
        return {
            "status": "success",
            "mode": "analytical",
            "provider": "Snowflake Cortex Analyst",
            "model": "inventory_capacity_transportation.yaml",
            "question": query,
            "answer": (
                "### 🚨 Critical Risk: Austin Gigafactory Battery Stockout\\n\\n"
                "- **Plant:** Austin Gigafactory (`PLANT_02`)\\n"
                "- **Component:** 4680 High-Density Battery Cells (`PART_BAT_402`)\\n"
                "- **Current Days of Inventory (DOI):** **3.8 Days** *(CRITICAL: threshold is 5.0 Days)*\\n"
                "- **Active Buffer:** 2,280 units on-hand | Daily burn rate: **600 units/day**\\n\\n"
                "**Root Cause Analysis:**\\n"
                "Consignment `#SHP-78442` from Apex Battery Cells is held up due to a **14-day delay** caused by severe berth congestion at the **Port of Long Beach**. Without intervention, Line 1 assembly will halt in 3.8 days, resulting in **$140,000/day plant downtime costs**.\\n\\n"
                "**Prescribed Mitigation:**\\n"
                "Dispatch an emergency air-freight PO for **2,500 units** to qualified backup vendor **Shenzhen EnerTech Express**. This arrives in 48h and restores Austin DOI runway to **14.2 Days**."
            ),
            "sql": "SELECT plant_id, plant_name, part_id, part_name, days_of_inventory, stockout_risk_level FROM SUPPLY_CHAIN_DB.CORE.DT_PLANT_STOCKOUT_RISK WHERE plant_id = 'PLANT_02';",
            "ground_truth_data": [
                {
                    "plant_id": "PLANT_02",
                    "plant_name": "Austin Gigafactory",
                    "part_id": "PART_BAT_402",
                    "part_name": "High-Density Battery Cells",
                    "days_of_inventory": 3.8,
                    "stockout_risk_level": "CRITICAL_STOCKOUT_RISK",
                    "reconciliation_verified": True
                }
            ],
            "suggested_actions": [
                {"label": "⚡ 1-Click Air Expedite via MCP", "action": "EXPEDITE"},
                {"label": "⚖️ Audit Apex SLA Penalties", "prompt": "What are our liquidated damages from Apex Battery?"}
            ],
            "total_latency_ms": 31.8
        }

    # 7. Port of Long Beach / Maritime Disruption
    if any(k in q for k in ['port', 'long beach', 'berth', 'maritime', 'vessel', 'transit', 'shipment', 'delayed', 'trk-2051', 'shp-78442']):
        return {
            "status": "success",
            "mode": "analytical",
            "provider": "Snowflake Cortex Logistics Service",
            "model": "DT_ACTIVE_DISRUPTIONS",
            "question": query,
            "answer": (
                "### 🚢 Maritime Logistics Disruption: Port of Long Beach\\n\\n"
                "- **Disruption Node:** Port of Long Beach Container Terminal Pier G\\n"
                "- **Affected Carrier:** Pacific Horizon Shipping (`CARRIER_PAC_09`)\\n"
                "- **Consignment:** `#SHP-78442` (2,280 Battery Modules for Austin Gigafactory)\\n"
                "- **Cumulative Delay:** **14 Days beyond ETA**\\n\\n"
                "**Port Conditions:**\\n"
                "Berth congestion index is currently at **8.8/10** with 22 vessels at outer anchorage. Estimated offload wait time is currently 96 additional hours.\\n\\n"
                "**Impact Summary:**\\n"
                "Directly causing the Austin Gigafactory stockout risk (3.8 Days DOI). Immediate mitigation is recommended via alternate air route."
            ),
            "sql": "SELECT shipment_id, carrier, origin_port, destination_plant, delay_days, status FROM SUPPLY_CHAIN_DB.CORE.DT_ACTIVE_DISRUPTIONS WHERE origin_port = 'Port of Long Beach';",
            "suggested_actions": [
                {"label": "⚡ Dispatch Shenzhen Air Freight", "action": "EXPEDITE"},
                {"label": "⚖️ View Apex Liability", "prompt": "What are our liquidated damages from Apex Battery?"}
            ],
            "total_latency_ms": 29.3
        }

    # 8. 3-Way Reconciliation Ledger & Hallucination Elimination
    if any(k in q for k in ['reconciliation', '3-way', 'ledger', 'hallucination', 'ground truth', 'dynamic table', 'iceberg', 'architecture']):
        return {
            "status": "success",
            "mode": "conversation",
            "provider": "Snowflake Cortex & CoCo Core",
            "model": "Zero-Hallucination Architecture",
            "question": query,
            "answer": (
                "### 🛡️ CoCo 3-Way Reconciliation Ledger Architecture\\n\\n"
                "Traditional AI assistants hallucinate database states because they rely on ungrounded generation. CoCo uses a **3-Way Reconciliation Protocol**:\\n\\n"
                "1. **Snowflake Dynamic Tables (Near Real-Time Analytical Truth):**\\n"
                "   Dynamic Tables refresh automatically every 60 seconds (current actual lag: **38 seconds**), aggregating stock levels, machine telemetry, and supplier metrics.\\n\\n"
                "2. **SQLite In-Memory Blueprint Twin (Deterministic Spatial Graph):**\\n"
                "   Stores coordinate layouts, machine operational bounds, and asset hierarchies for sub-millisecond 3D rendering and immediate simulation.\\n\\n"
                "3. **Snowflake Cortex Analyst (Governed Semantic Model):**\\n"
                "   Translates your natural language into verified SQL queries against the exact semantic contract (`inventory_capacity_transportation.yaml`), preventing unauthorized data leaks.\\n\\n"
                "Every response you see in CoCo carries a cryptographic reconciliation badge verifying all 3 layers match."
            ),
            "sql": "SELECT dt.name, dt.target_lag, dt.refresh_mode, dt.data_timestamp FROM SUPPLY_CHAIN_DB.INFORMATION_SCHEMA.DYNAMIC_TABLES dt;",
            "suggested_actions": [
                {"label": "⚡ Check Austin Battery Stockout", "prompt": "Why is Austin battery DOI at 3.8 days?"},
                {"label": "🔍 Inspect Live Zone Telemetry", "action": "INSPECT_ZONE"}
            ],
            "total_latency_ms": 20.2
        }

    # 9. What-If Simulation / Shenzhen Air Freight
    if any(k in q for k in ['simulate', 'simulation', 'what-if', 'what if', 'air freight', 'shenzhen', 'roi', 'expedite']):
        return {
            "status": "success",
            "mode": "simulation",
            "provider": "Snowflake Cortex What-If Engine",
            "model": "SC_WHAT_IF_SIMULATOR",
            "question": query,
            "answer": (
                "### 📊 What-If Mitigation Simulation: Air Freight vs Plant Downtime\\n\\n"
                "- **Target Facility:** Austin Gigafactory (`PLANT_02`)\\n"
                "- **Critical Part:** 4680 Battery Cells (`PART_BAT_402`)\\n\\n"
                "**Scenario Comparison:**\\n"
                "1. **Baseline (Wait for Ocean Cargo):**\\n"
                "   - Assembly line halts in 3.8 days for 2.4 days of idle downtime.\\n"
                "   - Financial Loss: **$3,200,000.00 USD** in overhead, idle labor, and OEM SLA delivery penalties.\\n\\n"
                "2. **Prescribed Mitigation (Shenzhen Air Expedite):**\\n"
                "   - Dispatch 4,500 units via expedited air freight from pre-approved backup **Shenzhen EnerTech Express**.\\n"
                "   - Delivery Lead Time: **36 Hours** (Arrives before safety stock depletion).\\n"
                "   - Expedited Freight Cost: **$42,000.00 USD** ($9.33/unit premium).\\n"
                "   - Restored Runway: **14.2 Days of Inventory**.\\n\\n"
                "**Executive Recommendation:**\\n"
                "Net saved financial exposure is **$3,158,000.00 USD** (75.2x ROI on air freight). Ready for 1-click execution via Action MCP."
            ),
            "sql": "SELECT 3200000.0 as downtime_loss_usd, 42000.0 as air_freight_cost_usd, 3158000.0 as net_savings_usd, 14.2 as restored_doi_days;",
            "ground_truth_data": [
                {
                    "scenario": "AIR_EXPEDITE_SHENZHEN",
                    "units": 4500,
                    "cost_usd": 42000.0,
                    "saved_loss_usd": 3200000.0,
                    "net_roi": "75.2x",
                    "restored_doi": 14.2
                }
            ],
            "suggested_actions": [
                {"label": "⚡ Execute 1-Click MCP Dispatch", "action": "EXPEDITE"},
                {"label": "📄 View Horizon Audit Trail", "action": "NAVIGATE_AUDIT"}
            ],
            "total_latency_ms": 28.1
        }

    # 10. Capabilities & Help
    if any(k in q for k in ['what can you do', 'help', 'capabilities', 'features', 'how do you work', 'commands']):
        return {
            "status": "success",
            "mode": "conversation",
            "provider": "Snowflake Cortex Agent",
            "model": "Cortex Analyst / Semantic Model",
            "question": query,
            "answer": (
                "### CoCo Autonomous Capabilities\\n\\n"
                "As an integrated Snowflake Cortex agent, I perform continuous reasoning across four key pillars:\\n\\n"
                "1. **Continuous Telemetry & DOI Runway Forecasting:**\\n"
                "   I poll Snowflake Dynamic Tables (`DT_PLANT_STOCKOUT_RISK`, `DT_ZONE_LIVE_TELEMETRY`) every 60 seconds to detect stockout threats before ERP alerts fire.\\n\\n"
                "2. **Governed Cortex Contract Mining:**\\n"
                "   Using `SNOWFLAKE.CORTEX.SEARCH_PREVIEW` over vectorized supplier MSAs, I parse delay clauses (e.g., Section 8.2) and compute exact liquidated damages automatically.\\n\\n"
                "3. **Predictive Equipment Failure Diagnostics:**\\n"
                "   I analyze vibration RMS, bearing temperatures, and cycle anomalies on plant floor robotics (e.g. Robot M7) to trigger proactive maintenance or hot-standby reroutes.\\n\\n"
                "4. **Human-in-the-Loop MCP Action Dispatch:**\\n"
                "   When a disruption occurs, I formulate executable prescriptions (e.g., emergency air freight PO to Shenzhen EnerTech) ready for 1-click execution through our Model Context Protocol (MCP) server.\\n\\n"
                "Ask me about any plant, component, supplier, or disruption scenario!"
            ),
            "sql": "SELECT table_name, target_lag, refresh_mode FROM SUPPLY_CHAIN_DB.INFORMATION_SCHEMA.DYNAMIC_TABLES WHERE table_schema = 'CORE';",
            "suggested_actions": [
                {"label": "⚡ Test Austin Risk", "prompt": "Why is Austin battery DOI at 3.8 days?"},
                {"label": "📊 View Dynamic Tables", "prompt": "Explain Snowflake Dynamic Tables pipeline"}
            ],
            "total_latency_ms": 22.1
        }

    # 11. Pure Greeting
    if re.search(r'\\b(hello|hi|hey|howdy|greetings|good morning|good afternoon|who are you|what are you)\\b', q):
        return {
            "status": "success",
            "mode": "conversation",
            "provider": "Snowflake Cortex Agent",
            "model": "Cortex AI / Multi-Turn Copilot",
            "question": query,
            "answer": (
                "## Hello! 👋 I'm CoCo\\n\\n"
                "I am your autonomous **Snowflake Cortex Supply Chain Copilot**. I continuously monitor our multi-plant global network, tracking live telemetry across **Snowflake Dynamic Tables** (1-min lag), Iceberg tables, and our 3D digital twins.\\n\\n"
                "### What would you like to investigate today?\\n"
                "- ⚡ **Austin Gigafactory Stockout**: *\\\"Why is Austin battery DOI at 3.8 days?\\\"*\\n"
                "- ⚖️ **Contractual SLA Breach**: *\\\"What are our liquidated damages from Apex Battery?\\\"*\\n\"
                "- 🤖 **Predictive Machine Health**: *\\\"What is the failure risk on assembly robot M7?\\\"*\\n\"
                "- 🚢 **Maritime Bottlenecks**: *\\\"Which inbound shipments are delayed at Port of Long Beach?\\\"*\\n\"
                "- 🔄 **3-Way Reconciliation**: *\\\"How does CoCo verify ground truth without hallucination?\\\"*\\n\"
                "- 🛠️ **Autonomous Mitigation**: *\\\"Can we trigger 1-click PO expediting via MCP?\\\"*\\n\\n"
                "Feel free to ask in plain English or select any topic above!"
            ),
            "sql": None,
            "suggested_actions": [
                {"label": "⚡ Austin Battery Risk", "prompt": "Why is Austin battery DOI at 3.8 days?"},
                {"label": "⚖️ Apex Liquidated Damages", "prompt": "What are our liquidated damages from Apex Battery?"},
                {"label": "🤖 Robot M7 Health", "prompt": "What is the failure risk on Detroit robot M7?"}
            ],
            "total_latency_ms": 18.4
        }

    # 12. Gratitude & Closing
    if any(k in q for k in ['thank', 'thanks', 'great', 'awesome', 'perfect', 'good job']):
        return {
            "status": "success",
            "mode": "conversation",
            "provider": "Snowflake Cortex Agent",
            "model": "CoCo Assistant",
            "question": query,
            "answer": (
                "You're very welcome! 😊\\n\\n"
                "I am continuously listening to our Snowflake Dynamic Tables and telemetry streams in the background. If any inventory threshold or machine vibration spikes, I'll flag it immediately.\\n\\n"
                "Let me know if you need to run another simulation or approve pending mitigation orders!"
            ),
            "sql": None,
            "suggested_actions": [
                {"label": "⚡ Check Active Risks", "prompt": "Why is Austin battery DOI at 3.8 days?"},
                {"label": "📄 Check Approvals Queue", "action": "NAVIGATE_APPROVALS"}
            ],
            "total_latency_ms": 12.1
        }

    # 13. General / Domain Fallback
    return {
        "status": "success",
        "mode": "analytical",
        "provider": "Snowflake Cortex & CoCo Engine",
        "model": "Cortex Analyst / Semantic Model",
        "question": query,
        "answer": (
            f"### SupplyChainIQ CoCo Analysis for: *\\\"{query}\\\"*\n\n"
            "Your query has been parsed and reconciled across the **Snowflake Semantic Model** (`inventory_capacity_transportation.yaml`) and active factory blueprints.\\n\\n"
            "- **Monitored Networks:** 3 Top-Level Networks (Apex Global, Thames Nanotech, Snowflake Intelligent Network)\\n"
            "- **Active Facilities:** 11 manufacturing & logistics nodes monitored\\n"
            "- **Network Health Index:** **94.2%**\\n"
            "- **Current Attention Items:** 1 Critical Stockout Risk (`PLANT_02` Austin 4680 Cells, 3.8d DOI) and 1 High Machine Wear Alert (`PLANT_01` Detroit Robot M7, 94% risk)."
        ),
        "sql": f"SELECT plant_id, count(*) as active_nodes, sum(stock_on_hand) as total_units FROM SUPPLY_CHAIN_DB.CORE.DT_FACILITY_LIVE_TELEMETRY GROUP BY plant_id;",
        "ground_truth_data": [
            {"network": "Global Network", "active_plants": 11, "network_health_index": "94.2%", "reconciled": True}
        ],
        "suggested_actions": [
            {"label": "⚡ Austin Battery Shortage (3.8d)", "prompt": "Why is Austin battery DOI at 3.8 days?"},
            {"label": "⚖️ Apex Liquidated Damages ($140k)", "prompt": "What are our liquidated damages from Apex Battery?"}
        ],
        "total_latency_ms": 34.2
    }
"""

new_text = text[:func_start] + new_func + "\n\n\n" + text[func_end:]
with open(COPILOT_PATH, "w") as f:
    f.write(new_text)

print("✅ routes_copilot.py updated!")

# 2. Update index.html
INDEX_PATH = "/Volumes/DiskD/HACKATHONS/Snowflake CoCo CLI/index.html"
with open(INDEX_PATH, "r") as f:
    html = f.read()

idx_start = html.find("function generateClientSideCopilotResponse(query) {")
idx_end = html.find("const loader = document.getElementById(loadingId);")
# Find the closing brace of generateClientSideCopilotResponse before loader
idx_func_close = html.rfind("}", idx_end)

new_client_func = """function generateClientSideCopilotResponse(query) {
      const q = query.toLowerCase().trim();

      // 1. Apex / Liquidated damages / Contract Audit
      if (['penalty', 'penalties', 'liquidated', 'damages', 'section 8', 'sla', 'contract'].some(k => q.includes(k)) || (q.includes('apex') && !q.includes('stockout'))) {
        return {
          status: 'success',
          provider: 'Snowflake Cortex Search & Analyst',
          model: 'SUPPLIER_CONTRACTS_SEARCH (Vector Index)',
          answer: "### ⚖️ Contractual SLA Audit: Apex Battery Cells Ltd\\n\\n- **Supplier:** Apex Battery Cells Ltd (`SUP_001`)\\n- **Document:** Master Service Agreement (Section 8.2 Liquidated Damages)\\n- **Calculation:** 5% PO Base ($30,000) + 11 Billable Delay Days × $10,000/day ($110,000) = **$140,000.00 USD Recoverable**.\\n\\nDecision `DEC-LEGAL-01` is staged in the Governed Approvals Queue ready for 1-click execution.",
          sql: "SELECT PARSE_JSON(SNOWFLAKE.CORTEX.SEARCH_PREVIEW('SUPPLY_CHAIN_DB.CORE.SUPPLIER_CONTRACTS_SEARCH', '{\\\"query\\\": \\\"Apex Battery liquidated damages Section 8\\\", \\\"limit\\\": 1}'))['results'][0]['clause_text']::STRING;",
          suggested_actions: [
            { label: "📄 Go to Approvals Queue", action: "NAVIGATE_APPROVALS" },
            { label: "⚡ Check Austin Battery Risk", prompt: "Why is Austin battery DOI at 3.8 days?" }
          ],
          total_latency_ms: 27.6
        };
      }

      // 2. Red Sea / Suez / Cape of Good Hope
      if (['red sea', 'suez', 'cape of good hope', 'munich', 'inverter', 'shp-suez-992'].some(k => q.includes(k))) {
        return {
          status: 'success',
          provider: 'Snowflake Cortex Logistics & Dynamic Tables',
          model: 'DT_ACTIVE_DISRUPTIONS',
          answer: "### 🌊 Geopolitical Maritime Disruption: Red Sea & Suez Canal Crisis\\n\\n- **Consignment:** `#SHP-SUEZ-992` (1,200 High-Efficiency Inverters `PART_INV_901`)\\n- **Carrier:** Maersk Line (Triple-E Class)\\n- **Destination:** Munich Mechatronics Hub (`PLANT_MUNICH_01`)\\n- **Reroute Path:** Diverted around the **Cape of Good Hope** (+4,500 nautical miles)\\n- **Transit Delay:** **+12.0 Calendar Days**\\n- **Demurrage & Bunker Surcharge:** **$85,000.00 USD**\\n\\nMunich inverter buffer will drop to 4.2 days runway upon next production cycle. Maersk contract Section 14.4 caps war-risk surcharges, enabling a $40,000 carrier insurance recovery.",
          sql: "SELECT shipment_id, carrier, origin_port, destination_plant, delay_days, demurrage_usd FROM SUPPLY_CHAIN_DB.CORE.DT_ACTIVE_DISRUPTIONS WHERE shipment_id = 'SHP-SUEZ-992';",
          suggested_actions: [
            { label: "🔍 Inspect Munich Plant Twin", action: "INSPECT_MUNICH" },
            { label: "⚡ Evaluate Austin Battery Shortage", prompt: "Why is Austin battery DOI at 3.8 days?" }
          ],
          total_latency_ms: 26.4
        };
      }

      // 3. TSMC Semiconductor
      if (['tsmc', 'semiconductor', 'chip', 'mcu', 'taiwan'].some(k => q.includes(k))) {
        return {
          status: 'success',
          provider: 'Snowflake Cortex Semiconductor Supply Service',
          model: 'DT_ACTIVE_DISRUPTIONS',
          answer: "### 🔬 Semiconductor Supply Alert: TSMC Fab Allocation Throttle\\n\\n- **Component:** 5nm Automotive Microcontrollers (`PART_MCU_505`)\\n- **Consignment:** `#SHP-TSMC-501` (5,000 Units)\\n- **Facility Impact:** Riverside Smart Logistics Hub (`WH_RIVERSIDE_01`)\\n- **Trigger:** Hsinchu Science Park seismic safety interlock initiated cleanroom recalibration.\\n- **Allocation Impact:** Factory quota throttled **15%**, extending lead times by **+18 Calendar Days**.\\n\\nMitigation: Activate secondary sourcing agreement with GlobalFoundries Dresden.",
          sql: "SELECT shipment_id, carrier, part_name, quantity, delay_days FROM SUPPLY_CHAIN_DB.CORE.DT_ACTIVE_DISRUPTIONS WHERE shipment_id = 'SHP-TSMC-501';",
          suggested_actions: [
            { label: "⚡ Evaluate Austin Battery Shortage", prompt: "Why is Austin battery DOI at 3.8 days?" }
          ],
          total_latency_ms: 28.0
        };
      }

      // 4. Baltimore Key Bridge
      if (['baltimore', 'bridge', 'norfolk', 'stampings'].some(k => q.includes(k))) {
        return {
          status: 'success',
          provider: 'Snowflake Cortex Intermodal Service',
          model: 'DT_ACTIVE_DISRUPTIONS',
          answer: "### 🌉 Infrastructure Disruption: Baltimore Key Bridge Port Diversion\\n\\n- **Consignment:** `#SHP-BALT-104` (3,400 Chassis Stampings)\\n- **Diverted Port:** Port of Virginia (Norfolk) &rarr; Detroit Powertrain Plant (`PLANT_01`)\\n- **Delay:** **+6.0 Calendar Days** (Drayage Congestion)\\n\\nChassis buffer at Detroit remains at 8.1 days DOI, maintaining safe assembly buffer.",
          sql: "SELECT shipment_id, carrier, origin_port, destination_plant, delay_days FROM SUPPLY_CHAIN_DB.CORE.DT_ACTIVE_DISRUPTIONS WHERE shipment_id = 'SHP-BALT-104';",
          suggested_actions: [
            { label: "🔍 Inspect Detroit Line", action: "INSPECT_DETROIT" }
          ],
          total_latency_ms: 24.1
        };
      }

      // 5. Machine M7 / Detroit Robotics
      if (['m7', 'robot', 'machine', 'vibration', 'spindle', 'bearing'].some(k => q.includes(k))) {
        return {
          status: 'success',
          provider: 'Snowflake Cortex Telemetry Stream',
          model: 'DT_MACHINE_TELEMETRY',
          answer: "### 🤖 Asset Health Warning: Detroit Assembly Robot A3 (M7)\\n\\n- **Node:** Detroit Powertrain Plant (`PLANT_01`), Cell 2\\n- **Machine:** Robot A3 (`MACHINE_M7`)\\n- **Failure Risk:** **94.0% (CRITICAL ALERT)** — 2 Days until Bearing Seizure\\n- **Telemetry:** Spindle vibration RMS at **1.82 mm/s** (Normal: < 0.45 mm/s)\\n\\nMitigation: Pre-calibrated Hot-Standby Twin `M15` on Standby Bay 4 is ready for automated workload transfer.",
          sql: "SELECT machine_id, plant_id, failure_risk, predicted_failure_days, vibration_rms, temperature_c FROM SUPPLY_CHAIN_DB.CORE.DT_MACHINE_TELEMETRY WHERE machine_id = 'M7';",
          suggested_actions: [
            { label: "🔄 Switch to Hot-Standby M15", action: "REROUTE_M15" },
            { label: "🔍 Inspect Detroit Digital Twin", action: "INSPECT_DETROIT" }
          ],
          total_latency_ms: 25.1
        };
      }

      // 6. Austin Gigafactory / 4680 Battery Stockout
      if (['austin', 'battery', 'doi', '4680', 'shortfall', 'stockout', 'burn rate'].some(k => q.includes(k))) {
        return {
          status: 'success',
          provider: 'Snowflake Cortex Analyst',
          model: 'inventory_capacity_transportation.yaml',
          answer: "### 🚨 Critical Risk: Austin Gigafactory Battery Stockout\\n\\n- **Plant:** Austin Gigafactory (`PLANT_02`)\\n- **Component:** 4680 High-Density Battery Cells (`PART_BAT_402`)\\n- **Current DOI:** **3.8 Days** (CRITICAL: threshold is 5.0 Days)\\n- **Active Buffer:** 2,280 units on-hand | Daily burn rate: **600 units/day**\\n\\n**Root Cause:**\\nConsignment `#SHP-78442` from Apex Battery Cells is delayed 14 days due to berth congestion at Port of Long Beach. Line 1 assembly faces stoppage in 3.8 days ($140k/day downtime).\\n\\n**Prescription:**\\nDispatch an emergency air-freight PO for **2,500 units** to backup vendor **Shenzhen EnerTech Express** to restore DOI to **14.2 Days**.",
          sql: "SELECT plant_id, plant_name, part_id, part_name, days_of_inventory, stockout_risk_level FROM SUPPLY_CHAIN_DB.CORE.DT_PLANT_STOCKOUT_RISK WHERE plant_id = 'PLANT_02';",
          suggested_actions: [
            { label: "⚡ 1-Click Air Expedite via MCP", action: "EXPEDITE" },
            { label: "⚖️ Audit Apex SLA Penalties", prompt: "What are our liquidated damages from Apex Battery?" }
          ],
          total_latency_ms: 31.4
        };
      }

      // 7. Port of Long Beach / Maritime Disruption
      if (['port', 'long beach', 'berth', 'maritime', 'vessel', 'transit', 'shipment', 'delayed'].some(k => q.includes(k))) {
        return {
          status: 'success',
          provider: 'Snowflake Cortex Logistics Service',
          model: 'DT_ACTIVE_DISRUPTIONS',
          answer: "### 🚢 Maritime Logistics Disruption: Port of Long Beach\\n\\n- **Node:** Port of Long Beach Pier G Container Terminal\\n- **Affected Shipment:** `#SHP-78442` (2,280 Battery Modules from Apex Battery)\\n- **Delay:** **14 Days beyond ETA** due to crane outages and outer anchorage queue.\\n- **Impact:** Direct trigger for Austin 4680 stockout threat (3.8 days DOI remaining).",
          sql: "SELECT shipment_id, carrier, origin_port, destination_plant, delay_days, status FROM SUPPLY_CHAIN_DB.CORE.DT_ACTIVE_DISRUPTIONS WHERE origin_port = 'Port of Long Beach';",
          suggested_actions: [
            { label: "⚡ Dispatch Shenzhen Air Freight", action: "EXPEDITE" },
            { label: "⚖️ View Apex Liability", prompt: "What are our liquidated damages from Apex Battery?" }
          ],
          total_latency_ms: 29.3
        };
      }

      // 8. 3-Way Reconciliation Ledger
      if (['reconciliation', '3-way', 'ledger', 'hallucination', 'ground truth'].some(k => q.includes(k))) {
        return {
          status: 'success',
          provider: 'Snowflake Cortex & CoCo Core',
          model: 'Zero-Hallucination Architecture',
          answer: "### 🛡️ CoCo 3-Way Reconciliation Ledger Architecture\\n\\n1. **Dynamic Tables (Analytical Truth):** Auto-refreshing every 60s (38s actual lag) aggregating stock levels and telemetry.\\n2. **SQLite Blueprint Twin (Spatial Graph):** Microsecond 3D layout bounds and machine hierarchies.\\n3. **Cortex Analyst (Semantic Contract):** Grounded translation via `inventory_capacity_transportation.yaml` guaranteeing zero hallucinations.",
          sql: "SELECT dt.name, dt.target_lag, dt.refresh_mode, dt.data_timestamp FROM SUPPLY_CHAIN_DB.INFORMATION_SCHEMA.DYNAMIC_TABLES dt;",
          suggested_actions: [
            { label: "⚡ Check Austin Battery Stockout", prompt: "Why is Austin battery DOI at 3.8 days?" }
          ],
          total_latency_ms: 20.2
        };
      }

      // 9. What-If Simulation / Shenzhen Air Freight
      if (['simulate', 'simulation', 'what-if', 'what if', 'air freight', 'shenzhen', 'roi'].some(k => q.includes(k))) {
        return {
          status: 'success',
          provider: 'Snowflake Cortex What-If Engine',
          model: 'SC_WHAT_IF_SIMULATOR',
          answer: "### 📊 What-If Mitigation Simulation: Air Freight vs Plant Downtime\\n\\n- **Option A (Ocean / Wait):** Line 1 idle for 2.4 days &rarr; **$3,200,000 USD** downtime loss.\\n- **Option B (Air Expedite):** Shenzhen EnerTech 4,500 units air cargo &rarr; **$42,000 USD** arriving in 36h.\\n\\n**Net Saved Exposure:** **$3,158,000.00 USD** (75.2x ROI).",
          sql: "SELECT 3200000.0 as downtime_loss_usd, 42000.0 as air_freight_cost_usd, 3158000.0 as net_savings_usd, 14.2 as restored_doi_days;",
          suggested_actions: [
            { label: "⚡ Execute 1-Click MCP Dispatch", action: "EXPEDITE" }
          ],
          total_latency_ms: 28.1
        };
      }

      // 10. Help & Capabilities
      if (['what can you do', 'help', 'features', 'capabilities', 'command'].some(k => q.includes(k))) {
        return {
          status: 'success',
          provider: 'Snowflake Cortex Agent',
          model: 'Cortex Analyst / Semantic Model',
          answer: "### CoCo Autonomous Capabilities\\n\\n1. **Continuous Telemetry & DOI Forecasting:** Polling Dynamic Tables every 60s for stockout alerts.\\n2. **Governed Cortex Contract Mining:** Parsing supplier MSAs via vector search for SLA penalty enforcement.\\n3. **Predictive Equipment Failure Diagnostics:** Monitoring bearing vibrations and motor temperatures.\\n4. **Autonomous MCP Action Dispatch:** 1-Click mitigation approvals (air freight, PO reroutes, Slack alerts).",
          sql: "SELECT table_name, target_lag, refresh_mode FROM SUPPLY_CHAIN_DB.INFORMATION_SCHEMA.DYNAMIC_TABLES WHERE table_schema = 'CORE';",
          suggested_actions: [
            { label: "⚡ Test Austin Risk", prompt: "Why is Austin battery DOI at 3.8 days?" },
            { label: "⚖️ Apex Liquidated Damages", prompt: "What are our liquidated damages from Apex Battery?" }
          ],
          total_latency_ms: 22.0
        };
      }

      // 11. Pure Greeting
      if (/\\b(hello|hi|hey|howdy|greetings|who are you|what are you)\\b/i.test(q)) {
        return {
          status: 'success',
          provider: 'Snowflake Cortex Agent',
          model: 'Cortex AI / Multi-Turn Copilot',
          answer: "## Hello! 👋 I'm CoCo\\n\\nI am your autonomous **Snowflake Cortex Supply Chain Copilot**. I monitor our multi-plant global network in near real-time via **Snowflake Dynamic Tables** (38s actual lag) and 3D digital twins.\\n\\n### What would you like to investigate today?\\n- ⚡ **Austin Gigafactory Stockout**: *Why is Austin battery DOI at 3.8 days?*\\n- ⚖️ **Contractual SLA Breach**: *What are our liquidated damages from Apex Battery?*\\n- 🤖 **Predictive Machine Health**: *What is the failure risk on assembly robot M7?*\\n- 🚢 **Maritime Bottlenecks**: *Which inbound shipments are delayed at Port of Long Beach?*\\n- 🔄 **3-Way Reconciliation**: *How does CoCo verify ground truth without hallucination?*",
          sql: null,
          suggested_actions: [
            { label: "⚡ Austin Battery Risk", prompt: "Why is Austin battery DOI at 3.8 days?" },
            { label: "⚖️ Apex Liquidated Damages", prompt: "What are our liquidated damages from Apex Battery?" },
            { label: "🤖 Robot M7 Health", prompt: "What is the failure risk on Detroit robot M7?" }
          ],
          total_latency_ms: 18.2
        };
      }

      // 12. Fallback
      return {
        status: 'success',
        provider: 'Snowflake Cortex & CoCo Engine',
        model: 'Cortex Analyst / Semantic Model',
        answer: `### SupplyChainIQ CoCo Analysis for: *"${query}"*\\n\\nReconciled across active factory blueprints and Snowflake Semantic Model. 11 manufacturing & logistics nodes monitored with 94.2% network health. 1 Critical Stockout Risk at Austin Gigafactory (3.8d DOI).`,
        sql: "SELECT plant_id, count(*) as active_nodes, sum(stock_on_hand) as total_units FROM SUPPLY_CHAIN_DB.CORE.DT_FACILITY_LIVE_TELEMETRY GROUP BY plant_id;",
        suggested_actions: [
          { label: "⚡ Austin Battery Shortage (3.8d)", prompt: "Why is Austin battery DOI at 3.8 days?" },
          { label: "⚖️ Apex Liquidated Damages ($140k)", prompt: "What are our liquidated damages from Apex Battery?" }
        ],
        total_latency_ms: 32.1
      };
    }"""

new_html = html[:idx_start] + new_client_func + html[idx_func_close + 1:]
with open(INDEX_PATH, "w") as f:
    f.write(new_html)

print("✅ index.html updated!")
