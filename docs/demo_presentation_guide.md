# Snowflake CoCo Hackathon: 3-Minute Demo Pitch Guide
## Track 5: Supply Chain Ontology & Governed Conversational Intelligence

---

## 🎯 The Hook & Narrative (30 Seconds)
* **The Pitch:** "In global manufacturing, supply chain data is scattered across ERP, logistics, and warehouse systems with inconsistent metrics. When a crisis strikes, the same question yields 3 different answers."
* **The Crisis Scenario:** "We are an electric vehicle manufacturer assembling powertrains across 3 Gigafactories (Austin, Fremont, Berlin). Port of Houston congestion has trapped shipments of high-density battery cells (`PART_BAT_402`)."
* **The Business Problem:**
  * VP of Procurement sees one delivery date.
  * Logistics Director sees container arrival dates.
  * Plant Operations Manager sees warehouse buffer dates.
  * *Result:* Zero single source of truth, leading to catastrophic plant shutdowns.

---

## ⚡ Live Demo Walkthrough (90 Seconds)

### Step 1: Show the Live Streamlit Command Center
* **URL:** `https://app.snowflake.com/ZJXLXUZ/JV50315/#/streamlit-apps/SUPPLY_CHAIN_DB.CORE.SUPPLY_CHAIN_COMMAND_CENTER`
* **Show Persona 1 (Plant Operations Manager):**
  * Point to the **3.8 Days of Inventory** metric badge (`CRITICAL_STOCKOUT_RISK`).
  * "CoCo's Dynamic Table continuously calculates the live burn rate (600 units/day) against available stock (2,280 units). In less than 4 days, Gigafactory Texas line stops."
* **Show Persona 2 (VP of Procurement):**
  * Switch persona in the sidebar.
  * "Notice how the metrics adapt instantly: Apex Battery Cells has 4 delayed shipments, an OTIF rate of 33.3%, and accumulated **$22,500** in liquidated damages."

### Step 2: Tab 2 — The Single Source of Truth Proof
* Click **Tab 2: Governed vs Ungoverned Truth**.
* Show judges the direct contrast:
  * **Ungoverned LLM:** Hallucinates contradictory delivery rates (94% vs 66%) because it lacks semantic grounding.
  * **Governed CoCo Ontology:** Resolves canonical formulas across all dimensions, guaranteeing 100% mathematical consistency.

### Step 3: Tab 3 — Cortex Unstructured Contract Intelligence
* Click **Tab 3: Cortex Contract Clause Investigator**.
* Show the live Cortex Search query:
  * "What are the liquidated damages penalties for Apex Battery Cells?"
  * Point to the cited contract: **Section 8.2** (\$1,500/day after 3-day grace period) and note that routine port congestion **does not qualify as Force Majeure**.

### Step 4: Tab 4 — Closing the Loop via MCP Action
* Click **Tab 4: MCP Action Center**.
* Click **"Trigger Emergency Air-Freight PO via MCP"** $\to$ Show JSON ERP dispatch ticket.
* Click **"Dispatch Formal Breach Notice to Slack"** $\to$ Show the formatted legal warning citation ready for the supplier channel.

---

## 🏆 Scoring Rubric Alignment Checklist (For Judges)

| Rubric Item | How We Demonstrated It |
|---|---|
| **Real-World Relevance** | Automotive EV assembly stockout crisis with port demurrage and SLA penalties. |
| **Full CoCo Lifecycle** | Planning (`docs/architecture_plan.md`), Development (`data/` & `pipelines/`), Execution (Dynamic Tables), and Testing (`tests/`). |
| **Synthetic Data Generation** | Referentially sound relational schema + realistic contract MSAs. |
| **Data Pipelines** | 3 Snowflake Dynamic Tables refreshing every 1 minute on `COMPUTE_WH`. |
| **Semantic Model & Ontology** | Governed semantic YAML with canonical metrics staged in Snowflake. |
| **Document Intelligence** | Snowflake Cortex Search Service (`SUPPLIER_CONTRACTS_SEARCH`) with cosine/reranker scoring. |
| **Streamlit App Generation** | Live deployed Streamlit in Snowflake (SiS) app. |
| **MCP External Actions** | Real-world action tools for automated ERP re-order and Slack alerts. |
| **Testing & Guardrails** | Automated SQL validation test suite testing referential integrity and boundary conditions. |
