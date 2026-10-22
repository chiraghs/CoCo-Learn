#!/usr/bin/env python3
"""scripts/record_vscode_coco_cli_video.py
Generates a broadcast-quality 1080p video demonstration of Snowflake CoCo working directly
inside the VS Code integrated terminal and editor.

Runtime: Strictly under 2 minutes (~100 seconds).
Features:
- Authentic VS Code IDE (Activity bar, Explorer, Editor showing Snowflake SQL pipelines).
- VS Code Integrated Terminal running CoCo CLI (`coco -c JV50315`).
- Turn 1: Object discovery & Dynamic Tables schema inspection (`SUPPLY_CHAIN_DB.CORE`).
- Turn 2: Querying `DT_PLANT_STOCKOUT_RISK` for Austin Gigafactory 3.8 Days DOI.
- Turn 3: Auditing `RAW_SUPPLIER_CONTRACTS` Section 8.2 ($140,000 Apex liquidated damages).
- Turn 4: Autonomous mitigation via Action MCP & Section 8.3 backup sourcing (Shenzhen EnerTech).
"""

import os
import subprocess
import time
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORK_DIR = os.path.join(BASE_DIR, "scripts", "vscode_video_temp")
OUTPUT_VIDEO = os.path.join(BASE_DIR, "static", "videos", "coco_cli_vscode_demo.mp4")
BACKUP_VIDEO = os.path.join(BASE_DIR, "static", "coco_demo.mp4")

os.makedirs(WORK_DIR, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "static", "videos"), exist_ok=True)

