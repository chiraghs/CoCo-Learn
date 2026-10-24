# ⚡ SupplyChainIQ — Autonomous Snowflake Cortex Digital Twin & Governed Control Tower

> **Snowflake Cortex Code CLI Hackathon (GCC Edition)**  
> **Team:** Aegis &bull; **Track:** Track 5 — Supply Chain Ontology & Governed Analytics  
> **Snowflake Production Account:** `ZJXLXUZ.JV50315` (`hf55215.ap-northeast-1.aws`) &bull; **Database:** `SUPPLY_CHAIN_DB.CORE`

[![Snowflake](https://img.shields.io/badge/Snowflake-Cortex%20AI%20%2B%20Dynamic%20Tables-29B5E8?logo=snowflake&logoColor=white)](https://app.snowflake.com/ZJXLXUZ/JV50315/)
[![CoCo CLI](https://img.shields.io/badge/CoCo%20CLI-v2.4.0-7928CA?logo=visualstudiocode&logoColor=white)](https://github.com/chiraghs/CoCo-Learn)
[![FastAPI](https://img.shields.io/badge/FastAPI-2.0.0-009688?logo=fastapi&logoColor=white)](https://supplychainiq.onrender.com)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

---

## 🌐 Live Prototype & Submission Links

* 🖥️ **Live Web Showcase & Interactive Simulator:** [https://chiraghs.github.io/CoCo-Learn/](https://chiraghs.github.io/CoCo-Learn/)
* 🚀 **Render Full-Stack Deployment:** [https://supplychainiq.onrender.com](https://supplychainiq.onrender.com)
* ❄️ **Native Streamlit in Snowflake (SiS) App:** [https://app.snowflake.com/ZJXLXUZ/JV50315/#/streamlit-apps/SUPPLY_CHAIN_DB.CORE.SUPPLY_CHAIN_COMMAND_CENTER](https://app.snowflake.com/ZJXLXUZ/JV50315/#/streamlit-apps/SUPPLY_CHAIN_DB.CORE.SUPPLY_CHAIN_COMMAND_CENTER)
* 🎬 **Unified Demo Video (< 2 Minutes: 112s):** [`static/coco_demo.mp4`](static/coco_demo.mp4) (UI Walkthrough + VS Code CoCo CLI)
* 📊 **Pitch Decks & Presentation Slides:** [showcase_overview.html](https://chiraghs.github.io/CoCo-Learn/showcase_overview.html)

---

## 📸 Platform Screenshots & Evidence

### 1. 🌐 Connected 3D Digital Twin & Real-Time Command Center
Real-time spatial visualization of the global supply network, dock turnaround times, active forklift telemetry, and dynamic buffer health across Austin, Fremont, Berlin, and Newark.
<p align="center"><img src="https://raw.githubusercontent.com/chiraghs/CoCo-Learn/main/docs/screenshots/01_connected_digital_twin.png" alt="Connected 3D Digital Twin & Real-Time Command Center" width="100%"/></p>

---

### 2. 💬 Ask CoCo — Snowflake Cortex Agent & 3-Way Reconciliation Ledger
Natural language conversational copilot powered by **Snowflake Cortex Analyst** and **Meta LLaMA 3.1 70B**. Every answer is cryptographically cross-verified against deterministic SQL queries and raw Dynamic Table state to eliminate hallucinations.
<p align="center"><img src="https://raw.githubusercontent.com/chiraghs/CoCo-Learn/main/docs/screenshots/02_ask_coco_cortex_modal.png" alt="Ask CoCo Copilot with 3-Way Reconciliation Ledger" width="100%"/></p>

---

### 3. 📊 Cortex What-If Mitigation Simulator (Air Freight vs Plant Downtime)
Quantifies financial ROI and operational impact: compares idling the Austin Gigafactory line ($3.2M downtime loss) against dispatching a 4,500-unit emergency air-freight batch from Shenzhen EnerTech ($42,000 cost), delivering **$3,158,000 in net preserved exposure**.
<p align="center"><img src="https://raw.githubusercontent.com/chiraghs/CoCo-Learn/main/docs/screenshots/03_what_if_simulator.png" alt="Cortex What-If Mitigation Simulator" width="100%"/></p>

---

### 4. ⚖️ Governed Decision Approvals Queue & 1-Click Action MCP
Human-in-the-loop operational governance. Review pending legal liquidated damage claims ($140,000 against Apex Battery Ltd under Section 8.2) and execute 1-click PO expediting via the Model Context Protocol (MCP).
<p align="center"><img src="https://raw.githubusercontent.com/chiraghs/CoCo-Learn/main/docs/screenshots/04_governed_approvals_mcp.png" alt="Governed Decision Approvals Queue & Action MCP" width="100%"/></p>

---

### 5. 💻 CoCo CLI Developer Workflow in VS Code
End-to-end command-line workflow inside the VS Code integrated terminal using `coco -c JV50315`. Introspects Dynamic Tables, queries stockout alerts, extracts legal contract terms, and invokes MCP write actions.
<p align="center"><img src="https://raw.githubusercontent.com/chiraghs/CoCo-Learn/main/docs/screenshots/05_coco_cli_vscode.png" alt="CoCo CLI Working Live in VS Code Terminal" width="100%"/></p>

---

### 6. 🛡️ Snowflake Horizon Audit Trail & Cryptographic Governance
Immutable audit ledger recording every automated prediction, user approval, MCP dispatch, and SQL execution with SHA-256 integrity hashes under strict Snowflake role-based access control (`ACCOUNTADMIN`).
<p align="center"><img src="https://raw.githubusercontent.com/chiraghs/CoCo-Learn/main/docs/screenshots/06_snowflake_horizon_audit.png" alt="Snowflake Horizon Audit Trail & Cryptographic Governance" width="100%"/></p>

---

## 🏛️ System Architecture: The 3-Way Reconciliation Protocol

Traditional generative AI assistants hallucinate database states because they rely on ungrounded text completion. **SupplyChainIQ** guarantees **100% zero-hallucination accuracy** by enforcing a **3-Way Reconciliation Protocol**:

```
                       ┌──────────────────────────────────────┐
                       │     USER / OPERATOR CONVERSATION     │
                       └──────────────────┬───────────────────┘
                                          │
                                          ▼
                      ┌────────────────────────────────────────┐
                      │        CORTEX ANALYST & AGENT          │
                      │ (Meta LLaMA 3.1 70B / Semantic Model)  │
                      └───────────────────┬────────────────────┘
                                          │
             ┌────────────────────────────┼────────────────────────────┐
             ▼                            ▼                            ▼
┌──────────────────────────┐ ┌──────────────────────────┐ ┌──────────────────────────┐
│   1. ANALYTICAL TRUTH    │ │    2. SPATIAL GRAPH      │ │   3. GOVERNED CONTRACT   │
│ Snowflake Dynamic Tables │ │  SQLite In-Memory Twin   │ │  Semantic Contract YAML   │
│ (1-min lag / 38s actual) │ │ (Microsecond CAD Bounds) │ │ (inventory_capacity.yaml)  │
└────────────┬─────────────┘ └────────────┬─────────────┘ └────────────┬─────────────┘
             │                            │                            │
             └────────────────────────────┼────────────────────────────┘
                                          ▼
                      ┌────────────────────────────────────────┐
                      │      3-WAY RECONCILIATION LEDGER       │
                      │  ✔ Narrative matches SQL & Ground Truth│
                      └───────────────────┬────────────────────┘
                                          │
                                          ▼
                      ┌────────────────────────────────────────┐
                      │    ACTION MCP SERVER & HORIZON AUDIT   │
                      │   1-Click PO Expedite + Slack Alerts   │
                      └────────────────────────────────────────┘
```

---

## ❓ 10 High-Impact Questions to Ask CoCo

| # | Domain Category | Natural Language Prompt | Snowflake Underlying Engine |
|---|---|---|---|
| **1** | **Stockout Risk** | *"Why is Austin battery DOI at 3.8 days?"* | `DT_PLANT_STOCKOUT_RISK` |
| **2** | **Port Bottleneck** | *"Which inbound shipments are delayed at Port of Long Beach?"* | `DT_ACTIVE_DISRUPTIONS` |
| **3** | **Contract Legal Audit** | *"What are our liquidated damages from Apex Battery under Section 8.2?"* | `SNOWFLAKE.CORTEX.SEARCH_PREVIEW` |
| **4** | **Financial Damages** | *"Calculate enforceable damages for the 14-day delay on shipment SHP-401"* | Cortex LLM + SQL Arithmetic ($140k claim) |
| **5** | **Secondary Sourcing** | *"Does Section 8.3 permit alternative backup sourcing?"* | Vectorized Contract Search (Shenzhen EnerTech) |
| **6** | **Geopolitical Maritime** | *"Are any shipments diverted through the Red Sea or Cape of Good Hope?"* | `DT_ACTIVE_DISRUPTIONS` (+12 days, $85k demurrage) |
| **7** | **Predictive Robotics** | *"What is the failure risk on Detroit assembly robot M7?"* | `DT_MACHINE_TELEMETRY` (94% failure risk in 48h) |
| **8** | **What-If Simulation** | *"Simulate air freight reorder from Shenzhen vs plant shutdown"* | What-If Simulator ($3.158M net saved loss) |
| **9** | **Action MCP Dispatch** | *"Trigger 1-click emergency PO expediting via Action MCP"* | `mcp/supply_chain_mcp.py` (`EXP_PO_0401`) |
| **10** | **Horizon Governance** | *"How does CoCo verify ground truth without hallucination?"* | 3-Way Reconciliation & `HORIZON_AUDIT_TRAIL` |

---

## 🛠️ Mandatory CoCo Full-Lifecycle Adoption

| Phase | Activities Demonstrated with CoCo | Artifact Location |
|---|---|---|
| **1. Planning** | Domain discovery, ontology hierarchy closure, and ERD generation | [`docs/architecture_plan.md`](docs/architecture_plan.md) |
| **2. Development** | Synthetic data generation, Dynamic Tables DDL, Semantic YAML authoring | [`pipelines/`](pipelines/) & [`semantics/`](semantics/) |
| **3. Orchestration** | Running pipeline DAGs, 1-min lag refreshes, and Action MCP tool dispatch | [`mcp/supply_chain_mcp.py`](mcp/supply_chain_mcp.py) |
| **4. Validation** | 3-Way Reconciliation verification, error fallback, and audit logging | [`tests/`](tests/) & [`core/snowflake_client.py`](core/snowflake_client.py) |

---

## 🚀 Local Quickstart

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/chiraghs/CoCo-Learn.git
cd CoCo-Learn
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Snowflake Credentials (`.env`)
```bash
SNOWFLAKE_CONNECTION=JV50315
SNOWFLAKE_ACCOUNT=hf55215.ap-northeast-1.aws
SNOWFLAKE_USER=CHIRAG
SNOWFLAKE_ROLE=ACCOUNTADMIN
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=SUPPLY_CHAIN_DB
SNOWFLAKE_SCHEMA=CORE
```

### 3. Run CoCo CLI Queries
```bash
coco -c JV50315
coco exec --bypass -c JV50315 "Query DT_PLANT_STOCKOUT_RISK in SUPPLY_CHAIN_DB.CORE"
```

### 4. Launch Full-Stack Application
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 👥 Team & Submission Information
* **Team:** Aegis
* **Lead Architect:** Chirag H S
* **Competition:** Snowflake Cortex Code CLI Hackathon (GCC Edition)
* **Track:** Track 5 — Supply Chain Ontology & Governed Analytics
* **Snowflake Account:** `ZJXLXUZ.JV50315`
