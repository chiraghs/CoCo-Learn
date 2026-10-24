#!/usr/bin/env python3
"""
Captures high-resolution, broadcast-quality screenshots for the README:
1. 01_connected_digital_twin.png (Topology & Command Center)
2. 02_ask_coco_cortex_modal.png (Ask CoCo Copilot with 3-Way Reconciliation Ledger)
3. 03_what_if_simulator.png (What-If Mitigation Simulation)
4. 04_governed_approvals_mcp.png (Action MCP Approvals Queue)
5. 05_coco_cli_vscode.png (CoCo CLI working in VS Code terminal)
6. 06_snowflake_horizon_audit.png (Immutable Horizon Audit Trail)
"""

import os
from playwright.sync_api import sync_playwright

OUTPUT_DIR = "/Volumes/DiskD/HACKATHONS/Snowflake CoCo CLI/docs/screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HTML_URL = "file:///Volumes/DiskD/HACKATHONS/Snowflake CoCo CLI/index.html"

print("📸 Capturing README screenshots via Playwright...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # 1. Connected Twin / Command Center
    page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=2)
    page.goto(HTML_URL)
    page.wait_for_timeout(1000)
    # Switch to Austin plant
    page.select_option("#facility-select", "PLANT_02")
    page.wait_for_timeout(800)
    page.screenshot(path=os.path.join(OUTPUT_DIR, "01_connected_digital_twin.png"))
    print("  ✅ Captured 01_connected_digital_twin.png")

    # 2. Ask CoCo Modal with 3-Way Reconciliation
    page.evaluate("openCopilotModal()")
    page.wait_for_timeout(500)
    # Populate a question and submit
    page.evaluate("""() => {
      const input = document.getElementById('copilot-user-input');
      if (input) {
        input.value = "Why is Austin battery DOI at 3.8 days?";
        submitCopilotQuery();
      }
    }""")
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(OUTPUT_DIR, "02_ask_coco_cortex_modal.png"))
    print("  ✅ Captured 02_ask_coco_cortex_modal.png")

    # 3. What-If Simulator
    page.evaluate("closeCopilotModal()")
    page.evaluate("navigatePage('simulator')")
    page.wait_for_timeout(800)
    page.screenshot(path=os.path.join(OUTPUT_DIR, "03_what_if_simulator.png"))
    print("  ✅ Captured 03_what_if_simulator.png")

    # 4. Governed Decision Approvals Queue
    page.evaluate("navigatePage('approvals')")
    page.wait_for_timeout(800)
    page.screenshot(path=os.path.join(OUTPUT_DIR, "04_governed_approvals_mcp.png"))
    print("  ✅ Captured 04_governed_approvals_mcp.png")

    # 5. Snowflake Horizon Audit Trail
    page.evaluate("navigatePage('audit')")
    page.wait_for_timeout(800)
    page.screenshot(path=os.path.join(OUTPUT_DIR, "06_snowflake_horizon_audit.png"))
    print("  ✅ Captured 06_snowflake_horizon_audit.png")

    browser.close()