NARRATION_SCRIPTS = [
    {
        "id": "scene_1_vscode_intro",
        "title": "Snowflake CoCo CLI in VS Code",
        "text": (
            "Welcome to the Snowflake CoCo CLI demonstration, operating directly inside Visual Studio Code. "
            "CoCo, the Cortex Code CLI, connects natively to our Snowflake account through connection JV50315, "
            "empowering developers and supply chain operators to reason over physical digital twins, Dynamic Tables, and contracts without ever leaving the editor."
        ),
        "terminal_input": "coco -c JV50315",
        "terminal_output": """<span class="coco-badge">❄️ Cortex Code (CoCo) v2.4.0</span> &bull; Active Connection: <span class="cyan">JV50315</span> (hf55215.ap-northeast-1.aws)
Initialized session for database: <span class="bold">SUPPLY_CHAIN_DB</span> &bull; warehouse: <span class="bold">COMPUTE_WH</span>
Available tools: SQL_EXECUTE, CORTEX_SEARCH, DYNAMIC_TABLE_MONITOR, MCP_DISPATCH
Type your prompt or question in plain English below:"""
    },
    {
        "id": "scene_2_schema_discovery",
        "title": "Turn 1: Dynamic Tables & Object Discovery",
        "text": (
            "First, we ask CoCo to inspect our supply chain schema. "
            "CoCo executes metadata discovery across SUPPLY_CHAIN_DB.CORE, identifying our eleven core objects, "
            "including our one-minute lag Dynamic Tables: DT_PLANT_STOCKOUT_RISK, DT_ACTIVE_DISRUPTIONS, and our vectorized supplier contracts."
        ),
        "terminal_input": "Show all tables and dynamic tables in SUPPLY_CHAIN_DB.CORE",
        "terminal_output": """The <span class="cyan">SUPPLY_CHAIN_DB.CORE</span> schema has 11 objects actively monitored:

<span class="yellow">| Table / Dynamic Table           | Type          | Rows | Target Lag |</span>
|----------------------------------|---------------|------|------------|
| CONFIG_RULES                     | Table         | 1    | N/A        |
| DIM_PARTS                        | Table         | 5    | N/A        |
| DIM_PLANTS                       | Table         | 4    | N/A        |
| <span class="green">DT_ACTIVE_DISRUPTIONS</span>            | Dynamic Table | 1    | 1 MINUTE   |
| <span class="red">DT_PLANT_STOCKOUT_RISK</span>           | Dynamic Table | 4    | 1 MINUTE   |
| DT_SUPPLIER_PERFORMANCE          | Dynamic Table | 6    | 1 MINUTE   |
| FACT_INVENTORY                   | Table         | 4    | N/A        |
| RAW_SUPPLIER_CONTRACTS           | Table         | 1    | N/A        |

All Dynamic Tables are active and updating continuously with sub-minute lag."""
    },
    {
        "id": "scene_3_stockout_analysis",
        "title": "Turn 2: Grounded Stockout Analysis (Austin 3.8d)",
        "text": (
            "Next, we query our stockout risk. "
            "CoCo queries DT_PLANT_STOCKOUT_RISK and flags a critical alert on Austin Gigafactory 1. "
            "With two thousand two hundred and eighty battery cells on hand and a burn rate of six hundred units daily, "
            "Austin has only 3.8 days of inventory remaining due to berth congestion at the Port of Long Beach."
        ),
        "terminal_input": "Query DT_PLANT_STOCKOUT_RISK to explain the Austin battery stockout risk",
        "terminal_output": """<span class="red-bg bold"> 🚨 CRITICAL_STOCKOUT_RISK: Austin Gigafactory 1 (PLANT_02) </span>

<span class="cyan bold">Component:</span> PART_BAT_402 (High-Density Lithium Battery Module)
&bull; <span class="bold">Stock on Hand:</span> 2,280 units | <span class="bold">Daily Burn Rate:</span> 600 units/day
&bull; <span class="red bold">Days of Inventory (DOI):</span> 2,280 ÷ 600 = <span class="red bold">3.8 Days</span> (Safety threshold: 5.0 Days)

<span class="yellow bold">Comparative Plant Inventory Across Network:</span>
| Site                            | On Hand | Daily Burn | Days of Inventory | Risk Level |
|---------------------------------|---------|------------|-------------------|------------|
| <span class="red">Austin Gigafactory 1</span>           | 2,280   | 600        | <span class="red bold">3.8 Days</span>          | <span class="red bold">CRITICAL</span>   |
| Fremont Assembly Plant          | 4,800   | 450        | 10.7 Days         | BALANCED   |
| Riverside Smart Logistics Hub   | 1,412   | 100        | 14.1 Days         | BALANCED   |

<span class="bold">Root Cause:</span> Inbound consignment #SHP-78442 delayed 14 days at Port of Long Beach outer anchorage."""
    },
    {
        "id": "scene_4_contract_audit",
        "title": "Turn 3: Cortex Contract Search ($140k Liquidated Damages)",
        "text": (
            "We now audit the supplier contract. "
            "We ask CoCo to inspect RAW_SUPPLIER_CONTRACTS for Apex Battery Cells. "
            "CoCo extracts Section 8.2 of the Master Service Agreement, calculates fourteen days of delay past the three-day grace period, "
            "and establishes a hundred and forty thousand dollars in enforceable liquidated damages."
        ),
        "terminal_input": "Check RAW_SUPPLIER_CONTRACTS for Apex Battery Section 8.2 liquidated damages clause",
        "terminal_output": """<span class="green-bg bold"> ⚖️ CONTRACT AUDIT: CTR_APEX_2024 (Apex Battery Cells Ltd) </span>

<span class="cyan bold">Grounded Clause &bull; Section 8.2 (Liquidated Damages for Inbound Delays):</span>
&bull; <span class="bold">Grace Period:</span> 3 Business Days.
&bull; <span class="bold">Daily Penalty:</span> 5% base contract penalty <span class="green bold">+ USD $10,000 per calendar day</span> of delay.
&bull; <span class="bold">Delay Duration:</span> 14 Calendar Days past dispatch window.

<span class="yellow bold">Enforceable Damages Calculation:</span>
5% Order Base ($30,000) + 11 Billable Delay Days × $10,000/day ($110,000) = <span class="green bold">$140,000.00 USD Recoverable</span>

<span class="bold">Cross-Reference Clause 8.3:</span>
Buyer is legally authorized to source replacement modules from secondary vendor <span class="cyan bold">Shenzhen EnerTech Express</span>; 
Apex is strictly liable for expedited freight differential."""
    },
    {
        "id": "scene_5_mcp_mitigation",
        "title": "Turn 4: 1-Click Action MCP Mitigation",
        "text": (
            "Finally, we execute the mitigation. "
            "CoCo formulates an emergency purchase order to Shenzhen EnerTech under Clause 8.3. "
            "Through our Model Context Protocol server on Port 8000, the air-freight order dispatches immediately to ERP, "
            "restoring Austin's inventory runway to 14.2 days and logging an immutable record in Snowflake Horizon."
        ),
        "terminal_input": "Dispatch emergency air-freight PO to Shenzhen EnerTech via MCP to restore Austin DOI",
        "terminal_output": """<span class="green-bg bold"> ✅ ACTION DISPATCHED VIA MCP SERVER (Port 8000) </span>

<span class="cyan bold">Dispatched Action:</span> EXPEDITE_AND_REROUTE_PO
&bull; <span class="bold">Emergency PO ID:</span> EXP-9412-AIR | <span class="bold">Vendor:</span> Shenzhen EnerTech Express
&bull; <span class="bold">Volume:</span> 2,500 Units (PART_BAT_402) | <span class="bold">Mode:</span> Chartered Air Cargo
&bull; <span class="green bold">New Projected DOI:</span> <span class="green bold">14.2 Days (Runway Restored)</span>
&bull; <span class="bold">Downtime Prevented:</span> 91.2 Hours ($140,000/day savings)
&bull; <span class="bold">ERP Status:</span> Synced &bull; <span class="bold">Slack Alert:</span> Dispatched to #supply-chain-crisis

<span class="cyan">Snowflake Horizon Audit:</span> Recorded immutable transaction hash <span class="bold">0x8f2d...c419</span>."""
    }
]

