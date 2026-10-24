#!/usr/bin/env python3
import sys

INDEX_FILE = "/Volumes/DiskD/HACKATHONS/Snowflake CoCo CLI/index.html"

with open(INDEX_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# Target 1: Greeting condition
old_greeting = "if (q.includes('hello') || q.includes('hi') || q.includes('who are you') || q.includes('hey')) {"
new_greeting = """const isGreeting = /\\b(hello|hi|hey|howdy|greetings|who are you|what are you)\\b/i.test(q);
      const hasDomainTopic = ['austin', 'battery', 'doi', '4680', 'shortfall', 'penalty', 'penalties', 'liquidated', 'apex', 'section 8', 'damages', 'm7', 'robot', 'machine', 'vibration', 'port', 'long beach', 'shipment', 'red sea', 'suez', 'tsmc', 'baltimore', 'reconciliation', '3-way', 'hallucination', 'simulate', 'simulation', 'what-if'].some(k => q.includes(k));
      if (isGreeting && !hasDomainTopic) {"""

if old_greeting in text:
    text = text.replace(old_greeting, new_greeting, 1)
    print("Replaced greeting condition successfully.")
else:
    print("Warning: old_greeting not found!")

# Target 2: Insert Long Beach, 3-Way Reconciliation, and Simulation after TSMC block
tsmc_marker = "if (q.includes('tsmc') || q.includes('semiconductor') || q.includes('chip') || q.includes('mcu')) {"
idx = text.find(tsmc_marker)
if idx != -1:
    # Find the closing of the TSMC block
    block_end = text.find("return {", idx)
    block_close = text.find("};", block_end) + 2
    
    extra_blocks = """
      if (['port', 'long beach', 'berth', 'maritime', 'vessel', 'shipment', 'delayed'].some(k => q.includes(k))) {
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
      }"""
    text = text[:block_close] + "\n" + extra_blocks + text[block_close:]
    print("Added extra blocks successfully.")
else:
    print("Warning: TSMC marker not found!")

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(text)

print("index.html patched cleanly.")
