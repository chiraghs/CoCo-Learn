#!/usr/bin/env python3
"""scripts/make_coco_demo_video.py
Generates a broadcast-quality 1080p demonstration video for Snowflake Cortex & CoCo.
Runtime: Under 2 minutes (~105 seconds).
Explains:
1. Multi-Plant Digital Twin & Snowflake Dynamic Tables (1-min lag).
2. Real-World Disruption 1: Port of Long Beach berth congestion & Austin battery stockout (3.8d DOI).
3. Real-World Disruption 2: Red Sea / Suez Canal crisis & Cape of Good Hope diversions.
4. CoCo Conversational Cortex AI, multi-turn reasoning, and 3-Way Reconciliation Ledger.
5. 1-Click Governed Action MCP Mitigation & Slack crisis escalation.
"""

import os
import subprocess
import time
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORK_DIR = os.path.join(BASE_DIR, "scripts", "video_gen_temp")
OUTPUT_DIR = os.path.join(BASE_DIR, "static", "videos")
FINAL_MP4 = os.path.join(OUTPUT_DIR, "coco_cortex_platform_demo.mp4")
BACKUP_MP4 = os.path.join(BASE_DIR, "static", "coco_demo.mp4")

os.makedirs(WORK_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "static"), exist_ok=True)