VSCODE_HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            width: 1920px;
            height: 1080px;
            background: #181818;
            color: #CCCCCC;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}
        
        /* 1. VS Code Titlebar */
        .titlebar {{
            height: 38px;
            background: #1F1F1F;
            border-bottom: 1px solid #2B2B2B;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 16px;
            font-size: 12px;
            color: #999999;
            user-select: none;
        }}
        .window-controls {{
            display: flex;
            gap: 8px;
        }}
        .circle {{ width: 12px; height: 12px; border-radius: 50%; }}
        .red-dot {{ background: #FF5F56; }}
        .yellow-dot {{ background: #FFBD2E; }}
        .green-dot {{ background: #27C93F; }}
        .title-center {{
            font-weight: 500;
            color: #CCCCCC;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .search-box {{
            background: #2D2D2D;
            border: 1px solid #3C3C3C;
            border-radius: 6px;
            padding: 3px 24px;
            font-size: 11px;
            color: #888888;
        }}

        /* 2. Main Workbench */
        .workbench {{
            display: flex;
            flex: 1;
            height: calc(1080px - 38px - 26px);
        }}

        /* Activity Bar */
        .activitybar {{
            width: 50px;
            background: #181818;
            border-right: 1px solid #2B2B2B;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 12px 0;
            gap: 20px;
        }}
        .act-icon {{
            font-size: 22px;
            color: #858585;
            cursor: pointer;
        }}
        .act-icon.active {{
            color: #FFFFFF;
            border-left: 2px solid #29B5E8;
            padding-left: 4px;
        }}

        /* Sidebar File Explorer */
        .sidebar {{
            width: 280px;
            background: #181818;
            border-right: 1px solid #2B2B2B;
            display: flex;
            flex-direction: column;
            font-size: 13px;
        }}
        .sidebar-header {{
            padding: 10px 16px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #888888;
            border-bottom: 1px solid #222222;
        }}
        .tree-section {{
            padding: 8px 12px;
            font-size: 11px;
            font-weight: 700;
            color: #AAAAAA;
        }}
        .file-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 5px 18px;
            color: #CCCCCC;
            font-size: 12.5px;
            cursor: pointer;
        }}
        .file-item.active {{
            background: #04395E;
            color: #FFFFFF;
        }}
        .file-item:hover {{
            background: #2A2D2E;
        }}

        /* Editor & Terminal Area */
        .editor-area {{
            flex: 1;
            display: flex;
            flex-direction: column;
            background: #1E1E1E;
        }}

        /* Editor Tabs */
        .tabs-bar {{
            height: 38px;
            background: #181818;
            display: flex;
            border-bottom: 1px solid #2B2B2B;
        }}
        .tab {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 0 16px;
            font-size: 12px;
            background: #181818;
            color: #969696;
            border-right: 1px solid #252525;
            cursor: pointer;
        }}
        .tab.active {{
            background: #1E1E1E;
            color: #FFFFFF;
            border-top: 2px solid #29B5E8;
        }}

        /* Code Viewer Top (Half Screen) */
        .code-pane {{
            height: 320px;
            background: #1E1E1E;
            padding: 16px 24px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            line-height: 1.6;
            overflow: hidden;
            border-bottom: 1px solid #333333;
        }}
        .sql-kw {{ color: #569CD6; font-weight: 700; }}
        .sql-fn {{ color: #DCDCAA; }}
        .sql-str {{ color: #CE9178; }}
        .sql-comment {{ color: #6A9955; font-style: italic; }}
        .sql-id {{ color: #9CDCFE; }}
        .line-num {{ color: #5A5A5A; margin-right: 16px; user-select: none; }}

        /* Integrated Terminal (Bottom Half Screen) */
        .terminal-panel {{
            flex: 1;
            background: #141414;
            display: flex;
            flex-direction: column;
        }}
        .terminal-header {{
            height: 34px;
            background: #181818;
            border-top: 1px solid #2B2B2B;
            border-bottom: 1px solid #252525;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 16px;
            font-size: 11px;
            color: #999999;
        }}
        .term-tabs {{
            display: flex;
            gap: 16px;
        }}
        .term-tab.active {{
            color: #FFFFFF;
            border-bottom: 1px solid #FFFFFF;
            padding-bottom: 6px;
        }}
        .term-body {{
            flex: 1;
            padding: 20px 28px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            line-height: 1.55;
            color: #E2E8F0;
            overflow-y: auto;
        }}
        .prompt-line {{
            color: #29B5E8;
            font-weight: 700;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .cmd-text {{
            color: #FFFFFF;
            font-weight: 700;
        }}
        .output-box {{
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(41, 181, 232, 0.2);
            border-radius: 12px;
            padding: 16px 20px;
            margin: 12px 0 20px 0;
            white-space: pre-wrap;
            font-size: 13.5px;
        }}

        /* Color Helpers */
        .cyan {{ color: #29B5E8; }}
        .green {{ color: #10B981; }}
        .red {{ color: #EF4444; }}
        .yellow {{ color: #F59E0B; }}
        .bold {{ font-weight: 700; }}
        .red-bg {{ background: rgba(239, 68, 68, 0.2); color: #EF4444; padding: 2px 8px; border-radius: 4px; }}
        .green-bg {{ background: rgba(16, 185, 129, 0.2); color: #10B981; padding: 2px 8px; border-radius: 4px; }}
        .coco-badge {{
            background: rgba(41, 181, 232, 0.2);
            color: #29B5E8;
            border: 1px solid rgba(41, 181, 232, 0.4);
            padding: 2px 8px;
            border-radius: 6px;
            font-weight: 800;
        }}

        /* 3. VS Code Status Bar */
        .statusbar {{
            height: 26px;
            background: #007ACC;
            color: #FFFFFF;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 14px;
            font-size: 11px;
            font-weight: 600;
        }}
        .status-left, .status-right {{
            display: flex;
            gap: 14px;
            align-items: center;
        }}
    </style>
</head>
<body>

    <!-- Top Window Titlebar -->
    <div class="titlebar">
        <div class="window-controls">
            <span class="circle red-dot"></span>
            <span class="circle yellow-dot"></span>
            <span class="circle green-dot"></span>
        </div>
        <div class="title-center">
            <span>Snowflake CoCo CLI &bull; Visual Studio Code</span>
            <span class="search-box">🔍 Snowflake CoCo CLI (Workspace)</span>
        </div>
        <div style="font-size: 11px; color: #888888;">Layout: Editor + CoCo Terminal</div>
    </div>

    <!-- Main Workbench -->
    <div class="workbench">
        <!-- Activity Bar -->
        <div class="activitybar">
            <span class="act-icon active">📁</span>
            <span class="act-icon">🔍</span>
            <span class="act-icon">🌿</span>
            <span class="act-icon">❄️</span>
            <span class="act-icon">⚙️</span>
        </div>

        <!-- Sidebar File Explorer -->
        <div class="sidebar">
            <div class="sidebar-header">Explorer: Snowflake CoCo CLI</div>
            <div class="tree-section">&or; SNOWFLAKE COCO CLI</div>
            <div class="file-item">📁 pipelines</div>
            <div class="file-item active">📄 deploy_full_supply_chain.sql</div>
            <div class="file-item">📄 insert_real_world_events.sql</div>
            <div class="file-item">📁 core / api</div>
            <div class="file-item">🐍 routes_copilot.py</div>
            <div class="file-item">📁 semantics</div>
            <div class="file-item">📋 inventory_capacity.yaml</div>
            <div class="file-item">🌐 index.html</div>
            <div class="file-item">📘 CoCo_Skills.md</div>
            <div class="file-item">📘 DEPLOYMENT.md</div>
        </div>

        <!-- Editor & Terminal Area -->
        <div class="editor-area">
            <!-- Open Editor Tabs -->
            <div class="tabs-bar">
                <div class="tab active">
                    <span>📄</span>
                    <span>deploy_full_supply_chain.sql</span>
                    <span>&times;</span>
                </div>
                <div class="tab">
                    <span>🐍</span>
                    <span>routes_copilot.py</span>
                </div>
                <div class="tab">
                    <span>🌐</span>
                    <span>index.html</span>
                </div>
            </div>

            <!-- Code Viewer (Top Half) -->
            <div class="code-pane">
                <div><span class="line-num">1</span><span class="sql-comment">-- SUPPLYCHAINIQ: Snowflake Cortex Dynamic Tables Pipeline</span></div>
                <div><span class="line-num">2</span><span class="sql-kw">USE ROLE</span> <span class="sql-id">ACCOUNTADMIN</span>; <span class="sql-kw">USE DATABASE</span> <span class="sql-id">SUPPLY_CHAIN_DB</span>; <span class="sql-kw">USE SCHEMA</span> <span class="sql-id">CORE</span>;</div>
                <div><span class="line-num">3</span></div>
                <div><span class="line-num">4</span><span class="sql-kw">CREATE OR REPLACE DYNAMIC TABLE</span> <span class="sql-id">DT_PLANT_STOCKOUT_RISK</span></div>
                <div><span class="line-num">5</span><span class="sql-kw">TARGET_LAG</span> = <span class="sql-str">'1 MINUTE'</span> <span class="sql-kw">WAREHOUSE</span> = <span class="sql-id">COMPUTE_WH</span></div>
                <div><span class="line-num">6</span><span class="sql-kw">AS SELECT</span></div>
                <div><span class="line-num">7</span>  <span class="sql-id">plant_id</span>, <span class="sql-id">plant_name</span>, <span class="sql-id">part_id</span>, <span class="sql-id">part_name</span>, <span class="sql-id">stock_on_hand</span>, <span class="sql-id">daily_burn_rate</span>,</div>
                <div><span class="line-num">8</span>  <span class="sql-fn">ROUND</span>(<span class="sql-id">stock_on_hand</span> / <span class="sql-fn">NULLIF</span>(<span class="sql-id">daily_burn_rate</span>, 0), 1) <span class="sql-kw">AS</span> <span class="sql-id">days_of_inventory</span>,</div>
                <div><span class="line-num">9</span>  <span class="sql-kw">CASE WHEN</span> (<span class="sql-id">stock_on_hand</span> / <span class="sql-fn">NULLIF</span>(<span class="sql-id">daily_burn_rate</span>, 0)) &lt; 5.0 <span class="sql-kw">THEN</span> <span class="sql-str">'CRITICAL_STOCKOUT_RISK'</span> <span class="sql-kw">ELSE</span> <span class="sql-str">'BALANCED'</span> <span class="sql-kw">END</span> <span class="sql-kw">AS</span> <span class="sql-id">stockout_risk_level</span></div>
                <div><span class="line-num">10</span><span class="sql-kw">FROM</span> <span class="sql-id">FACT_INVENTORY</span>;</div>
            </div>

            <!-- Integrated Terminal (Bottom Half) -->
            <div class="terminal-panel">
                <div class="terminal-header">
                    <div class="term-tabs">
                        <span class="term-tab active">TERMINAL: CoCo CLI (cortex)</span>
                        <span class="term-tab">OUTPUT</span>
                        <span class="term-tab">PROBLEMS</span>
                        <span class="term-tab">DEBUG CONSOLE</span>
                    </div>
                    <div>zsh &bull; ❄️ Connection: JV50315</div>
                </div>

                <div class="term-body">
                    <div class="prompt-line">
                        <span>chiraghs@chiraghs-MacBook-Air Snowflake CoCo CLI %</span>
                        <span class="cmd-text">{terminal_input}</span>
                    </div>
                    <div class="output-box">{terminal_output}</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bottom Status Bar -->
    <div class="statusbar">
        <div class="status-left">
            <span>🌿 main*</span>
            <span>⟳ 0 &darr; 0 &uarr;</span>
            <span>❄️ Snowflake: JV50315 (Connected)</span>
            <span>Role: ACCOUNTADMIN</span>
            <span>Warehouse: COMPUTE_WH</span>
        </div>
        <div class="status-right">
            <span>Ln 10, Col 42</span>
            <span>Spaces: 2</span>
            <span>UTF-8</span>
            <span>SQL</span>
            <span>CoCo Agent: Ready</span>
        </div>
    </div>

</body>
</html>
"""

def generate_voiceovers():
    """Generates crystal-clear audio narration files using macOS TTS."""
    print("🎙️ Generating studio voiceover using macOS TTS (Samantha @ 185 wpm)...")
    audio_files = []
    total_dur = 0.0
    for item in NARRATION_SCRIPTS:
        sid = item["id"]
        aiff_path = os.path.join(WORK_DIR, f"{sid}.aiff")
        wav_path = os.path.join(WORK_DIR, f"{sid}.wav")
        
        # High quality TTS
        subprocess.run(["/usr/bin/say", "-v", "Samantha", "-r", "185", "-o", aiff_path, item["text"]], check=True)
        subprocess.run(["/opt/homebrew/bin/ffmpeg", "-y", "-i", aiff_path, "-ar", "44100", "-ac", "2", wav_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        # Probe exact duration
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", wav_path]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        dur = float(res.stdout.strip() or 18.0)
        total_dur += dur
        audio_files.append({"id": sid, "wav": wav_path, "duration": dur})
        print(f"  ✅ {sid}: {dur:.1f}s")
        
    print(f"⏱️ Total Narration Duration: {total_dur:.1f}s (< 120s: {'YES ✅' if total_dur < 120 else 'NO ⚠️'})")
    return audio_files

def render_vscode_scenes(audio_files):
    """Renders 1080p high-resolution visual scenes of VS Code & CoCo CLI."""
    print("📸 Rendering broadcast 1080p VS Code scenes via Playwright...")
    clip_paths = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        
        for idx, item in enumerate(NARRATION_SCRIPTS):
            sid = item["id"]
            wav_file = audio_files[idx]["wav"]
            dur = audio_files[idx]["duration"] + 1.2
            
            html_content = VSCODE_HTML_TEMPLATE.format(
                terminal_input=item["terminal_input"],
                terminal_output=item["terminal_output"]
            )
            html_file = os.path.join(WORK_DIR, f"{sid}.html")
            png_file = os.path.join(WORK_DIR, f"{sid}.png")
            clip_file = os.path.join(WORK_DIR, f"{sid}.mp4")
            
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(html_content)
                
            page.goto(f"file://{html_file}")
            page.wait_for_timeout(350)
            page.screenshot(path=png_file, full_page=False)
            
            # Encode MP4 clip looped with narration audio
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
            print(f"  🎞️ Rendered & Encoded {sid}.mp4 ({dur:.1f}s)")
            
        browser.close()
    return clip_paths

def concatenate_final_video(clips):
    """Concatenates all VS Code clips into the final video."""
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
        OUTPUT_VIDEO
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # Copy to backup location
    subprocess.run(["cp", OUTPUT_VIDEO, BACKUP_VIDEO], check=True)
    
    # Probe final duration
    probe_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", OUTPUT_VIDEO]
    res = subprocess.run(probe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    final_dur = float(res.stdout.strip() or 0.0)
    
    file_size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
    print("=" * 75)
    print("🎉 COCO CLI IN VS CODE DEMO VIDEO COMPLETE!")
    print(f"📁 Video Location: {OUTPUT_VIDEO}")
    print(f"⏱️ Video Duration: {final_dur:.2f} seconds (< 2 minutes: {'YES ✅' if final_dur < 120 else 'NO ⚠️'})")
    print(f"📦 File Size: {file_size_mb:.2f} MB")
    print(f"🔗 Mirrored to: {BACKUP_VIDEO}")
    print("=" * 75)
    return OUTPUT_VIDEO, final_dur

if __name__ == "__main__":
    t0 = time.time()
    audio_files = generate_voiceovers()
    clips = render_vscode_scenes(audio_files)
    final_video, dur = concatenate_final_video(clips)
    print(f"✨ Workflow finished in {time.time() - t0:.1f}s.")