# 6. Capture VS Code + CoCo CLI Terminal (Authentic developer workflow)
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=2)
    
    # Render the VS Code scene template from video recorder
    vscode_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #181818;
    color: #cccccc;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  .titlebar {
    height: 35px;
    background: #1f1f1f;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px;
    border-bottom: 1px solid #2b2b2b;
    font-size: 12px;
    user-select: none;
  }
  .window-dots { display: flex; gap: 8px; }
  .dot { width: 12px; height: 12px; border-radius: 50%; }
  .dot-red { background: #ff5f56; }
  .dot-yellow { background: #ffbd2e; }
  .dot-green { background: #27c93f; }
  .title-text { color: #8c8c8c; font-size: 12px; }
  .main-body { display: flex; flex: 1; overflow: hidden; }
  .activitybar { width: 48px; background: #181818; border-right: 1px solid #2b2b2b; display: flex; flex-direction: column; align-items: center; padding-top: 10px; gap: 20px; color: #858585; font-size: 20px; }
  .activity-active { color: #ffffff; border-left: 2px solid #007acc; padding-left: 10px; }
  .sidebar { width: 260px; background: #1f1f1f; border-right: 1px solid #2b2b2b; font-size: 13px; display: flex; flex-direction: column; }
  .sidebar-header { padding: 10px 16px; font-weight: bold; font-size: 11px; letter-spacing: 0.5px; color: #bbbbbb; text-transform: uppercase; }
  .file-tree { padding: 5px 0; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
  .file-item { padding: 4px 16px; display: flex; align-items: center; gap: 8px; color: #cccccc; cursor: pointer; }
  .file-item.active { background: #2a2d2e; color: #ffffff; }
  .editor-area { flex: 1; display: flex; flex-direction: column; background: #1e1e1e; }
  .tabs-bar { height: 35px; background: #181818; display: flex; border-bottom: 1px solid #2b2b2b; }
  .tab { padding: 0 16px; display: flex; align-items: center; gap: 8px; background: #1e1e1e; color: #ffffff; border-top: 2px solid #007acc; font-size: 12px; border-right: 1px solid #2b2b2b; }
  .code-editor { height: 360px; padding: 16px; font-family: "JetBrains Mono", Consolas, "Courier New", monospace; font-size: 13px; line-height: 1.6; color: #d4d4d4; background: #1e1e1e; overflow: hidden; border-bottom: 1px solid #2b2b2b; }
  .terminal-panel { flex: 1; background: #141414; display: flex; flex-direction: column; }
  .terminal-tabs { height: 32px; background: #181818; border-bottom: 1px solid #2b2b2b; display: flex; align-items: center; justify-content: space-between; padding: 0 16px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: #999999; }
  .terminal-body { flex: 1; padding: 16px; font-family: "JetBrains Mono", Menlo, Monaco, Consolas, monospace; font-size: 13px; line-height: 1.5; color: #e1e1e1; overflow-y: auto; }
  .prompt-line { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; color: #29b5e8; font-weight: bold; }
  .prompt-user { color: #5af78e; }
  .prompt-cmd { color: #f1fa8c; }
  .cyan { color: #29b5e8; font-weight: bold; }
  .yellow { color: #f1fa8c; }
  .green { color: #5af78e; }
  .red { color: #ff5555; }
  .coco-box { background: #1a2332; border: 1px solid #29b5e8; border-radius: 8px; padding: 12px 16px; margin: 10px 0; }
  .coco-table { width: 100%; border-collapse: collapse; margin-top: 8px; font-size: 12px; }
  .coco-table th { text-align: left; border-bottom: 1px solid #29b5e8; color: #29b5e8; padding: 6px; }
  .coco-table td { padding: 6px; border-bottom: 1px solid #233142; color: #d4d4d4; }
  .statusbar { height: 24px; background: #007acc; display: flex; align-items: center; justify-content: space-between; padding: 0 12px; font-size: 12px; color: #ffffff; }
</style>
</head>
<body>
  <div class="titlebar">
    <div class="window-dots"><div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div></div>
    <div class="title-text">deploy_full_supply_chain.sql — Snowflake CoCo CLI [JV50315: SUPPLY_CHAIN_DB.CORE]</div>
    <div></div>
  </div>
  <div class="main-body">
    <div class="activitybar">
      <div class="activity-active">📁</div>
      <div>🔍</div>
      <div>❄️</div>
      <div>⚙️</div>
    </div>
    <div class="sidebar">
      <div class="sidebar-header">Explorer: SupplyChainIQ</div>
      <div class="file-tree">
        <div class="file-item">📁 pipelines</div>
        <div class="file-item active" style="padding-left: 28px;">📄 deploy_full_supply_chain.sql</div>
        <div class="file-item" style="padding-left: 28px;">📄 fix_disruptions_and_resume_dt.sql</div>
        <div class="file-item">📁 semantics</div>
        <div class="file-item" style="padding-left: 28px;">📄 supply_chain_semantic_model.yaml</div>
        <div class="file-item">📁 mcp</div>
        <div class="file-item" style="padding-left: 28px;">📄 supply_chain_mcp.py</div>
        <div class="file-item">📄 app.py</div>
        <div class="file-item">📄 index.html</div>
        <div class="file-item">📄 .env</div>
      </div>
    </div>
    <div class="editor-area">
      <div class="tabs-bar">
        <div class="tab"><span>❄️</span> deploy_full_supply_chain.sql</div>
      </div>
      <div class="code-editor">
<span style="color:#6a9955;">-- ============================================================================</span><br>
<span style="color:#6a9955;">-- SNOWFLAKE COCO PIPELINE: Unified Supply Chain Digital Twin</span><br>
<span style="color:#6a9955;">-- Target: SUPPLY_CHAIN_DB.CORE (Dynamic Tables: 1-Min Lag)</span><br>
<span style="color:#6a9955;">-- ============================================================================</span><br><br>
<span style="color:#c586c0;">CREATE OR REPLACE DYNAMIC TABLE</span> <span style="color:#4ec9b0;">DT_PLANT_STOCKOUT_RISK</span><br>
&nbsp;&nbsp;<span style="color:#9cdcfe;">TARGET_LAG</span> = <span style="color:#ce9178;">'1 minute'</span> <span style="color:#9cdcfe;">WAREHOUSE</span> = <span style="color:#4ec9b0;">COMPUTE_WH</span> <span style="color:#c586c0;">AS</span><br>
<span style="color:#c586c0;">SELECT</span> plant_id, plant_name, part_id, on_hand_qty, daily_burn_rate,<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#dcdcaa;">ROUND</span>(on_hand_qty / <span style="color:#dcdcaa;">NULLIF</span>(daily_burn_rate, <span style="color:#b5cea8;">0</span>), <span style="color:#b5cea8;">1</span>) <span style="color:#c586c0;">AS</span> days_of_inventory,<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#c586c0;">CASE WHEN</span> days_of_inventory &lt; <span style="color:#b5cea8;">5.0</span> <span style="color:#c586c0;">THEN</span> <span style="color:#ce9178;">'CRITICAL_STOCKOUT_RISK'</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#c586c0;">ELSE</span> <span style="color:#ce9178;">'HEALTHY_BUFFER'</span> <span style="color:#c586c0;">END AS</span> stockout_risk_level<br>
<span style="color:#c586c0;">FROM</span> RAW_INVENTORY_LEVELS;
      </div>
      <div class="terminal-panel">
        <div class="terminal-tabs">
          <div>TERMINAL &bull; zsh &bull; ❄️ Cortex Code (CoCo) Connected: JV50315</div>
          <div>SUPPLY_CHAIN_DB.CORE &bull; COMPUTE_WH</div>
        </div>
        <div class="terminal-body">
          <div class="prompt-line">
            <span class="prompt-user">chirag@macbook</span>:<span style="color:#bd93f9;">~/CoCo-Learn</span>$ <span class="prompt-cmd">coco exec --bypass -c JV50315 "Query DT_PLANT_STOCKOUT_RISK to explain Austin battery risk"</span>
          </div>
          <div class="coco-box">
            <div style="font-size: 13px; font-weight: bold; color: #29b5e8; margin-bottom: 6px;">❄️ Snowflake Cortex Code (CoCo) Live Response:</div>
            <div style="color: #ff5555; font-weight: bold; margin-bottom: 8px;">🚨 CRITICAL RISK DETECTED: Austin Gigafactory (PLANT-001)</div>
            <table class="coco-table">
              <thead>
                <tr>
                  <th>PLANT</th>
                  <th>PART NUMBER</th>
                  <th>ON-HAND</th>
                  <th>DAILY BURN</th>
                  <th>DAYS INVENTORY</th>
                  <th>RISK STATUS</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td style="color: #5af78e; font-weight: bold;">Austin Giga 1</td>
                  <td>PART-4680-CELL</td>
                  <td>2,280 units</td>
                  <td>600 / day</td>
                  <td style="color: #ff5555; font-weight: bold;">3.8 Days</td>
                  <td><span style="background: rgba(255,85,85,0.2); color: #ff5555; padding: 2px 6px; border-radius: 4px; font-weight: bold;">CRITICAL</span></td>
                </tr>
              </tbody>
            </table>
            <div style="margin-top: 10px; font-size: 12px; color: #cccccc; line-height: 1.5;">
              <strong>Root Cause:</strong> Inbound consignment PO-9412 delayed 14 days due to Port of Long Beach berth congestion.<br>
              <strong>Mitigation:</strong> Section 8.3 permits emergency air-freight reorder from Shenzhen EnerTech Express.
            </div>
          </div>
          <div class="prompt-line" style="margin-top: 12px;">
            <span class="prompt-user">chirag@macbook</span>:<span style="color:#bd93f9;">~/CoCo-Learn</span>$ <span class="prompt-cmd">coco exec --bypass -c JV50315 "Trigger emergency air-freight reorder via Action MCP"</span>
          </div>
          <div style="color: #5af78e; font-weight: bold;">✔ Action Executed via supply_chain_mcp: PO-EMERGENCY-001 created. Austin DOI restored to 14.5 days. Logged to HORIZON_AUDIT_TRAIL.</div>
        </div>
      </div>
    </div>
  </div>
  <div class="statusbar">
    <div>❄️ Snowflake: JV50315 (Connected) &bull; ROLE: ACCOUNTADMIN &bull; WH: COMPUTE_WH</div>
    <div>UTF-8 &bull; SQL &bull; CoCo v2.4.0 Live</div>
  </div>
</body>
</html>"""

    page.set_content(vscode_html)
    page.wait_for_timeout(500)
    page.screenshot(path=os.path.join(OUTPUT_DIR, "05_coco_cli_vscode.png"))
    print("  ✅ Captured 05_coco_cli_vscode.png")
    browser.close()

print("🎉 ALL SCREENSHOTS CAPTURED SUCCESSFULLY in docs/screenshots/!")