SCENES = [
    {
        "id": "scene_1_intro",
        "title": "SupplyChainIQ: Autonomous Digital Twin Studio",
        "subtitle": "Powered by Snowflake Cortex AI, Dynamic Tables & Iceberg • Near Zero Latency",
        "narration": (
            "Welcome to SupplyChainIQ, the autonomous industrial digital twin studio built natively on Snowflake Cortex. "
            "By reconciling high-frequency factory telemetry with global logistics into Snowflake Dynamic Tables, "
            "our platform provides continuous analytical truth with a 38-second actual lag across our entire manufacturing network."
        ),
        "html": """
        <div class="card">
            <div class="badge-row">
                <span class="badge cyan">❄️ Snowflake Cortex AI</span>
                <span class="badge blue">⚡ 1-Minute Dynamic Tables</span>
                <span class="badge green">🧊 Iceberg Semantic Layer</span>
            </div>
            <h1 class="main-title">SupplyChain<span class="highlight">IQ</span></h1>
            <p class="tagline">Autonomous Multi-Plant Digital Twin & Governed Cortex Reasoning</p>
            <div class="grid-stats">
                <div class="stat-box">
                    <div class="stat-num">11</div>
                    <div class="stat-label">Active Plants & Hubs</div>
                </div>
                <div class="stat-box">
                    <div class="stat-num">38s</div>
                    <div class="stat-label">Dynamic Table Lag</div>
                </div>
                <div class="stat-box">
                    <div class="stat-num">100%</div>
                    <div class="stat-label">Grounded SQL Ledger</div>
                </div>
                <div class="stat-box">
                    <div class="stat-num">&lt; 35ms</div>
                    <div class="stat-label">Cortex Query Latency</div>
                </div>
            </div>
            <div class="facility-preview">
                <div class="fac-chip">🏭 Gigafactory Texas (Austin, USA)</div>
                <div class="fac-chip">⚡ Apex Powertrain Plant (Detroit, USA)</div>
                <div class="fac-chip">🔄 Bavaria Mechatronics Hub (Munich, Germany)</div>
                <div class="fac-chip">📦 Riverside Smart Logistics Hub (California, USA)</div>
            </div>
        </div>
        """
    },
    {
        "id": "scene_2_austin_longbeach",
        "title": "Real-World Crisis 1: Port of Long Beach & Austin Battery Runway",
        "subtitle": "Consignment #SHP-78442 • Berth Congestion • Days of Inventory Crashes to 3.8 Days",
        "narration": (
            "In Austin Gigafactory, real-world supply disruption strikes. "
            "Consignment SHP-78442 is delayed fourteen days by severe berth congestion at the Port of Long Beach. "
            "Austin's battery cell inventory crashes to 3.8 days, breaching safety limits and threatening a 140,000-dollar daily assembly line stoppage."
        ),
        "html": """
        <div class="card">
            <div class="badge-row">
                <span class="badge red">🚨 CRITICAL STOCKOUT ALERT</span>
                <span class="badge dark">Austin Gigafactory • Assembly Line 1</span>
            </div>
            <h2 class="section-title">Component: 4680 High-Density Battery Cells (PART_BAT_402)</h2>
            <div class="grid-2col">
                <div class="alert-box alert-red">
                    <div class="box-title">Inventory Runway & Stockout Curve</div>
                    <div class="metric-row">
                        <span>Current Stock On-Hand:</span>
                        <span class="metric-val">2,280 Units</span>
                    </div>
                    <div class="metric-row">
                        <span>Daily Assembly Burn Rate:</span>
                        <span class="metric-val">600 Units / Day</span>
                    </div>
                    <div class="metric-row">
                        <span>Days of Inventory (DOI):</span>
                        <span class="metric-val red-text">3.8 Days (CRITICAL)</span>
                    </div>
                    <div class="metric-row">
                        <span>Downtime Penalty Exposure:</span>
                        <span class="metric-val red-text">$140,000 / Day</span>
                    </div>
                </div>
                <div class="alert-box">
                    <div class="box-title">Maritime Root Cause: Port of Long Beach Pier G</div>
                    <p class="desc-text">
                        Carrier <b>Pacific Horizon Shipping</b> is delayed 14 days. Pier G outer anchorage currently reports 22 vessels idling with 96-hour discharge delays.
                    </p>
                    <div class="action-rec">
                        <span class="rec-title">Prescribed Mitigation:</span>
                        <span>Emergency Air-Freight PO to Shenzhen EnerTech (Restores buffer to 14.2 Days).</span>
                    </div>
                </div>
            </div>
        </div>
        """
    },
    {
        "id": "scene_3_red_sea_suez",
        "title": "Real-World Crisis 2: Red Sea & Suez Canal Geopolitical Diversion",
        "subtitle": "Consignment #SHP-SUEZ-992 • Cape of Good Hope Transit • Munich Mechatronics Hub",
        "narration": (
            "Simultaneously, geopolitical conflict in the Red Sea diverts container vessels around the Cape of Good Hope. "
            "Consignment SHP-SUEZ-992 incurs twelve days of transit delay and 85,000 dollars in demurrage, triggering automated Dynamic Table alerts across our European Munich hub."
        ),
        "html": """
        <div class="card">
            <div class="badge-row">
                <span class="badge amber">🌊 MARITIME GEOPOLITICAL EVENT</span>
                <span class="badge blue">Maersk Line Triple-E • Bab-el-Mandeb Divert</span>
            </div>
            <h2 class="section-title">Munich Mechatronics Hub: Power Inverter Consignment</h2>
            <div class="grid-2col">
                <div class="alert-box">
                    <div class="box-title">Vessel Navigation Reroute</div>
                    <div class="metric-row">
                        <span>Original Route:</span>
                        <span class="metric-val">Suez Canal / Red Sea</span>
                    </div>
                    <div class="metric-row">
                        <span>Reroute Trajectory:</span>
                        <span class="metric-val amber-text">Cape of Good Hope (+4,500 nm)</span>
                    </div>
                    <div class="metric-row">
                        <span>Cumulative Transit Delay:</span>
                        <span class="metric-val red-text">+12.0 Days</span>
                    </div>
                    <div class="metric-row">
                        <span>Fuel & Demurrage Surcharge:</span>
                        <span class="metric-val">$85,000.00 USD</span>
                    </div>
                </div>
                <div class="alert-box">
                    <div class="box-title">Snowflake Dynamic Table Reconciliation</div>
                    <p class="desc-text">
                        Dynamic Table <code>DT_ACTIVE_DISRUPTIONS</code> flags Munich inverter runway compressing to 4.2 days. 
                        Contract Section 14.4 caps war-risk surcharges at $45,000, triggering an automated $40,000 carrier insurance recovery.
                    </p>
                </div>
            </div>
        </div>
        """
    },
    {
        "id": "scene_4_coco_chat_reconciliation",
        "title": "Ask CoCo: Conversational Multi-Turn Cortex Agent",
        "subtitle": "Natural Language Reasoning • Vectorized Contract Search • 3-Way Reconciliation Ledger",
        "narration": (
            "We open Ask CoCo, our conversational Cortex Agent. "
            "In plain English, we ask: 'What are our liquidated damages from Apex Battery under Section 8.2?' "
            "Grounded by Cortex Search over vectorized contracts, CoCo parses the legal grace period, computes eleven billable delay days, and proves 140,000 dollars in recoverable penalties with a verified SQL ledger."
        ),
        "html": """
        <div class="card">
            <div class="badge-row">
                <span class="badge cyan">💬 Ask CoCo</span>
                <span class="badge blue">Cortex Vector Search</span>
                <span class="badge green">Zero Hallucination</span>
            </div>
            <h2 class="section-title">Conversational Contract Audit & SLA Calculation</h2>
            <div class="chat-container">
                <div class="chat-bubble user-bubble">
                    <strong>USER:</strong> What are our enforceable liquidated damages from Apex Battery under Section 8.2?
                </div>
                <div class="chat-bubble coco-bubble">
                    <div class="coco-header">
                        <span>❄️ CoCo Cortex Agent &bull; SUPPLIER_CONTRACTS_SEARCH</span>
                        <span class="latency-tag">⚡ 28.5ms</span>
                    </div>
                    <p><strong>Master Service Agreement &bull; Section 8.2 Liquidated Damages:</strong></p>
                    <p>Inbound PO-9412 is delayed 14 calendar days. Factoring the 72-hour grace period (11 billable days):</p>
                    <div class="calc-box">
                        5% PO Base ($30,000) + 11 Days × $10,000/day ($110,000) = <strong class="green-text">$140,000.00 USD Recoverable</strong>
                    </div>
                    <div class="sql-box">
                        <code>SELECT PARSE_JSON(SNOWFLAKE.CORTEX.SEARCH_PREVIEW('SUPPLY_CHAIN_DB.CORE.SUPPLIER_CONTRACTS_SEARCH', '{"query": "Apex Battery liquidated damages Section 8"}'))['results'][0]['clause_text']::STRING;</code>
                    </div>
                </div>
            </div>
        </div>
        """
    },
    {
        "id": "scene_5_mcp_action_approvals",
        "title": "Closed-Loop Governance: 1-Click Action MCP Mitigation",
        "subtitle": "Human-in-the-Loop Approvals • ERP Dispatch • Slack Crisis Alerts • Horizon Audit",
        "narration": (
            "To solve the Austin stockout, CoCo formulates an executable prescription: "
            "dispatching emergency air freight to backup supplier Shenzhen EnerTech. "
            "With one click, our Model Context Protocol dispatches the purchase order to ERP and posts an alert to Slack, restoring Austin runway to 14.2 days with zero downtime."
        ),
        "html": """
        <div class="card">
            <div class="badge-row">
                <span class="badge green">✅ 1-CLICK ACTION READY</span>
                <span class="badge blue">Model Context Protocol (MCP)</span>
                <span class="badge dark">Snowflake Horizon Audit</span>
            </div>
            <h2 class="section-title">Governed Decision Approvals & Autonomous Execution</h2>
            <div class="grid-2col">
                <div class="approval-card border-green">
                    <div class="card-head">
                        <span class="tag-badge green-bg">STOCKOUT MITIGATION</span>
                        <span class="dec-id">DEC-SUPPLY-02</span>
                    </div>
                    <p class="card-title">Dispatch Emergency Air-Freight PO to Shenzhen EnerTech</p>
                    <p class="card-desc">2,500 battery units shipped via charter air transit. Replaces delayed maritime batch.</p>
                    <div class="impact-row">
                        <span>Runway Impact:</span>
                        <span class="green-text">Austin DOI Restored: 3.8d &rarr; 14.2 Days</span>
                    </div>
                    <div class="btn-demo">⚡ Approved via MCP (Port 8000) &rarr; ERP Synced</div>
                </div>
                <div class="approval-card border-blue">
                    <div class="card-head">
                        <span class="tag-badge blue-bg">LEGAL RECOVERY</span>
                        <span class="dec-id">DEC-LEGAL-01</span>
                    </div>
                    <p class="card-title">Issue SLA Breach & $140,000 Liquidated Damages Notice</p>
                    <p class="card-desc">Grounded in Master Service Agreement Section 8.2 against Apex Battery Cells.</p>
                    <div class="impact-row">
                        <span>Recovery Amount:</span>
                        <span class="green-text">$140,000.00 Claim Recorded</span>
                    </div>
                    <div class="btn-demo blue-btn">📢 Dispatched to #supply-chain-crisis on Slack</div>
                </div>
            </div>
        </div>
        """
    },
    {
        "id": "scene_6_architecture_conclusion",
        "title": "Autonomous Enterprise Resilience on Snowflake Cortex",
        "subtitle": "Physical Digital Twin ↔ Snowflake Dynamic Tables ↔ Cortex Agent ↔ Action MCP",
        "narration": (
            "From sensor telemetry to governed execution, "
            "Snowflake Cortex and CoCo deliver complete operational resilience with zero hallucination. "
            "Welcome to the future of intelligent, self-healing supply chains."
        ),
        "html": """
        <div class="card">
            <div class="badge-row">
                <span class="badge cyan">Enterprise Architecture</span>
                <span class="badge green">Zero Hallucination</span>
                <span class="badge blue">Continuous Resilience</span>
            </div>
            <h1 class="main-title">Continuous <span class="highlight">Intelligence</span></h1>
            <p class="tagline">The Full-Stack Snowflake Cortex Supply Chain Studio</p>
            <div class="arch-flow">
                <div class="flow-step">
                    <div class="step-icon">🏭</div>
                    <div class="step-name">3D Digital Twin</div>
                    <div class="step-sub">Deterministic Blueprints</div>
                </div>
                <div class="flow-arrow">&rarr;</div>
                <div class="flow-step">
                    <div class="step-icon">⚡</div>
                    <div class="step-name">Dynamic Tables</div>
                    <div class="step-sub">1-Min Near Real-Time Lag</div>
                </div>
                <div class="flow-arrow">&rarr;</div>
                <div class="flow-step">
                    <div class="step-icon">❄️</div>
                    <div class="step-name">CoCo Cortex Agent</div>
                    <div class="step-sub">Semantic Views & Vector Search</div>
                </div>
                <div class="flow-arrow">&rarr;</div>
                <div class="flow-step">
                    <div class="step-icon">🛠️</div>
                    <div class="step-name">Action MCP Server</div>
                    <div class="step-sub">1-Click Governed Dispatch</div>
                </div>
            </div>
            <div class="footer-stats">
                <span>❄️ Snowflake Cortex Platform</span> &bull; 
                <span>🔒 Cryptographic Ledger Verification</span> &bull; 
                <span>🚀 Ready for Production Deployment</span>
            </div>
        </div>
        """
    }
]

SLIDE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&family=JetBrains+Mono:wght@500;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            width: 1920px;
            height: 1080px;
            background: radial-gradient(circle at 15% 15%, #0B192C 0%, #060D17 100%);
            color: #F8FAFC;
            font-family: 'Plus Jakarta Sans', sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            position: relative;
        }}
        .bg-grid {{
            position: absolute;
            inset: 0;
            background-image: 
                linear-gradient(rgba(41, 181, 232, 0.08) 1px, transparent 1px),
                linear-gradient(90deg, rgba(41, 181, 232, 0.08) 1px, transparent 1px);
            background-size: 60px 60px;
            pointer-events: none;
        }}
        .top-glow {{
            position: absolute;
            top: -150px;
            left: 20%;
            width: 900px;
            height: 450px;
            background: radial-gradient(circle, rgba(41, 181, 232, 0.22) 0%, transparent 70%);
            filter: blur(80px);
            pointer-events: none;
        }}
        .card {{
            position: relative;
            z-index: 10;
            width: 1680px;
            height: 920px;
            background: rgba(13, 27, 42, 0.75);
            backdrop-filter: blur(24px);
            border: 1.5px solid rgba(41, 181, 232, 0.28);
            border-radius: 36px;
            padding: 50px 70px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 40px 100px -20px rgba(0, 0, 0, 0.7), 0 0 50px rgba(41, 181, 232, 0.15);
        }}
        .badge-row {{
            display: flex;
            gap: 14px;
        }}
        .badge {{
            padding: 8px 18px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .badge.cyan {{ background: rgba(41, 181, 232, 0.15); color: #29B5E8; border: 1px solid rgba(41, 181, 232, 0.4); }}
        .badge.blue {{ background: rgba(59, 130, 246, 0.15); color: #60A5FA; border: 1px solid rgba(59, 130, 246, 0.4); }}
        .badge.green {{ background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.4); }}
        .badge.red {{ background: rgba(239, 68, 68, 0.15); color: #EF4444; border: 1px solid rgba(239, 68, 68, 0.4); }}
        .badge.amber {{ background: rgba(245, 158, 11, 0.15); color: #F59E0B; border: 1px solid rgba(245, 158, 11, 0.4); }}
        .badge.dark {{ background: rgba(255, 255, 255, 0.06); color: #94A3B8; border: 1px solid rgba(255, 255, 255, 0.12); }}
        
        .main-title {{
            font-size: 76px;
            font-weight: 900;
            letter-spacing: -2px;
            color: #FFFFFF;
            line-height: 1;
            margin-top: 15px;
        }}
        .section-title {{
            font-size: 42px;
            font-weight: 900;
            letter-spacing: -1px;
            color: #FFFFFF;
            margin: 10px 0 20px 0;
        }}
        .highlight {{ color: #29B5E8; }}
        .tagline {{
            font-size: 26px;
            color: #94A3B8;
            font-weight: 600;
            margin-top: 8px;
        }}
        .grid-stats {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 24px;
            margin: 20px 0;
        }}
        .stat-box {{
            background: rgba(17, 34, 56, 0.65);
            border: 1px solid rgba(41, 181, 232, 0.2);
            border-radius: 24px;
            padding: 30px;
            text-align: center;
        }}
        .stat-num {{
            font-size: 56px;
            font-weight: 900;
            color: #29B5E8;
            font-family: 'JetBrains Mono', monospace;
            line-height: 1.1;
        }}
        .stat-label {{
            font-size: 16px;
            font-weight: 700;
            color: #94A3B8;
            margin-top: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .facility-preview {{
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
        }}
        .fac-chip {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 14px 22px;
            border-radius: 16px;
            font-size: 17px;
            font-weight: 700;
            color: #E2E8F0;
        }}
        
        /* 2 Column Layout */
        .grid-2col {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 32px;
            flex: 1;
            margin: 15px 0;
        }}
        .alert-box {{
            background: rgba(17, 34, 56, 0.7);
            border: 1.5px solid rgba(41, 181, 232, 0.25);
            border-radius: 24px;
            padding: 36px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .alert-red {{
            border-color: rgba(239, 68, 68, 0.5);
            background: rgba(239, 68, 68, 0.05);
        }}
        .box-title {{
            font-size: 22px;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .metric-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            font-size: 18px;
            color: #CBD5E1;
        }}
        .metric-val {{
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
            font-size: 20px;
            color: #FFFFFF;
        }}
        .red-text {{ color: #EF4444 !important; }}
        .green-text {{ color: #10B981 !important; }}
        .amber-text {{ color: #F59E0B !important; }}
        .desc-text {{
            font-size: 20px;
            line-height: 1.6;
            color: #94A3B8;
        }}
        .action-rec {{
            background: rgba(41, 181, 232, 0.1);
            border: 1px solid rgba(41, 181, 232, 0.3);
            border-radius: 16px;
            padding: 20px;
            margin-top: 15px;
            font-size: 18px;
            color: #E2E8F0;
        }}
        .rec-title {{
            display: block;
            font-weight: 800;
            color: #29B5E8;
            font-size: 15px;
            text-transform: uppercase;
            margin-bottom: 6px;
            font-family: 'JetBrains Mono', monospace;
        }}
        
        /* Chat Layout */
        .chat-container {{
            display: flex;
            flex-direction: column;
            gap: 20px;
            flex: 1;
            margin: 15px 0;
        }}
        .chat-bubble {{
            border-radius: 24px;
            padding: 24px 32px;
            font-size: 20px;
            line-height: 1.5;
        }}
        .user-bubble {{
            align-self: flex-end;
            background: #29B5E8;
            color: #060D17;
            font-weight: 700;
            max-width: 80%;
            border-bottom-right-radius: 4px;
        }}
        .coco-bubble {{
            align-self: flex-start;
            background: rgba(17, 34, 56, 0.85);
            border: 1.5px solid rgba(41, 181, 232, 0.3);
            color: #F8FAFC;
            max-width: 90%;
            border-bottom-left-radius: 4px;
        }}
        .coco-header {{
            display: flex;
            justify-content: space-between;
            font-size: 14px;
            font-weight: 800;
            color: #29B5E8;
            font-family: 'JetBrains Mono', monospace;
            border-bottom: 1px solid rgba(41, 181, 232, 0.2);
            padding-bottom: 10px;
            margin-bottom: 14px;
        }}
        .calc-box {{
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 14px;
            padding: 14px 20px;
            margin: 14px 0;
            font-family: 'JetBrains Mono', monospace;
            font-size: 18px;
        }}
        .sql-box {{
            background: #060D17;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 14px 18px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            color: #29B5E8;
            overflow-x: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
        }}
        
        /* Approvals Layout */
        .approval-card {{
            background: rgba(17, 34, 56, 0.75);
            border-radius: 24px;
            padding: 32px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .border-green {{ border: 2px solid rgba(16, 185, 129, 0.5); }}
        .border-blue {{ border: 2px solid rgba(41, 181, 232, 0.5); }}
        .card-head {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .tag-badge {{
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
        }}
        .green-bg {{ background: rgba(16, 185, 129, 0.2); color: #10B981; }}
        .blue-bg {{ background: rgba(41, 181, 232, 0.2); color: #29B5E8; }}
        .dec-id {{ font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #94A3B8; font-weight: 700; }}
        .card-title {{ font-size: 24px; font-weight: 800; color: #FFFFFF; margin-top: 14px; }}
        .card-desc {{ font-size: 17px; color: #94A3B8; margin-top: 8px; }}
        .impact-row {{
            background: rgba(255, 255, 255, 0.04);
            border-radius: 14px;
            padding: 14px 18px;
            display: flex;
            justify-content: space-between;
            font-size: 17px;
            margin: 18px 0;
            font-family: 'JetBrains Mono', monospace;
        }}
        .btn-demo {{
            background: #10B981;
            color: #060D17;
            font-weight: 800;
            padding: 16px;
            border-radius: 14px;
            text-align: center;
            font-size: 17px;
        }}
        .blue-btn {{ background: #29B5E8; }}
        
        /* Flow Layout */
        .arch-flow {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 40px 0;
            gap: 16px;
        }}
        .flow-step {{
            flex: 1;
            background: rgba(17, 34, 56, 0.8);
            border: 1.5px solid rgba(41, 181, 232, 0.3);
            border-radius: 24px;
            padding: 30px 20px;
            text-align: center;
        }}
        .step-icon {{ font-size: 48px; margin-bottom: 12px; }}
        .step-name {{ font-size: 20px; font-weight: 800; color: #FFFFFF; }}
        .step-sub {{ font-size: 14px; color: #94A3B8; margin-top: 6px; font-family: 'JetBrains Mono', monospace; }}
        .flow-arrow {{ font-size: 40px; color: #29B5E8; font-weight: 900; }}
        .footer-stats {{
            text-align: center;
            font-size: 18px;
            color: #94A3B8;
            font-weight: 700;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
        }}
    </style>
</head>
<body>
    <div class="bg-grid"></div>
    <div class="top-glow"></div>
    {content}
</body>
</html>
"""

def generate_voiceover():
    """Generates broadcast TTS audio tracks for each storyboard scene."""
    print("🎙️ Generating studio voiceover using macOS TTS (Samantha @ 175 wpm)...")
    tracks = []
    for scene in SCENES:
        sid = scene["id"]
        aiff_file = os.path.join(WORK_DIR, f"{sid}.aiff")
        wav_file = os.path.join(WORK_DIR, f"{sid}.wav")
        text = scene["narration"]
        
        # macOS TTS
        subprocess.run(["/usr/bin/say", "-v", "Samantha", "-r", "190", "-o", aiff_file, text], check=True)
        # Convert to high-fidelity stereo WAV
        subprocess.run(["/opt/homebrew/bin/ffmpeg", "-y", "-i", aiff_file, "-ar", "44100", "-ac", "2", wav_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        # Probe exact duration
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", wav_file]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        dur = float(res.stdout.strip() or 18.0)
        tracks.append({"id": sid, "wav": wav_file, "duration": dur})
        print(f"  ✅ {sid}: {dur:.1f}s")
    return tracks

def render_slides_and_record():
    """Renders 1080p slide screenshots using Playwright."""
    print("📸 Rendering broadcast 1080p visual scenes via Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        
        for scene in SCENES:
            sid = scene["id"]
            html_content = SLIDE_TEMPLATE.format(content=scene["html"])
            html_file = os.path.join(WORK_DIR, f"{sid}.html")
            png_file = os.path.join(WORK_DIR, f"{sid}.png")
            
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(html_content)
                
            page.goto(f"file://{html_file}")
            page.wait_for_timeout(400)
            page.screenshot(path=png_file, full_page=False)
            print(f"  🖼️ Rendered {png_file}")
            
        browser.close()

def compile_scene_clips(tracks):
    """Compiles each PNG and WAV into a synchronized 1080p MP4 clip."""
    print("🎬 Encoding synchronized MP4 clips using ffmpeg...")
    clip_paths = []
    total_duration = 0.0
    
    for trk in tracks:
        sid = trk["id"]
        dur = trk["duration"] + 1.2 # add slight breathing tail
        total_duration += dur
        png_file = os.path.join(WORK_DIR, f"{sid}.png")
        wav_file = trk["wav"]
        clip_file = os.path.join(WORK_DIR, f"{sid}.mp4")
        
        # ffmpeg command: static PNG looped over audio track
        cmd = [
            "/opt/homebrew/bin/ffmpeg", "-y",
            "-loop", "1", "-i", png_file,
            "-i", wav_file,
            "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-t", f"{dur:.2f}",
            "-shortest",
            clip_file
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        clip_paths.append(clip_file)
        print(f"  🎞️ Compiled {sid}.mp4 ({dur:.1f}s)")
        
    print(f"⏱️ Total Estimated Video Duration: {total_duration:.1f}s (Target: < 120s)")
    return clip_paths, total_duration

def concatenate_final_video(clips):
    """Concatenates all scene clips into the final video."""
    print("🚀 Concatenating all scenes into final video...")
    concat_txt = os.path.join(WORK_DIR, "concat_list.txt")
    with open(concat_txt, "w") as f:
        for c in clips:
            f.write(f"file '{c}'\n")
            
    cmd = [
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_txt,
        "-c", "copy",
        FINAL_MP4
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # Copy to backup location
    subprocess.run(["cp", FINAL_MP4, BACKUP_MP4], check=True)
    
    # Verify final video length
    probe_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", FINAL_MP4]
    res = subprocess.run(probe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    final_dur = float(res.stdout.strip() or 0.0)
    
    file_size_mb = os.path.getsize(FINAL_MP4) / (1024 * 1024)
    print("=" * 70)
    print(f"🎉 BROADCAST DEMO VIDEO COMPLETE: {FINAL_MP4}")
    print(f"⏱️ Final Video Duration: {final_dur:.2f} seconds (< 2 minutes: {'YES ✅' if final_dur < 120 else 'NO ⚠️'})")
    print(f"📦 File Size: {file_size_mb:.2f} MB")
    print(f"🔗 Backup Mirrored to: {BACKUP_MP4}")
    print("=" * 70)
    return FINAL_MP4, final_dur

if __name__ == "__main__":
    t0 = time.time()
    tracks = generate_voiceover()
    render_slides_and_record()
    clips, est_dur = compile_scene_clips(tracks)
    final_video, real_dur = concatenate_final_video(clips)
    print(f"✨ Workflow finished in {time.time() - t0:.1f}s.")
